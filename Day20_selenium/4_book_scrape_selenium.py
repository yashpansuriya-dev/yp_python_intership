"""
    It Scrapes bookstoscrape.com with selenium and
    extracts it to csv .
"""

# -------------------------------------------------------------------

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------------------------------------------------------

def save_books_to_csv(num_of_pages):
    try:
        driver = webdriver.Chrome()
        data = {
                'Name': [],
                'Price': [],
                'Rating': []
            }

        driver.get("https://books.toscrape.com")
        driver.implicitly_wait(2)

        wait = WebDriverWait(driver, 10)


        for _ in range(1,num_of_pages+1):
            # scrolls whole page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            books = wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "product_pod"))
            )

            for book in books:
                name = book.find_element("css selector", "h3 > a").get_attribute("title")
                price = book.find_element("class name", "price_color").text[1:]
                rating = book.find_element("tag name", "p").get_attribute("class").split(" ")[1]
                data['Name'].append(name)
                data['Price'].append(float(price))
                data['Rating'].append(rating)

        print(f"Saved {len(data['Name'])} Books Succesfully")
        df = pd.DataFrame(data)
        df.to_csv("books_data.csv")

        driver.close()
    except Exception as e:
        print("Error Occured : ",e)


# -------------------------------------------------------------------

def main() -> None:
    save_books_to_csv(30)

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()
