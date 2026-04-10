import asyncio
from apify import Actor
from playwright.async_api import async_playwright

async def main():
    async with Actor:
        input_data = await Actor.get_input() or {}
        start_urls = input_data.get("start_urls", ["https://books.toscrape.com/"])

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless= False)
            page = await browser.new_page()

            await page.goto(start_urls[0])
            await page.wait_for_selector(".product_pod")
            books = page.locator(".product_pod")
            count_books = await books.count()
            for i in range(count_books):
                title = await books.nth(i).locator("h3").inner_text()
                price = await books.nth(i).locator("p.price_color").inner_text()
                print(f" {title}   :   {price}")

                await Actor.push_data({
                    "title":title,
                    "price":price
                })

            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())