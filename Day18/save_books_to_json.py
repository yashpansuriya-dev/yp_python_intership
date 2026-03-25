import requests
from bs4 import BeautifulSoup
import json

# -------------------------------------------------------------------

def save_books_to_json(filename: str, num_of_pages : int = 1) -> list:
    """
        It saves books details such as name, price, rating
        into a json file .

        Args :
            filename : name of file to save
            num_of_pages : no. of pages of website to scrape
    """

    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
    }

    book_details = []

    # Scrapping Webiste and collecting data
    for i in range(1, num_of_pages+1):
        try:
            url = f"https://books.toscrape.com/catalogue/page-{i}.html"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            books = soup.select("article.product_pod")

            for book in books:
                name = book.select_one("h3 a").get('title')
                price = book.select_one(".price_color").text
                rating = book.select_one(".star-rating")["class"][1]

                book_details.append({'name':name, 
                                    'price' : price[-5:],
                                    'rating' : rating})
        except ConnectionError as e:
            print("Network error",e)
        except Exception as e:
            print(e)
        
    # Save to JSON file
    try:
        with open(filename, "w", encoding="utf8") as f:
            json.dump(book_details, f, indent=4)
    except Exception as e:
        print("Error occured : ",e)
    else:
        print("Saved Successfully")

        
    return book_details

# -------------------------------------------------------------------

def main() -> None:
    num_of_pages = 5
    books = save_books_to_json("Database/books_data.json" , num_of_pages)

    print("Total no. of books are : ", len(books))


# -------------------------------------------------------------------

if __name__ == '__main__':
    main()

