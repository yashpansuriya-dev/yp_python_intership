"""
    It Scrapes techforce's services page
    and saved it to json file .

    links_elements = driver.find_elements(By.XPATH, "//div[@aria-labelledby='homeMegaMenu_technologies']//a")

    in XPATH -> / -> must be direct child
                // -> anywhere insdie

                tag[@attribute = 'value']
"""
# erorr handling , consled printing

import json

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import time

# -------------------------------------------------------------------

URL ="https://techforceglobal.com"

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
# Title and Services details
# -------------------------------------------------------------------

def fetch_title(driver):
    print("-"*50)
    return driver.title


def fetch_services_links(driver, wait):

    service_btn = driver.find_element(By.CSS_SELECTOR, "a[title='Technologies']")
    service_btn.click()
    links = []
    time.sleep(5)
    links_elements = driver.find_elements(By.XPATH, "//div[@aria-labelledby='homeMegaMenu_technologies']//a")
    print("There are ",len(links_elements), "Services We provide")

    links = [element.get_attribute("href") for element in links_elements]
    return links


def fetch_each_service_page(link):

    try:
        print("-"*50)
        # print(f"Scrapping {link}...")
        driver = setup_driver(link)
        wait = get_wait(driver)
        time.sleep(5)

        # title
        title = driver.find_element(By.CSS_SELECTOR, "h1").text

        # Info
        info  = driver.find_elements(By.CSS_SELECTOR, "span.TextRun.BCX0")[1].text

        # What Do we do
        what_we_do_elements = driver.find_elements(By.CSS_SELECTOR, "span.lists_descrip")
        what_we_do = [element.text for element in what_we_do_elements]
     

        # Projects
        projects = []
        projects_elements = driver.find_elements(By.CSS_SELECTOR, "div.portfolio-txt")
        
        for project_element in projects_elements:
            project_name = project_element.find_element(By.CSS_SELECTOR, "h3").text
            project_info = project_element.find_element(By.CSS_SELECTOR, "p").text
            project_url = project_element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

            projects.append({
                "project_name" :project_name,
                "project_info":project_info,
                "project_url":project_url
            })
        
        # FAQs
        FAQs = []
        faq_elements = driver.find_elements(By.CSS_SELECTOR, ".panel-group .panel")
        for faq_element in faq_elements:
            question  = faq_element.find_element(By.CSS_SELECTOR, ".panel-heading h4").text
            answer  = faq_element.find_element(By.CSS_SELECTOR, ".panel-collapse .panel-body p").get_attribute("textContent")

            FAQs.append({
                "Que":question,
                "Ans":answer.replace("\n","").strip()
            })

        print(f"{title} Scrapped Succesfully")
        print("-"*50)
        driver.quit()

        return {
            "service_name":title,
            "service_info":info,
            "what_we_do":what_we_do,
            "projects_on_it":projects,
            "faqs":FAQs
        }
    
    except Exception as e:
        print("Failed To scrap data : ",e)

def save_to_json(data: list):
    """save list into a json file."""
    # write python list to json file
    try:
        with open("Extracted_data/Our_services.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print("Data Saved to Our_services.json Succesfully")
    except Exception as e:
        print("Failed To Save into json file : ",e)

        
# -------------------------------------------------------------------

def main() -> None:

    driver = setup_driver(URL)
    wait = get_wait(driver)
    scroll_to_bottom(driver)
    services_data = []

    links = fetch_services_links(driver, wait)

    for link in links[:3]:
        services_data.append(fetch_each_service_page(link))
    
    save_to_json(services_data)

    driver.quit()
    
    

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()
    
