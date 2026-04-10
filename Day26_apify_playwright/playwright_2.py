import asyncio
from apify import Actor
from playwright.async_api import async_playwright

async def main():
    async with Actor:
        input_data = await Actor.get_input() or {}
        start_urls = input_data.get("start_urls", ["https://books.toscrape.com/"])



        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            for url in start_urls:
                print(f"Opening: {url}")
    
                await page.goto(url)
                                                                                                                                    
                # wait for page load
                await page.wait_for_load_state("networkidle")

                # extract data
                title = await page.title()

                await Actor.push_data({
                    "url": url,
                    "title": title
                })

            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())