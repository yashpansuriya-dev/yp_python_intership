"""
    It Scrapes techforce's Contact Us page
    and saved it to json file .
"""
# erorr handling , consled printing

import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# -------------------------------------------------------------------

URL ="https://techforceglobal.com/contact-us"

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
# Scrapes Title and Contact Us Page
# -------------------------------------------------------------------

def scrape_title(driver):
    print("-"*50)
    return driver.title


def scrape_contact_us(driver):
    try:
        print("-"*50)
        print(f"Scrapping Contact Us Page...")
        time.sleep(5)

        # page title
        title = driver.find_element(By.CSS_SELECTOR, "div.hero-content h1.hero-title").text

        # company_highlights
        company_highlights = []
        highligts_cards = driver.find_elements(By.CSS_SELECTOR, "div.stat-card")
        
        for card in highligts_cards:
            number = card.find_element(By.CSS_SELECTOR, "h3.stat-number").text.strip()
            label = card.find_element(By.CSS_SELECTOR, "p.stat-label").text.strip()

            # Format rules
            if number == "24":
                number = "24*7"
            else:
                number = f"{number}+"

            company_highlights.append(f"{number} {label}")

        # our contacts
        contacts = []
        contacts_cards = driver.find_elements(By.CSS_SELECTOR, ".consultation-card")
        for card in contacts_cards:
            contact_role = card.find_element(By.CSS_SELECTOR, "h4").text
            contact_numer = card.find_elements(By.CSS_SELECTOR, ".card-contact .contact-item a")[0].get_attribute("href")
            contact_email = card.find_elements(By.CSS_SELECTOR, ".card-contact .contact-item a")[1].get_attribute("href")
            
            contacts.append({
                "Role":contact_role,
                "Mobile number" : contact_numer.replace("tel:",""),
                "Email": contact_email.replace("mailto:","")
            })
        
        contact_us = {
            "Title" : title,
            "Company Highlights" : company_highlights,
            "Contact info" : contacts
        }
        print("Contact us Page Scrapped Succesfully")
        print("-"*50)
        return contact_us
    except Exception as e:
        print("Error occured while scrapping",e)

def filing_contact_us_form(driver):
    print("-"*50)
    print("Filing Contact us Form....")
    try:
        f_name = driver.find_element(By.CSS_SELECTOR, "#First_Name").send_keys("mihir")
        l_name = driver.find_element(By.CSS_SELECTOR, "#Last_Name").send_keys("patel")
        email = driver.find_element(By.CSS_SELECTOR, "#Email").send_keys("randommail@gmail.com")
        phone = driver.find_element(By.CSS_SELECTOR, "#Phone").send_keys("9856741112")
        budget = Select(driver.find_element(By.CSS_SELECTOR, "#LEADCF10")).select_by_value("Between 10K to 50K")
        category = Select(driver.find_element(By.CSS_SELECTOR, "#LEADCF9")).select_by_value("Fintech Solution")
        description = driver.find_element(By.CSS_SELECTOR, "#Description").send_keys("random text")

        submit_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")

        # Uncomment Below Line if Want to Submit Form(Otherwise It Fills dummy data)
        # driver.execute_script("arguments[0].click()", submit_btn)
        
        print("Form filled Succesfully")
        print("-"*50)

    except Exception as e:
        print("Error occured while filing form ",e)


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
    
    contact_us = scrape_contact_us(driver)
    save_to_json("contact_us_page.json", contact_us)

    # If Wanted to fill form , uncomment Below Line
    # filing_contact_us_form(driver)

    driver.quit()
    

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()
