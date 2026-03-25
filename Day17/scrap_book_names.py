import requests
from bs4 import BeautifulSoup

# -------------------------------------------------------------------

def print_book_names(num_of_pages = 1):
    """
        It print book name of book.toscrape.com using
        BeautifulSoup scrapping .
    """
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
    }

    print("\nBook Details")
    idx =1
    for i in range(num_of_pages):
        url = f"https://books.toscrape.com/catalogue/page-{i}.html"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        books = soup.select("article.product_pod")

        for book in books:
            name = book.select_one("h3 a").get('title')
            print(f" {idx}. {name}\n")
            idx += 1

# -------------------------------------------------------------------

def main() -> None:
    num_of_pages = 5
    print_book_names(num_of_pages)

# -------------------------------------------------------------------

if __name__ == '__main__':
    main()

