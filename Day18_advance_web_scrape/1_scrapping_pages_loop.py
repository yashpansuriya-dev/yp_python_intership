import requests
import time
from bs4 import BeautifulSoup

# -------------------------------------------------------------------

def collect_book_details(num_of_pages) -> dict:
    """
        It returns list containing books details such as 
        book name,price, rating  scrapped from book.toscrape.com using
        BeautifulSoup scrapping .

        Args :
            num_of_pages : no. of pages of website to scrape
        
        Returns :
            list : list of dicts containing books details
    """

    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
    }

    book_details = []
    
    for i in range(1, num_of_pages+1):
        try:
            time.sleep(5)
            url = f"https://books.toscrape.com/catalogue/page-{i}.html"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            books = soup.select("article.product_pod")

            for book in books:
                name = book.select_one("h3 a").get('title')
                price = book.select_one(".price_color").text
                rating = book.select_one(".star-rating")["class"][1]

                book_details.append({'name':name, 
                                    'price' : price,
                                    'rating' : rating})
        
        except Exception as e:
            print(e)
        else:
            print(f"page {i} scrapped succesfully")
            
    return book_details
        

# -------------------------------------------------------------------

def main() -> None:
    num_of_pages = 5
    books = collect_book_details(num_of_pages)

    print("Total no. of books are : ", len(books))

    for book in books:
        print(book)

# -------------------------------------------------------------------

if __name__ == '__main__':
    main()

