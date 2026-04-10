import asyncio
import httpx
from bs4 import BeautifulSoup
from apify import Actor

async def main():
    async with Actor:
        # 📥 Get input
        input_data = await Actor.get_input() or {}
        start_urls = input_data.get("start_urls", ["https://books.toscrape.com/"])

        async with httpx.AsyncClient() as client:
            for url in start_urls:
                print(f"Scraping: {url}")

                # 🌐 Fetch page
                response = await client.get(url)
                html = response.text

                # 🧠 Parse HTML
                soup = BeautifulSoup(html, "lxml")

                # 🎯 Extract data
                title = soup.title.string if soup.title else "No title"

                # 📦 Save to dataset
                await Actor.push_data({
                    "url": url,
                    "title": title
                })

if __name__ == "__main__":
    asyncio.run(main())