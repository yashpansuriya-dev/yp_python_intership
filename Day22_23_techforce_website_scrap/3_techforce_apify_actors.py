"""
    It Scrapes techforce global website's apify page , and

    - list all apify actors name
    - list all apify actors details such as
    name, description, features through visiting
    each page .
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

URL = "https://techforceglobal.com/apify-actors/"

# -------------------------------------------------------------------
# Setup
# -------------------------------------------------------------------

def setup_driver(URL):
    print(f"Fetching {URL}")
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
# Title and apify acotrs details
# -------------------------------------------------------------------

def fetch_title(driver):
    print("-"*50)
    return driver.title

def fetch_apify_actors_name(driver):
    apify_actors_name = []
    time.sleep(2)

    actors = driver.find_elements(By.CSS_SELECTOR, ".portfolio-grid .portfolio-gridbox")

    print(f"We have total {len(actors)} apify actors . ")
    for actor in actors:
        name = actor.find_element(By.CSS_SELECTOR, "div a h3").get_attribute("textContent").strip()
        apify_actors_name.append(name)
    
    return apify_actors_name


def fetch_apify_actors_data(driver):
    apify_actors_data = []
    apify_actors_link = []
    time.sleep(2)

    actors = driver.find_elements(By.CSS_SELECTOR, ".portfolio-grid .portfolio-gridbox")

    for actor in actors:
        name = actor.find_element(By.CSS_SELECTOR, "div a").get_attribute("href").strip()
        apify_actors_link.append(name)
    

    for link in apify_actors_link:
        print("-"*50)
        try:
            driver = setup_driver(link)
            wait = get_wait(driver)

            actor_detail = fetch_apify_actor_details(driver, wait)
            apify_actors_data.append(actor_detail)
            print("-"*50)
            driver.quit()
        except Exception as e:
            print(f"Error occured while scrapping {link}",e)

    print("Scrapped All Actors Succesfully")
    return apify_actors_data

    

def fetch_apify_actor_details(driver, wait):

    apify_actor_detail = {
        "name" : "",
        "short_info":"",
        "about" : [],
        "features" : []
    }

    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".apify-actor-main"))
    )

    # ---------------------------Fetch title----------------------------------
    title = driver.find_element(By.CSS_SELECTOR, ".portfolioinner-banntxt h1").text

    #--------------------------Fetch Description of actor ---------------------
    about_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".col-md-6.portfolioin-abttxt"))
    )

    about_title = about_element.find_element(By.CSS_SELECTOR, "h2").text

    about_info_elements = about_element.find_elements(By.CSS_SELECTOR, "p")
    about_info = [element.text for element in about_info_elements]

    # --------------------------- Fetch Features ----------------------------------
    features_elements = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".portfolio-corevalues-text"))
    )

    for feature in features_elements:
        feature_name = feature.find_element(By.CSS_SELECTOR, ".box-content h3").text
        feature_info = feature.find_elements(By.CSS_SELECTOR, ".box-content p")[1].text

        apify_actor_detail["features"].append(f" {feature_name} : {feature_info}")

    apify_actor_detail["name"] = title
    apify_actor_detail["short_info"] = about_title        
    apify_actor_detail["about"] = about_info

    print(f"Scrapped {title} Succesfully")
    return apify_actor_detail

def save_to_json(data: list):
    """save list into a json file."""
    # write python list to json file
    try:
        with open("Extracted_data/Our_apify_actors.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print("Data Saved to Our_apify_actors.json Succesfully")
    except Exception as e:
        print("Failed To Save into json file : ",e)

    
# -------------------------------------------------------------------

# -------------------------------------------------------------------

def main() -> None:
    driver = setup_driver(URL)
    # wait = get_wait(driver)

    scroll_to_bottom(driver)

    print("Title : ", fetch_title(driver))
    print("Apify Actors : ", fetch_apify_actors_name(driver))


    apify_actors_all_detail = fetch_apify_actors_data(driver)
    save_to_json(apify_actors_all_detail)

    driver.quit()


# -------------------------------------------------------------------

if __name__ == "__main__":
    main()