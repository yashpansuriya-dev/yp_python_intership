import requests
from bs4 import BeautifulSoup

# -------------------------------------------------------------------

def collect_book_details(num_of_pages = 1) -> list:
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
    try:
        # Scarapping pages
        for i in range(1, num_of_pages+1):
            url = f"https://books.toscrape.com/catalogue/page-{i}.html"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            books = soup.select("article.product_pod")

            # Storing books_details
            for book in books:
                name = book.select_one("h3 a").get('title')
                price = book.select_one(".price_color").text
                rating = book.select_one(".star-rating")["class"][1]

                book_details.append({'name':name, 
                                     'price' : float(price[2:]),
                                     'rating' : rating})
    except Exception as e:
        print(e)
    else:
        return book_details
            

def sort_by_price_low_to_high(books):
    books_sorted_asc = sorted(books, key= lambda x : x['price'])
    return books_sorted_asc

def sort_by_price_high_to_low(books):
    books_sorted_desc = sorted(books, key= lambda x : x['price'], reverse=True)
    return books_sorted_desc

# -------------------------------------------------------------------

def main() -> None:
    num_of_pages = int(input("How Many Pages Do you want to Scrap (Between 1 to 40) : "))
    books = collect_book_details(num_of_pages)

    print("\nTotal no. of books are : ", len(books))


    sorted_books = sort_by_price_low_to_high(books)
    print("Books Sorted by Price Low to High")
    print("-"*80)
    for book in sorted_books:
        print(book)

    sorted_books_reverse = sort_by_price_high_to_low(books)
    print("\n\nBooks Sorted by Price High To Low")
    print("-"*80)
    for book in sorted_books_reverse:
        print(book)
# -------------------------------------------------------------------

if __name__ == '__main__':
    main()

