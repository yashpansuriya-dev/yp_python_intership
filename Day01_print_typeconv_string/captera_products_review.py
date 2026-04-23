from __future__ import annotations

import asyncio
import random
import sys
from typing import Any
from urllib.parse import quote_plus
from urllib.parse import urljoin

from apify import Actor, Request
from playwright.async_api import Browser, BrowserContext, Page, async_playwright
sys.stdout.reconfigure(encoding='utf-8')

async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        category_name = actor_input.get('software_category', "Ahmedabad")
        category_query = category_name.lower()
        
        software_category = category_query.replace(" ", "-") + "-software/"
        start_url = f"https://www.capterra.com/{software_category}"


        request_queue = await Actor.open_request_queue(name=None)

        await request_queue.add_request(
            Request.from_url(start_url, user_data={'depth': 0})
        )

        total_products =int(actor_input.get('total_products_to_scrape', 5))
        count_products = 0
        stop_scrapping = False

        async with async_playwright() as playwright:

            # proxy_configuration = await Actor.create_proxy_configuration(
            #     groups=["RESIDENTIAL"]
            # )

            browser = await playwright.chromium.launch(
            headless=False,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
            ])

            while not stop_scrapping and (request := await request_queue.fetch_next_request()):
                url = request.url
                depth = int(request.user_data['depth'])

                Actor.log.info(f'Scraping {url} (depth={depth}) ...')

                # ROTATE PROXY PER REQUEST
                # proxy_info = await proxy_configuration.new_proxy_info()

                context = await browser.new_context(
                    # proxy={
                    #     "server": proxy_info.url,
                    #     "username": proxy_info.username,
                    #     "password": proxy_info.password,
                    # },
                    # user_agent=random.choice([
                    #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                    # ]),
                    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                )

                page = await context.new_page()

                # remove webdriver flag
                await page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                    window.chrome = { runtime: {} };
                    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
                    """)

                try:
                    await page.goto(url, timeout=60000)

                    await asyncio.sleep(random.uniform(2, 4))
                    await page.mouse.move(100, 200)
                    await page.wait_for_timeout(1000)
                    await page.mouse.move(300, 400)

                    if depth == 0:
                        await asyncio.sleep(7)  # wait 5 seconds

                        cards = page.locator('div[id^="product-card-container-"]')
                        count_cards = await cards.count()
                        print(f"Total cards found: {count_cards}")

                        for i in range(total_products):
                            card = cards.nth(i)
                            link = card.locator('a:has(button:has-text("View Profile"))')
                            link_href = await link.get_attribute('href')
                            product_url = urljoin(start_url, link_href)

                            if link_href:
                                await request_queue.add_request(
                                    Request.from_url(product_url, user_data={'depth': 1})
                                )
                            
                    elif depth == 1:
                        # Product title
                        title = await page.locator("h1").first.inner_text()
                        Actor.log.info(title)

                        # product overview
                        # overview_card = page.locator("section#key-takeaways div.lg:w-7/12")
                        # overview = overview_card.inner_text()
                        overview_card = page.locator("section#key-takeaways div.lg\\:w-7\\/12")

                        # if await overview_card.count() > 0:
                        overview = await overview_card.inner_text()
                        # else:
                            # overview = ""


                        # Fetch reviews
                        reviews = []

                        review_cards = page.locator("div.space-y-6 div.rounded-xl.border.border-neutral-40.bg-card.text-card-foreground.shadow-elevation-2.p-6")
                        reviews_count = await review_cards.count()
                        Actor.log.info(f"total reviews counted -- {reviews_count}")

                        # for review in review_cards:
                        for i in range(reviews_count):
                            review = review_cards.nth(i)
                            author_info = review.locator("div.flex.justify-between.items-start div p")

                            author_name = await author_info.nth(0).inner_text()
                            author_profession = await author_info.nth(1).inner_text()
                            author_industry = await author_info.nth(2).inner_text()

                            # Actor.log.info()

                            review_title = await review.locator("h3").inner_text()
                            review_stars = await review.locator("span.text-typo-20.text-neutral-99").first.inner_text()
                            review_date = await review.locator("p.text-typo-0.text-neutral-90.mb-2").inner_text()
                            # review_description = await review.locator("div.mb-4 p.text-typo-10.text-neutral-99").inner_text()
                            
                            desc_locator = review.locator("div.mb-4 p.text-typo-10.text-neutral-99")
                            if await desc_locator.count() > 0:
                                review_description = await desc_locator.first.inner_text()
                            else:
                                review_description = ""
                            pros_text = await review.locator(
                                'div.flex.items-center.gap-2.mb-2:has(span.text-typo-10.font-semibold.text-neutral-99:has-text("Pros")) + p.text-typo-20.text-neutral-90.mt-2'
                            ).inner_text()

                            cons_text = await review.locator(
                                'div.flex.items-center.gap-2.mb-2:has(span.text-typo-10.font-semibold.text-neutral-99:has-text("Cons")) + p.text-typo-20.text-neutral-90.mt-2'
                            ).inner_text()

                            # cons_text = await page.locator(
                            #     'div:has(span:has-text("Cons")) + p'
                            # ).inner_text()

                            reviews.append({
                                "review_title":review_title,
                                "author_name":author_name,
                                "author_profession":author_profession,
                                "author_industry":author_industry,
                                "review_stars":review_stars,
                                "review_date":review_date,
                                "review_description":review_description,
                                "review_pros":pros_text,
                                "review_cons":cons_text
                            })


                        data = {
                            "title":title,
                            "overview":overview,
                            "reviews":reviews
                        }

                        await Actor.push_data(data)
                        count_products += 1

                        if count_products >= total_products:
                            stop_scrapping = True
            
                except Exception as e:
                    Actor.log.exception(f'Error on {url}: {e}')

                finally:
                    await page.close()
                    await context.close()
                    await request_queue.mark_request_as_handled(request)
