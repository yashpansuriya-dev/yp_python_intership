"""
    It Scrapes techforce's About us page
    and saved it to json file .

"""
# -------------------------------------------------------------------

import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------------------------------------------------------

URL ="https://techforceglobal.com/about-us"

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
# Scrapes Title and About us Page
# -------------------------------------------------------------------

def fetch_title(driver):
    print("-"*50)
    return driver.title


def scrape_about_us(driver):
    try:
        print("-"*50)
        print(f"Scrapping About US Page...")
        time.sleep(5)

        # our_motive
        our_motive = driver.find_element(By.CSS_SELECTOR, "h2.section-main-title").get_attribute("textContent")

        # company_info
        company_info_tags = driver.find_elements(By.CSS_SELECTOR, "section.hero-section div.container p")
        company_info = [tag.text for tag in company_info_tags]

        # what we do
        our_solutions = []
        solution_section = driver.find_element(By.CSS_SELECTOR, "section.solutions-section")
        solution_cards = solution_section.find_elements(By.CSS_SELECTOR, "div.solution-card-main>div.solution-card.p-4")

        for card in solution_cards:
            solution_title = card.find_element(By.CSS_SELECTOR, "h4.solution-title").text
            solution_info  = card.find_element(By.CSS_SELECTOR, "p").text

            our_solutions.append({
                "Title" : solution_title,
                "Description" : solution_info
            })
        
        # company certification
        certification_name = driver.find_element(By.CSS_SELECTOR, "section.iso-section h2.section-main-title").text
        certification_info = driver.find_element(By.CSS_SELECTOR, "section.iso-section p").text

        certification = {
            "Name" : certification_name,
            "Description" : certification_info
        }

        # Our approch - " > means direct child "
        approaches_cards = driver.find_elements(By.CSS_SELECTOR, "section.our-approach1 div.our-approach>.solution-card")
        approaches = [
            card.find_element(By.CSS_SELECTOR, "h4.solution-title").text 
            for card in approaches_cards
        ]

        # why choose techforce
        why_choose_cards = driver.find_elements(By.CSS_SELECTOR, "section.why-choose-section div.feature-card p")

        why_choose_us = [card.text for card in why_choose_cards]

        # our leaders
        our_leaders = []
        team_cards = driver.find_elements(By.CSS_SELECTOR, "section.our-leaders div.team-card-main div .info")
        for card in team_cards:
            leader_name = card.find_element(By.CSS_SELECTOR, "h4").text
            leader_role = card.find_element(By.CSS_SELECTOR, "span").text

            our_leaders.append({
                "Name":leader_name,
                "Their Role":leader_role
            })
        
        # life at techforce
        life_at_techforce = []
        life_cards = driver.find_elements(By.CSS_SELECTOR , ".life-at-techforce div.solution-card")
        for card in life_cards:
            name = card.find_element(By.CSS_SELECTOR, "h4").text
            info = card.find_element(By.CSS_SELECTOR, "p").text

            life_at_techforce.append({
                "Title": name,
                "Description": info,
            })
        
        # Storing Data to dict
        about_us = {
            "Our Motive": our_motive,
            "Company Info.": company_info,
            "Our Solutions": our_solutions,
            "Certification": certification,
            "Approaches": approaches,
            "Why Choose Us": why_choose_us,
            "Our Leaders": our_leaders,
            "Life at Techforce": life_at_techforce
        }

        print("About us Scrapped Succesfully")
        print("-"*50)

        return about_us
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
    
    about_techforce = scrape_about_us(driver)
    save_to_json("about_us_page.json", about_techforce)

    driver.quit()
    

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()
