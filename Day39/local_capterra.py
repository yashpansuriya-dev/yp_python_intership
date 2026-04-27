import asyncio
import random
import json
from urllib.parse import urljoin

from playwright.async_api import async_playwright


async def scrape(category_name="crm", total_products=5):
    category_query = category_name.lower()
    software_category = category_query.replace(" ", "-") + "-software/"
    start_url = f"https://www.capterra.com/{software_category}"

    results = []
    count_products = 0

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--no-sandbox"]
        )

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        )

        page = await context.new_page()

        print(f"Opening: {start_url}")
        await page.goto(start_url, timeout=60000)

        # await asyncio.sleep(25)
        # await w
        # Wait until at least 1 product card appears
        await page.wait_for_selector('div[id^="product-card-container-"]', timeout=60000)

        # # Optional: extra safety → wait until multiple cards load
        # await page.wait_for_function("""
        # () => document.querySelectorAll('div[id^="product-card-container-"]').length > 0
        # """)

        # ===== STEP 1: GET PRODUCT LINKS =====
        cards = page.locator('div[id^="product-card-container-"]')
        count_cards = await cards.count()
        print(f"Total cards found: {count_cards}")

        product_urls = []

        for i in range(min(total_products, count_cards)):
            card = cards.nth(i)
            link = card.locator('a:has(button:has-text("View Profile"))')
            href = await link.get_attribute("href")

            if href:
                full_url = urljoin(start_url, href)
                product_urls.append(full_url)

        # ===== STEP 2: SCRAPE EACH PRODUCT =====
        for url in product_urls:
            print(f"\nScraping product: {url}")

            await page.goto(url, timeout=60000)
            await asyncio.sleep(random.uniform(3, 5))

            try:
                title = await page.locator("h1").first.inner_text()

                overview_locator = page.locator("section#key-takeaways div.lg\\:w-7\\/12")
                overview = await overview_locator.inner_text() if await overview_locator.count() > 0 else ""

                reviews = []

                review_cards = page.locator(
                    "div.space-y-6 div.rounded-xl.border.border-neutral-40.bg-card"
                )

                reviews_count = await review_cards.count()
                print(f"Reviews found: {reviews_count}")

                for i in range(reviews_count):
                    review = review_cards.nth(i)

                    try:
                        author_info = review.locator("div.flex.justify-between.items-start div p")

                        author_name = await author_info.nth(0).inner_text()
                        author_profession = await author_info.nth(1).inner_text()
                        author_industry = await author_info.nth(2).inner_text()

                        review_title = await review.locator("h3").inner_text()
                        review_stars = await review.locator(
                            "span.text-typo-20.text-neutral-99"
                        ).first.inner_text()

                        review_date = await review.locator(
                            "p.text-typo-0.text-neutral-90.mb-2"
                        ).inner_text()

                        desc_locator = review.locator(
                            "div.mb-4 p.text-typo-10.text-neutral-99"
                        )
                        review_description = (
                            await desc_locator.first.inner_text()
                            if await desc_locator.count() > 0 else ""
                        )

                        pros = await review.locator(
                            'div:has-text("Pros") + p'
                        ).inner_text()

                        cons = await review.locator(
                            'div:has-text("Cons") + p'
                        ).inner_text()

                        reviews.append({
                            "review_title": review_title,
                            "author_name": author_name,
                            "author_profession": author_profession,
                            "author_industry": author_industry,
                            "review_stars": review_stars,
                            "review_date": review_date,
                            "review_description": review_description,
                            "review_pros": pros,
                            "review_cons": cons
                        })

                    except Exception as e:
                        print(f"Error in one review: {e}")
                        continue

                results.append({
                    "title": title,
                    "overview": overview,
                    "reviews": reviews
                })

                count_products += 1

                if count_products >= total_products:
                    break

            except Exception as e:
                print(f"Error scraping product: {e}")

        await browser.close()

    # ===== SAVE TO FILE =====
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print("\n✅ Data saved to output.json")


# ===== RUN SCRIPT =====
if __name__ == "__main__":
    category = input("Enter software category (e.g. CRM, ERP): ")
    total = int(input("How many products to scrape: "))

    asyncio.run(scrape(category, total))