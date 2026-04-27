from __future__ import annotations

import asyncio
import random
from urllib.parse import urljoin

from apify import Actor, Request
from playwright.async_api import Browser, BrowserContext, Page, async_playwright
from typing import Any
from urllib.parse import quote_plus

async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        request_queue = await Actor.open_request_queue(name=None)

        category_name = actor_input.get('software_category', "Ahmedabad")
        category_query = category_name.lower()
        
        software_category = category_query.replace(" ", "-") + "-software/"
        start_url = f"https://www.capterra.com/{software_category}"

        total_products =int(actor_input.get('total_products_to_scrape', 5))

        async with async_playwright() as playwright:

            # proxy_configuration = await Actor.create_proxy_configuration(
            #     groups=["RESIDENTIAL"]
            # )

            # browser = await playwright.chromium.launch(headless=False)
            browser = await playwright.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
            ])
            Actor.log.info(f'Scraping {start_url}.......')

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
            await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
            """)

            try:
                await page.goto(start_url, timeout=60000)
                title = await page.title()
                Actor.log.info(f"Title :::::: ------{title}")
                Actor.log.info(f'-----Scraping {start_url} ...')
                await asyncio.sleep(random.uniform(2, 4))

                cards = page.locator('div[id^="product-card-container-"]')
                count_cards = await cards.count()
                print(f"Total cards found: {count_cards}")

                # for card in cards:
                for i in range(total_products):
                    try:
                        card = cards.nth(i)

                        # -------------------------
                        # ✅ PRODUCT NAME
                        # -------------------------
                        product_name = await card.locator("h2").inner_text()

                        # -------------------------
                        # ✅ PRODUCT URL
                        # -------------------------
                        partial_url = await card.locator("a").first.get_attribute("href")
                        product_url = urljoin(start_url, partial_url)

                        # -------------------------
                        # ✅ RATING + NO OF REVIEWS
                        # -------------------------
                        rating_text = await card.locator("span.sr2r3oj").first.inner_text()
                        # Example: "4.7 (6231)"

                        rating = rating_text.split("(")[0].strip()
                        no_of_reviews = rating_text.split("(")[1].replace(")", "").strip()

                        # -------------------------
                        # ✅ DESCRIPTION
                        # -------------------------
                        description = await card.locator("p.text-neutral-99").first.inner_text()

                        # -------------------------
                        # ✅ FEATURES
                        # -------------------------

                        feature_items = card.locator('[data-testid="product-card-category-features"] div.flex.items-center')

                        count_features = await feature_items.count()

                        included_features = []
                        not_included_features = []

                        for j in range(count_features):
                            feature = feature_items.nth(j)

                            text = await feature.inner_text()

                            # check icon class
                            icon_class = await feature.locator("i").get_attribute("class")

                            if "icon-check" in icon_class:
                                included_features.append(text.strip())
                            elif "icon-x" in icon_class:
                                not_included_features.append(text.strip())


                        # -------------------------
                        # ✅ FINAL DATA
                        # -------------------------

                        data = {
                            "name": product_name,
                            "url": product_url,
                            "rating": rating,
                            "reviews": no_of_reviews,
                            "description": description,
                            "features_included": included_features,
                            "features_not_included": not_included_features
                        }


                        await request_queue.add_request(
                            Request.from_url(link_href, user_data={'depth': 1})
                        )
                        print(data)
                        await Actor.push_data(data)

                    except Exception as e:
                        print("Error:", e)

            except Exception as e:
                Actor.log.exception(f'Error on {start_url}: {e}')

            finally:
                await page.close()
                await context.close()
                # await request_queue.mark_request_as_handled(request)
