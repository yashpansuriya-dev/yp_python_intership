from __future__ import annotations
from urllib.parse import urljoin
from apify import Actor, Request
from playwright.async_api import async_playwright

async def main() -> None:

    async with Actor:
        # retruve actor's input
        actor_input = await Actor.get_input() or {}
        job_role = actor_input.get('job_role', "Java Developer")
        max_depth = actor_input.get('max_depth', 1)
        role_query = job_role.replace(" ", "%20")
        start_url = f"https://in.linkedin.com/jobs/search?keywords={role_query}"

        # if job role is empty
        if not job_role:
            Actor.log.info('No Job role specified in Actor input, exiting...')
            await Actor.exit()

        request_queue = await Actor.open_request_queue()

        # Enqueue the start URLs with an initial crawl depth of 0.
        Actor.log.info('Launching Playwright...')

        start_url = f"https://in.linkedin.com/jobs/search?keywords={role_query}"
        new_request = Request.from_url(start_url, user_data={'depth': 0})
        await request_queue.add_request(new_request)
   
        total_jobs = actor_input.get('total_jobs_to_scrape',20)
        count = 0
        stop_scrapping = False

        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless = False)
            context = await browser.new_context()

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
                        jobs_links = await page.locator(".base-card__full-link").all()


                    elif depth == 1:
                        job_role = await page.locator("h1.topcard__title").inner_text()

                  
                except Exception:
                    Actor.log.exception(f'Cannot extract data from {url}.')

                finally:
                    await page.close()
                    await request_queue.mark_request_as_handled(request)
