"""
    It Scrapes techforce global website's packages page , and

    returns all details of packages .

    webdriver - control the browser
    EC - wait for specified conditions
    locators - By.CSS_SELECTOR, By.CLASS_NAME

    driver.find_element(By.CSS_SELECTOR, ".my-class) -> returns WebElement object
    driver.find_elements(By.CSS_SELECTOR, ".my-class) -> returns list of WebElement object

"""

# -------------------------------------------------------------------

import json

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import time

# -------------------------------------------------------------------

URL ="https://techforceglobal.com/Best-website-development-services-in-USA/"

# -------------------------------------------------------------------
# Setup
# -------------------------------------------------------------------

def setup_driver(URL):
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
# Title and packages details
# -------------------------------------------------------------------

def fetch_title(driver):
    print("-"*50)
    return driver.title

def fetch_packages(wait):
    packages_data = []
    print("-"*50)
    print(f"Scrapping Package Page...")
    try:
        package_cards_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".pricing-container .pricing-plan"))
        )
        del package_cards_elements[1]

        for package_card in package_cards_elements:
            title = package_card.find_element(By.CSS_SELECTOR, ".plan-title").text
            info = package_card.find_element(By.CSS_SELECTOR, ".plan-description").text
            price = package_card.find_element(By.CSS_SELECTOR, "div.plan-price").text.split()[0]

            whats_included_elements = package_card.find_elements(By.CSS_SELECTOR, "li.feature-included")
            whats_included = [element.text for element in whats_included_elements]

            link = package_card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

            packages_data.append({
                "title":title,
                "info":info,
                "price":price,
                "whats_included":whats_included,
                "link":link
            })

            print(f"{title} Scrapped Succesfully")
            print("-"*50)

        return packages_data
    except Exception as e:
        print("Failed To scrap data : ",e)
        

def save_to_json(data: list):
    """save list into a json file."""
    # write python list to json file
    try:
        with open("Extracted_data/Our_packages.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print("Data Saved to Our_package.json Succesfully")
    except Exception as e:
        print("Failed To Save into json file : ",e)

        

# -------------------------------------------------------------------

def main() -> None:

    driver = setup_driver(URL)
    wait = get_wait(driver)
    scroll_to_bottom(driver)

    packages_data = fetch_packages(wait)
    save_to_json(packages_data)

    driver.quit()

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()
    