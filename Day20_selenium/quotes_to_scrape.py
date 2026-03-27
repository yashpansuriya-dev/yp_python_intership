import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------------------------------------------------------

def save_quotes_to_csv(num_of_quotes):
    try:
        driver = webdriver.Chrome()
        data = {
                'Quote': [],
                'Author': [],
                'Tags': []
            }
        
        driver.get("https://quotes.toscrape.com/scroll")
        driver.implicitly_wait(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        wait = WebDriverWait(driver, 10)

        while len(data['Quote']) < num_of_quotes:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            quotes = wait.until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "quote"))
                )

            for quote in quotes:
                quote_text = quote.find_element("class name", "text").text
                author  = quote.find_element("css selector", "span > small").text

                tags = quote.find_elements("css selector", ".tags > a")
                tags_list = [tag.text for tag in tags]

                data['Quote'].append(quote_text)
                data['Author'].append(author)                
                data["Tags"].append(tags_list)

                if len(data['Quote']) >= num_of_quotes:
                    break


        df = pd.DataFrame(data)
        print(f"Saved {len(df)} Quotes Succesfully")
        df.to_csv("quotes_data.csv", index=False)

        driver.quit()
    except Exception as e:
        print("Error Occured : ",e)

# -------------------------------------------------------------------

def main() -> None:
    save_quotes_to_csv(30)

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()
