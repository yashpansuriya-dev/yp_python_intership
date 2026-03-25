import requests
from bs4 import BeautifulSoup
import csv

# -------------------------------------------------------------------

def collect_book_details(filename, num_of_pages = 1) -> list:
    """
        It saves books details such as name, price, rating
        into a csv file .

        Args :
            filename : name of file to save
            num_of_pages : no. of pages of website to scrape
    """
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
    }

    book_details = []
    fields = ["name", "price", "rating"]      


    # Scrapping webiste and  collecting data
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

                book_details.append([name, price, rating])
        except ConnectionError as e:
            print("Network error",e)
        except Exception as e:
            print(e)


    # Saving to CSV file  
    try:
        with open(filename, "w", newline="", encoding="utf8") as f:
            writer = csv.writer(f)
            writer.writerow(fields)
            writer.writerows(book_details)
    except Exception as e:
        print("Error occured : ",e)
    else:
        print("Saved Successfully")

        
    return book_details

# -------------------------------------------------------------------

def main() -> None:
    num_of_pages = 5
    books = collect_book_details("Database/books_data2.csv" , num_of_pages)

    print("Total no. of books are : ", len(books))

    # for book in books:
    #     print(book)

# -------------------------------------------------------------------

if __name__ == '__main__':
    main()



"""
    try:
        with open(file_name, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(fields)
            writer.writerows(rows)
    except PermissionError:
        print("File is not accessible")
    except Exception:
        print("Some Interupttion occurs")

"""