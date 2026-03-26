import requests
from bs4 import BeautifulSoup

# -------------------------------------------------------------------

def collect_book_details(num_of_pages=1) -> list:
    """
    Returns list of book details (name, price, rating)
    scraped from books.toscrape.com with improved try,except 
    leaves blank if no tag,missing attribute .

    Args:
        num_of_pages (int): number of pages to scrape

    Returns:
        list: list of dictionaries
    """

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    book_details = []

    for i in range(1, num_of_pages + 1):

        url = f"https://books.toscrape.com/catalogue/page-{i}.html"

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                print(f"Failed to fetch page {i}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            books = soup.select("article.product_pod")

            for book in books:
                # TITLE
                try:
                    name = book.select_one("h3 a").get("title")
                except (AttributeError, TypeError, KeyError):
                    name = "No title"

                # PRICE
                try:
                    price = book.select_one(".price_color").text
                except Exception:
                    price = "No price"

                # RATING
                try:
                    rating = book.select_one(".star-rating")["class"][1]
                except Exception:
                    rating = "No rating"

                book_details.append({
                    "name": name,
                    "price": price,
                    "rating": rating
                })

            print(f"Page {i} scraped successfully")

        except requests.exceptions.RequestException as e:
            print(f"Request failed on page {i}: {e}")

        except Exception as e:
            print(f"Unexpected error on page {i}: {e}")

    return book_details


# -------------------------------------------------------------------

def main() -> None:
    num_of_pages = 0
    books = collect_book_details(num_of_pages)

    print("\nTotal no. of books are:", len(books))

    for book in books:
        print(book)


# -------------------------------------------------------------------

if __name__ == '__main__':
    main()