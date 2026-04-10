# -------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup
from apify import Actor
import asyncio
# -------------------------------------------------------------------


async def main():
    async with Actor:
        url = "https://books.toscrape.com/"

        headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        books_details = []

        books = soup.select("article.product_pod")

        for book in books:
            name = book.select_one("h3 a").get('title')
            price = book.select_one(".price_color").text
            rating = book.select_one(".star-rating")["class"][1]

            await Actor.push_data({
                "name": name,
                "price" : price,
                "rating" : rating
            })

# -------------------------------------------------------------------
# -------------------------------------------------------------------    

if __name__ == "__main__":
    asyncio.run(main())