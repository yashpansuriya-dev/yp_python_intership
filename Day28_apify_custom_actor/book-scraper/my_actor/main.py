"""Module defines the main entry point for the Apify Actor.

Feel free to modify this file to suit your specific needs.

To build Apify Actors, utilize the Apify SDK toolkit, read more at the official documentation:
https://docs.apify.com/sdk/python
"""

from __future__ import annotations
from urllib.parse import urljoin
from apify import Actor, Request
from playwright.async_api import async_playwright


async def main() -> None:

    # Enter the context of the Actor.
    async with Actor:
        # Retrieve the Actor input, and use default values if not provided.
        actor_input = await Actor.get_input() or {}
        start_urls = actor_input.get('start_urls', [{'url': 'https://books.toscrape.com/'}])
        max_depth = actor_input.get('max_depth', 1)

        # Exit if no start URLs are provided.
        if not start_urls:
            Actor.log.info('No start URLs specified in Actor input, exiting...')
            await Actor.exit()

        # Open the default request queue for handling URLs to be processed.
        request_queue = await Actor.open_request_queue()

        for item in start_urls:
            url = item["url"]
            new_request = Request.from_url(url,user_data={"depth": 0})
            await request_queue.add_request(new_request)

        # Enqueue the start URLs with an initial crawl depth of 0.
        max_page = actor_input.get('max_pages_to_scrape',5)
        total_books = actor_input.get('total_books_to_scrape',20)
        count = 0
        stop_scrapping = False

        Actor.log.info(f"scraping up to {max_page} Pages...")
        Actor.log.info(f"scraping total {total_books} Books...")


        for i in range(2,max_page+1):
            url = f"https://books.toscrape.com/catalogue/page-{i}.html"
            new_request = Request.from_url(url, user_data={'depth': 0})
            await request_queue.add_request(new_request)

        Actor.log.info('Launching Playwright...')

        # Launch Playwright and open a new browser context.
        async with async_playwright() as playwright:
            # Configure the browser to launch in headless mode as per Actor configuration.
            browser = await playwright.chromium.launch(
                headless=Actor.configuration.headless,
                args=['--disable-gpu'],
            )
            context = await browser.new_context()

            # Process the URLs from the request queue.
            while not stop_scrapping and (request := await request_queue.fetch_next_request()):
                url = request.url

                if not isinstance(request.user_data['depth'], (str, int)):
                    raise TypeError('Request.depth is an unexpected type.')

                depth = int(request.user_data['depth'])
                Actor.log.info(f'Scraping {url} (depth={depth}) ...')

                try:
                    # Open a new page in the browser context and navigate to the URL.
                    page = await context.new_page()
                    await page.goto(url)

                    if depth == 0:
                    # 🔹 Listing page → extract product links
                        books_links = await page.locator(".product_pod h3 a").all()

                        for link in books_links:
                            link_href = await link.get_attribute('href')
                            link_url = urljoin(url, link_href)

                            new_request = Request.from_url(
                                link_url,
                                user_data={'depth': 1}
                            )
                            await request_queue.add_request(new_request)

                    elif depth == 1:
                        # 🔹 Product page → extract data
                        data = {
                            'url': url,
                            'title': await page.locator("h1").inner_text(),
                            'price': await int(page.locator(".price_color").nth(0).inner_text().replace('£','')),
                            'product_desc': await page.locator("#product_description + p").inner_text()
                        }
                        count += 1
                        await Actor.push_data(data)

                        if (count >= total_books):
                            stop_scrapping = True
                            
                  
                except Exception:
                    Actor.log.exception(f'Cannot extract data from {url}.')

                finally:
                    await page.close()
                    # Mark the request as handled to ensure it is not processed again.
                    await request_queue.mark_request_as_handled(request)
