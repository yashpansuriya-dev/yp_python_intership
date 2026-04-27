from __future__ import annotations

import asyncio
import os
import random
import sys
from urllib.parse import urljoin

from apify import Actor, Request
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")


CF_TITLES = {
    "just a moment",
    "attention required!",
    "please wait...",
    "checking your browser",
    "one more step",
    "security check",
    "access denied",
}

VIEWPORTS = [
    {"width": 1280, "height": 720},
    {"width": 1366, "height": 768},
    {"width": 1440, "height": 900},
    {"width": 1920, "height": 1080},
]


async def human_delay(min_s=1.0, max_s=2.5):
    await asyncio.sleep(random.uniform(min_s, max_s))


async def human_mouse_wander(page):
    for _ in range(random.randint(3, 6)):
        await page.mouse.move(
            random.randint(80, 1200),
            random.randint(80, 700),
            steps=random.randint(10, 25),
        )
        await asyncio.sleep(random.uniform(0.08, 0.25))


async def random_scroll(page):
    for _ in range(random.randint(2, 4)):
        await page.evaluate(f"window.scrollBy(0, {random.randint(250, 650)})")
        await asyncio.sleep(random.uniform(0.35, 0.8))


async def wait_for_cloudflare(page, timeout_s=180, *, allow_manual=True) -> bool:
    deadline = asyncio.get_event_loop().time() + timeout_s
    manual_notice_shown = False

    while asyncio.get_event_loop().time() < deadline:
        try:
            title = (await page.title()).lower().strip()
        except Exception:
            title = ""

        Actor.log.info(f"[CF] title='{title}'")

        challenge_count = await page.locator(
            "iframe[src*='challenges.cloudflare.com'],"
            "iframe[src*='hcaptcha.com'],"
            "div#challenge-form,"
            "div#cf-challenge-running"
        ).count()

        if challenge_count:
            if not allow_manual:
                Actor.log.warning("[CF] Checkbox/challenge found. Run headed to verify manually.")
                return False
            if not manual_notice_shown:
                Actor.log.warning("[CF] Click the checkbox in the opened browser; the actor will continue.")
                manual_notice_shown = True
            await asyncio.sleep(2)
            continue

        if not any(keyword in title for keyword in CF_TITLES):
            Actor.log.info("[CF] Challenge cleared")
            return True

        await human_mouse_wander(page)
        await asyncio.sleep(2)

    Actor.log.warning("[CF] Timed out waiting for challenge to clear.")
    return False


async def launch_browser(playwright, *, headless: bool):
    args = [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-blink-features=AutomationControlled",
        "--window-size=1366,768",
    ]

    if os.name == "nt":
        try:
            Actor.log.info(f"Launching installed Google Chrome headless={headless}")
            return await playwright.chromium.launch(channel="chrome", headless=headless, args=args)
        except Exception as e:
            Actor.log.warning(f"Chrome channel failed, using bundled Chromium: {e}")

    Actor.log.info(f"Launching bundled Chromium headless={headless}")
    return await playwright.chromium.launch(headless=headless, args=args)


async def make_context(browser):
    viewport = random.choice(VIEWPORTS)
    return await browser.new_context(
        viewport=viewport,
        screen=viewport,
        locale="en-US",
        timezone_id="America/New_York",
        color_scheme="light",
        java_script_enabled=True,
        accept_downloads=False,
    )


async def goto_verified(page, url: str, *, headless: bool) -> bool:
    response = await page.goto(url, wait_until="domcontentloaded", timeout=60_000)
    Actor.log.info(f"HTTP {response.status if response else '?'} {url}")
    return await wait_for_cloudflare(
        page,
        timeout_s=45 if headless else 180,
        allow_manual=not headless,
    )


async def optional_inner_text(locator, default="") -> str:
    try:
        if await locator.count() == 0:
            return default
        return " ".join((await locator.first.inner_text()).split())
    except Exception:
        return default


async def optional_raw_inner_text(locator, default="") -> str:
    try:
        if await locator.count() == 0:
            return default
        return (await locator.first.inner_text()).strip()
    except Exception:
        return default


async def scrape_product_card(card, start_url: str) -> dict | None:
    try:
        product_name = await optional_inner_text(card.locator("h2"))
        partial_url = await card.locator('a[href*="/p/"]').first.get_attribute("href")
        product_url = urljoin(start_url, partial_url).rstrip("/") if partial_url else ""

        rating_text = await optional_inner_text(card.locator("span.sr2r3oj").first)
        rating = rating_text.split("(")[0].strip() if rating_text else ""
        no_of_reviews = ""
        if "(" in rating_text and ")" in rating_text:
            no_of_reviews = rating_text.split("(", 1)[1].split(")", 1)[0].strip()

        description = await optional_inner_text(card.locator("p.text-neutral-99").first)

        # included_features = []
        # not_included_features = []
        # feature_items = card.locator(
        #     '[data-testid="product-card-category-features"] div.flex.items-center,'
        #     '[data-test-id="product-card-category-features"] div.flex.items-center'
        # )
        # for i in range(await feature_items.count()):
        #     feature = feature_items.nth(i)
        #     text = await optional_inner_text(feature)
        #     icon_class = await feature.locator("i").first.get_attribute("class") or ""
        #     if "icon-check" in icon_class:
        #         included_features.append(text)
        #     elif "icon-x" in icon_class:
        #         not_included_features.append(text)

        if not product_url:
            return None

        return {
            "name": product_name,
            "url": product_url,
            "rating": rating,
            "reviews_count": no_of_reviews,
            "description": description,
        }
    except Exception as e:
        Actor.log.warning(f"Product card parse error: {e}")
        return None


async def scrape_review_page(page) -> tuple[list[dict], bool]:
    await random_scroll(page)
    await human_delay(1.0, 2.0)

    container = page.locator('div[data-test-id="review-cards-container"]')
    review_cards = container.locator("div.e1xzmg0z.c1ofrhif.typo-10")
    reviews_count = await review_cards.count()
    Actor.log.info(f"  Reviews on this page: {reviews_count}")

    if reviews_count == 0:
        return [], False

    reviews = []
    for i in range(reviews_count):
        review = review_cards.nth(i)
        try:
            author_text = await optional_raw_inner_text(review.locator("div.typo-10.text-neutral-90"))
            lines = [line.strip() for line in author_text.split("\n") if line.strip()]

            pros_locator = review.locator("span:has-text('Pros') >> xpath=../following-sibling::p")
            cons_locator = review.locator("span:has-text('Cons') >> xpath=../following-sibling::p")

            reviews.append({
                "review_title": (await optional_inner_text(review.locator("h3"))).replace('"', ""),
                "author_name": lines[0] if len(lines) > 0 else "",
                "author_profession": lines[1] if len(lines) > 1 else "",
                "author_industry": lines[2] if len(lines) > 2 else "",
                "author_duration": lines[3] if len(lines) > 3 else "",
                "review_stars": await optional_inner_text(review.locator("span.sr2r3oj").nth(0)),
                "review_date": await optional_inner_text(review.locator("div.typo-0")),
                "review_description": await optional_inner_text(review.locator("div.space-y-6 > p")),
                "review_pros": await optional_inner_text(pros_locator),
                "review_cons": await optional_inner_text(cons_locator),
            })
        except Exception as e:
            Actor.log.warning(f"Review {i} parse error: {e}")

    return reviews, True


async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        category_name = actor_input.get("software_category", "Application Development")
        total_products = int(actor_input.get("total_products_to_scrape", 5))
        max_review_pages = max(1, min(100, int(actor_input.get("review_pages_per_product", 1))))
        max_cf_retries = int(actor_input.get("max_cf_retries", 2))
        headless = bool(actor_input.get("headless", False))

        category_query = category_name.lower().replace(" ", "-")
        start_url = f"https://www.capterra.com/{category_query}-software/"

        request_queue = await Actor.open_request_queue(name=None)
        await request_queue.add_request(Request.from_url(start_url, user_data={"depth": 0, "retries": 0}))

        products_done = 0

        async with async_playwright() as playwright:
            browser = await launch_browser(playwright, headless=headless)
            context = await make_context(browser)

            while products_done < total_products and (request := await request_queue.fetch_next_request()):
                page = await context.new_page()
                url = request.url
                depth = int(request.user_data.get("depth", 0))
                retries = int(request.user_data.get("retries", 0))
                Actor.log.info(f"→ {url} depth={depth} retry={retries}/{max_cf_retries}")

                try:
                    if not await goto_verified(page, url, headless=headless):
                        if retries < max_cf_retries:
                            await request_queue.add_request(
                                Request.from_url(
                                    url,
                                    unique_key=f"{url}#retry-{retries + 1}-{random.random()}",
                                    user_data={**request.user_data, "retries": retries + 1},
                                ),
                                forefront=True,
                            )
                        continue

                    await human_delay(1.5, 3.0)
                    await human_mouse_wander(page)

                    if depth == 0:
                        await page.wait_for_selector('div[id^="product-card-container-"]', timeout=30_000)
                        cards = page.locator('div[id^="product-card-container-"]')
                        count_cards = await cards.count()
                        Actor.log.info(f"Cards on page: {count_cards}")

                        for i in range(min(total_products, count_cards)):
                            product = await scrape_product_card(cards.nth(i), start_url)
                            if not product:
                                continue

                            review_url = f"{product['url']}/reviews/?page=1"
                            await request_queue.add_request(
                                Request.from_url(
                                    review_url,
                                    user_data={
                                        "depth": 1,
                                        "retries": 0,
                                        "current_page": 1,
                                        "product": product,
                                        "all_reviews": [],
                                    },
                                )
                            )
                            Actor.log.info(f"Queued reviews: {review_url}")

                    elif depth == 1:
                        current_page = int(request.user_data.get("current_page", 1))
                        product = request.user_data.get("product", {})
                        all_reviews = request.user_data.get("all_reviews", [])

                        if current_page == 1:
                            page_title = await optional_inner_text(page.locator("h1"))
                            overview = await optional_inner_text(page.locator("section#key-takeaways div.lg\\:w-7\\/12"))
                            product["review_page_title"] = page_title
                  

                        page_reviews, has_more = await scrape_review_page(page)
                        all_reviews.extend(page_reviews)

                        next_page = current_page + 1
                        if has_more and page_reviews and next_page <= max_review_pages:
                            base_url = product["url"]
                            await request_queue.add_request(
                                Request.from_url(
                                    f"{base_url}/reviews/?page={next_page}",
                                    user_data={
                                        "depth": 1,
                                        "retries": 0,
                                        "current_page": next_page,
                                        "product": product,
                                        "all_reviews": all_reviews,
                                    },
                                ),
                                forefront=True,
                            )
                        else:
                            await Actor.push_data({
                                **product,
                                "total_reviews_scraped": len(all_reviews),
                                "reviews": all_reviews,
                            })
                            products_done += 1
                            Actor.log.info(f"Done {products_done}/{total_products}: {product.get('name')}")

                except Exception as e:
                    Actor.log.exception(f"Error on {url}: {e}")

                finally:
                    await page.close()
                    await request_queue.mark_request_as_handled(request)

            await context.close()
            await browser.close()
