""""
    CSS Selector :
    select -> selects all attributes matching, returns list
    select_one -> single element

    selectors :
        selector   example

        tag          h3 , a
        class        .product-pod , .price-color
        id           #myid , #product-pod
        nested         h3.product-pod             h3 with product-pod class
        inside element     h3 a                      h3->a
        attributes          a[href]               who has attribute

    link= tag.get('href') or tag['href']
    class = tag.get('class') or tag['class']

    soup.select("article.product_pod h3 a")

    here , 
        book.find("h3").find("a").get("title")
        book.select_one("h3 a").get("title")
    
"""

# -------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup

# -------------------------------------------------------------------


def save_book_details() -> dict :
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

        books_details.append({
            "name": name,
            "price" : price,
            "rating" : rating
        })
    
    return books_details

# -------------------------------------------------------------------

def main() -> None :
    books = save_book_details()

    print("Book Details")
    for book in books:
        print(book)

# -------------------------------------------------------------------    

if __name__ == "__main__":
    main()