"""
    It Scrapes techforce's Industires page
    and saved it to json file .

    links_elements = driver.find_elements(By.XPATH, "//div[@aria-labelledby='homeMegaMenu_technologies']//a")

    in XPATH -> / -> must be direct child
                // -> anywhere inside

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


def fetch_industries_links(driver, wait):

    industries_btn = driver.find_element(By.CSS_SELECTOR, "a[title='Industries']")
    industries_btn.click()
    links = []
    time.sleep(5)
    links_elements = driver.find_elements(By.CSS_SELECTOR, ".row.sub-menu-all-icn.social_icn_main a")

    print("There are ",len(links_elements), "Industires we Serve.")

    links = [element.get_attribute("href") for element in links_elements]
    return links


def fetch_each_industry_page(link):

    try:
        print("-"*50)
        driver = setup_driver(link)
        wait = get_wait(driver)
        time.sleep(5)

        main_title = driver.find_element(By.CSS_SELECTOR, ".banner-index-main-content .banner-index-text h1").text

        main_info = driver.find_element(By.CSS_SELECTOR, "p span.TextRun.BCX0 span.NormalTextRun.BCX0").text


        # Our experties
        experties = []
        experties_card_elements = driver.find_elements(By.CSS_SELECTOR, "div.col-md-6 div.p-3")
        for element in experties_card_elements:
            exprty_title = element.find_element(By.CSS_SELECTOR, "b").text
            exprty_info = element.find_element(By.CSS_SELECTOR, ".NormalTextRun.BCX0").text
            experties.append(f" {exprty_title} : {exprty_info} ")
        
        # Our solutions
        solutions = []
        solution_elements = driver.find_elements(By.CSS_SELECTOR, "div.tab-content#v-pills-tabContent > div[role='tabpanel']")

        for element in solution_elements:
            title = element.find_element(By.CSS_SELECTOR, "h4.indus-tab-title").get_attribute("textContent")
            info = element.find_element(By.CSS_SELECTOR, "div.card-body").get_attribute("textContent")

            solutions.append(f" {title} : {info.replace("\n","").strip()}")
        
        #domain experties
        domain_experties = []
        domain_elements = driver.find_elements(By.CSS_SELECTOR, ".accordion .accordion-item")

        for element in domain_elements:
            title = element.find_element(By.CSS_SELECTOR, "button.accordion-button").get_attribute("textContent")
            info = element.find_element(By.CSS_SELECTOR, "div.accordion-body p").get_attribute("textContent")

            domain_experties.append(f"{title.replace("\n", "").strip() } : {info}")
        
        # why choose us
        dev_services  = []

        dev_services_cards = driver.find_elements(By.CSS_SELECTOR, "div.mt-4.deveoper-services.boxes .p-3")
        for element in dev_services_cards:
            service_text = element.find_element(By.CSS_SELECTOR, "h4").text
            dev_services.append(service_text)
        
        #projects
        projects = []
        projects_cards = driver.find_elements(By.CSS_SELECTOR, "div.portfolio-txt")

        for project in projects_cards:
            title = project.find_element(By.CSS_SELECTOR , "h3").text
            info = project.find_elements(By.CSS_SELECTOR , "p")[1].text
            link = project.find_element(By.CSS_SELECTOR , "a").get_attribute('href')

            projects.append({
                "title":title,
                "info":info,
                "link" :link
            })

        data = {
            "Title": main_title,
            "Info": main_info,
            "Experties": experties,
            "Solutions": solutions,
            "Domain Experties": domain_experties,
            "Dev Services": dev_services,
            "Projects": projects
        }
        print(f"{main_title} Scrapped succesfully")
        print("-"*50)

        driver.quit()
        return data

    except Exception as e:
        print("Failed To scrap data : ",e)

def save_to_json(data: list):
    """save list into a json file."""
    # write python list to json file
    try:
        with open("Extracted_data/Our_industries.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print("Data Saved to Our_industries.json Succesfully")
    except Exception as e:
        print("Failed To Save into json file : ",e)

        
# -------------------------------------------------------------------

def main() -> None:

    driver = setup_driver(URL)
    wait = get_wait(driver)
    scroll_to_bottom(driver)
    industries_data = []

    links = fetch_industries_links(driver, wait)
    # print(links)

    for link in links[:2]:
        industries_data.append(fetch_each_industry_page(link))

    save_to_json(industries_data)

    driver.quit()
    

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()
