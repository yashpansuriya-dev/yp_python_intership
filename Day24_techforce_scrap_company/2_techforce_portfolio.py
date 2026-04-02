"""
    It Scrapes techforce's Portfolio page
    and saved it to json file .

"""

import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# -------------------------------------------------------------------

URL ="https://techforceglobal.com/our-work"

# -------------------------------------------------------------------
# Setup
# -------------------------------------------------------------------

def setup_driver(URL):
    print(f"Fetching {URL}...")
    driver = webdriver.Chrome()
    driver.get(URL)
    driver.implicitly_wait(5)
    return driver

def get_wait(driver, timeout = 10):
    wait = WebDriverWait(driver, timeout)
    return wait

# -------------------------------------------------------------------
# Utility Functions
# -------------------------------------------------------------------

def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# -------------------------------------------------------------------
# Scrappes title and Portfolio Page
# -------------------------------------------------------------------

def scrape_title(driver):
    print("-"*50)
    return driver.title


def scrape_portfolio(driver,wait):
    try:
        print("-"*50)
        print(f"Scrapping Portfolio Page...")
        time.sleep(5)

        # page title
        title = driver.find_element(By.CSS_SELECTOR, "h1.pf-hero-title").text

        # info
        info = driver.find_element(By.CSS_SELECTOR, "p.pf-hero-desc").text


        # projects - category wise
        projects = []
        project_category_buttons = driver.find_elements(By.CSS_SELECTOR, "section.pf-grid-section button.pf-filter-btn")

        # Loops through each category
        for category_button in project_category_buttons:
            category_name = category_button.text
            driver.execute_script("arguments[0].click();", category_button)

            projects_of_category = []

            # it select only visible cards with not(contains(@style,'display: none'))
            projects_cards = driver.find_elements(
                By.XPATH,
                "//div[contains(@class,'pf-cards-grid')]//div[contains(@class,'pf-card-wrapper') and not(contains(@style,'display: none'))]"
            )

            for card in projects_cards:
                title = card.find_element(By.CSS_SELECTOR, ".pf-card-overlay-title").get_attribute("textContent").strip()
                desc = card.find_element(By.CSS_SELECTOR, ".pf-card-overlay-desc").get_attribute("textContent").strip()
                link = card.find_element(By.CSS_SELECTOR , "a").get_attribute("href")

                projects_of_category.append({
                    "Title" : title,
                    "Description":desc,
                    "Link":link
                })
            
            projects.append({
                category_name : projects_of_category
            })
        
        our_portfolio = {
            "Title" : title,
            "Info" : info,
            "Projects" : projects
        }

        print("Portfolio Page Scrapped Succesfully")
        print("-"*50)
        return our_portfolio
    except Exception as e:
        print("Error occured while scrapping",e)


def save_to_json(filename: str, data: list):
    """save list into a json file."""
    # write python list to json file
    try:
        with open(f"Extracted_data/{filename}", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print(f"Data Saved to {filename} Succesfully")
    except Exception as e:
        print("Failed To Save into json file : ",e)

        
# -------------------------------------------------------------------

def main() -> None:

    driver = setup_driver(URL)
    wait = get_wait(driver)
    scroll_to_bottom(driver)
    
    about_techforce = scrape_portfolio(driver, wait)
    save_to_json("portfolio_page.json", about_techforce)

    driver.quit()
    

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()
