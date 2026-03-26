"""
    It Scraped a Book Website With Copleted Logging over 
    console and file . and save it in
    json file .
    
"""
# -------------------------------------------------------------------

import requests
import logging
import json
from bs4 import BeautifulSoup

# -------------------------------------------------------------------

logging.basicConfig(filename="Pages/book_scrape.log" , 
                    level=logging.DEBUG , 
                    format='[%(asctime)s] [%(levelname)s] [%(message)s]')

# -------------------------------------------------------------------

def parse_page():
    '''
        It Parsed url and returns its html text.
    '''
    try:
        headers = {
            'User-Agent' : 'Mozilla/5.0'
        }

        url = f"https://books.toscrape.com/catalogue/page-1.html"
        response = requests.get(url, headers=headers)
        logging.info(f"Fetched URL successfully: {url}")
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch {url} - {e}")
        return None
    

def book_scrape(html) -> list:
    """
        It Scraped books details through html and
        returns list of books.
    """
    try:
        book_details = []
        soup = BeautifulSoup(html, 'html.parser')

        books = soup.select("article.product_pod")

        for book in books:
            name = book.select_one("h3 a").get('title')
            price = book.select_one(".price_color").text
            rating = book.select_one(".star-rating")["class"][1]

            book_details.append({'name':name, 
                                'price' : price[-5:],
                                'rating' : rating})
            
        logging.info(f"Parsed {len(book_details)} books")
        return book_details
    except Exception as e:
        logging.error("Parse Error" , e)
        return None


def save_to_json(filename: str , book_details: list):  
    """
        It saves books details in JSON file .
    """      
    # Save to JSON file
    try:
        with open(filename, "w", encoding="utf8") as f:
            json.dump(book_details, f, indent=4)
        logging.info(f"Books Data Saved in {filename} Succesfully")
    except Exception as e:
        logging.error(f"Error occured in Saving Books to {filename}")

# -------------------------------------------------------------------

def main() -> None :
    """ Main Function"""

    html = parse_page()
    if html:
        books = book_scrape(html)
        if books:
            save_to_json("Pages/book_details.json", books)
        else:
            logging.warning("Skipping Saving Books to file due to file error")
    else:
        logging.warning("Skipping parsing due to fetch failure")

# -------------------------------------------------------------------

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.critical(f"Program crashed: {e}")
