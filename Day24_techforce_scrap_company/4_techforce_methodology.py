"""
    It Scrapes techforce's Methodology page
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

URL ="https://techforceglobal.com/our-methodology/"

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
# Scrapes Title and Methodologies Page
# -------------------------------------------------------------------

def scrape_title(driver):
    print("-"*50)
    return driver.title

def scrape_methodologies(driver,wait):
    try:
        print("-"*50)
        print(f"Scrapping Methodologies Page...")
        time.sleep(5)

        # page title
        title_1 = driver.find_element(By.CSS_SELECTOR, "h1.display-3.fw-bold.text-dark.mb-4.lh-tight").text
        title_2 = driver.find_element(By.CSS_SELECTOR, "span.text-gradient").text
        title = title_1+title_2

        # info
        info = driver.find_element(By.CSS_SELECTOR, "p.tf-hero-desc").text

        # flexible models
        flexible_models = []
        flexible_models_cards = driver.find_elements(By.CSS_SELECTOR, "section.engagement-section div.card")

        for card in flexible_models_cards:
            model_title = card.find_element(By.CSS_SELECTOR, "h3.card-title").text
            model_desc = card.find_element(By.CSS_SELECTOR, "p.card-text").text

            model_check_points_tags = card.find_elements(By.CSS_SELECTOR, "ul li")
            model_check_points= [tag.text.strip() for tag in model_check_points_tags]
            model_link = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        
            flexible_models.append({
                "Title": model_title,
                "Description": model_desc,
                "What's Included": model_check_points,
                "Link": model_link
            })

        # our approch
        our_approch = []
        approch_cards = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "section.approach-section div.approach-card-content"))
        )

        for card in approch_cards:
            approch_step_number = card.find_element(By.CSS_SELECTOR, "div.approach-step-number").text
            approch_title = card.find_element(By.CSS_SELECTOR, "h3.approach-card-title").text
            approch_desc = card.find_element(By.CSS_SELECTOR, "p.approach-card-desc").text

            approch_includes_tags = card.find_elements(By.CSS_SELECTOR, "div.approach-tags span")
            approch_includes = [tag.text for tag in approch_includes_tags]

            our_approch.append({
                "Step ": approch_step_number,
                "Title": approch_title,
                "Description": approch_desc,
                "It includes": approch_includes
            })
        
        #why techforce -  our benifits
        our_benifits = []
        benifits_cards = driver.find_elements(By.CSS_SELECTOR, "section.benefits-section div.bento-item")
        for card in benifits_cards:
            benifit_title = card.find_element(By.CSS_SELECTOR, "h5").text
            benifit_info = card.find_element(By.CSS_SELECTOR, "p").text

            our_benifits.append({
                "Title":benifit_title,
                "Description":benifit_info
            })
        
        # Saved into dict.
        methodologies = {
            "Title" : title,
            "Info": info,
            "Flexible Models" : flexible_models,
            "Our Approches" : our_approch,
            "Our Benifits" : our_benifits
        }

        print("Methodologies page Scrapped Succesfully")
        print("-"*50)
        return methodologies
    
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
    
    methodologies = scrape_methodologies(driver, wait)
    save_to_json("methodology_page.json", methodologies)

    driver.quit()
    

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()
