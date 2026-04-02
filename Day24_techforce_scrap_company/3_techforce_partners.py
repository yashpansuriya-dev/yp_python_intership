"""
    It Scrapes techforce's Partners page
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

URL ="https://techforceglobal.com/partners"

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
# Scrapes Title and Partners Page
# -------------------------------------------------------------------

def scrape_title(driver):
    print("-"*50)
    return driver.title


def scrape_partners(driver):
    try:
        print("-"*50)
        print(f"Scrapping Our Partners Page...")
        time.sleep(5)

        # page title
        title = driver.find_element(By.CSS_SELECTOR, "h1.tp-hero-title").text

        # info
        info = driver.find_element(By.CSS_SELECTOR, "p.tp-hero-desc").text

        # technology partners
        tech_partners = []
        tech_partners_cards = driver.find_elements(By.CSS_SELECTOR, "div.tp-pcard.tp-pcard--aws")

        for card in tech_partners_cards:
            # title - scrape title through logo link
            p_title = card.find_element(By.CSS_SELECTOR, "div.tp-pcard-logo-wrap img").get_attribute("src").split("/")
            partner_title = p_title[-1].replace(".png","")

            partner_role = card.find_element(By.CSS_SELECTOR, "p.tp-pcard-role").text

            partner_info = card.find_element(By.CSS_SELECTOR, "p.tp-pcard-desc").text

            partner_use_cases_tags = card.find_elements(By.CSS_SELECTOR, "div.tp-pcard-tags span")
            partner_use_cases = [tag.text for tag in partner_use_cases_tags]

            partner_link = card.find_element(By.CSS_SELECTOR, "div.tp-pcard-footer a").get_attribute("href")

            tech_partners.append({
                "Title": partner_title,
                "Role": partner_role,
                "Description": partner_info,
                "Use cases": partner_use_cases,
                "Link": partner_link
            })
        
        #afflilate partners
        afflilate_partners = []
        afflilate_partners_cards = driver.find_elements(By.CSS_SELECTOR, "div.tp-bento .tp-bento-cell")

        for card in afflilate_partners_cards:
            # title - scrape title through logo link
            p_title = card.find_element(By.CSS_SELECTOR, ".tp-bento-top img").get_attribute("data-src").split("/")
            partner_title = p_title[-1].replace("-Logo.png","")

            partner_info = card.find_element(By.CSS_SELECTOR, "p.tp-bento-desc").text

            partner_use_cases_tags = card.find_elements(By.CSS_SELECTOR, "div.tp-bento-tags span")
            partner_use_cases = [tag.text for tag in partner_use_cases_tags]

            partner_link = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

            afflilate_partners.append({
                "Title": partner_title,
                "Description": partner_info,
                "Use Cases": partner_use_cases,
                "Link": partner_link
            })
        
        partners = {
            "Title":title,
            "Info":info,
            "Technology partners":tech_partners,
            "Afflilate partners":afflilate_partners
        }

        print("Our Partners page Scrapped Succesfully")
        print("-"*50)
        return partners
    
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
    
    partners = scrape_partners(driver)
    save_to_json("our_partners_page.json", partners)

    driver.quit()
    

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()
