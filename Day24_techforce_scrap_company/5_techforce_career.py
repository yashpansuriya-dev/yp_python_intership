
"""
    It Scrapes techforce's Career page
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

URL = "https://techforceglobal.com/career/"

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
# Scrapes Title and Career Page
# -------------------------------------------------------------------

def scrape_title(driver):
    print("-"*50)
    return driver.title


def scrape_career(driver):
    try:
        print("-"*50)
        print(f"Scrapping Career Page...")
        time.sleep(5)

        # page title
        title = driver.find_element(By.CSS_SELECTOR, "section.tf-hero h1").text.replace("\n",", ").strip()

        # info
        info = driver.find_element(By.CSS_SELECTOR, "section.tf-hero p.tf-hero-desc").text.replace("\n",", ").strip()

        # available jobs
        available_jobs = []
        job_cards = driver.find_elements(By.CSS_SELECTOR, "section.tf-explore div.job-card")
        for job in job_cards:
            job_title = job.find_element(By.CSS_SELECTOR, "h3.job-title").text
            job_experience = job.find_element(By.CSS_SELECTOR, "div.experience-detail").text.replace("Experience:","")
            job_role = job.find_element(By.CSS_SELECTOR, "div.job-detail").text.replace("Position:","")

            job_skills_list = job.find_elements(By.CSS_SELECTOR, "div.skills-list span")
            required_skills = [tag.text for tag in job_skills_list]

            job_link = job.find_element(By.CSS_SELECTOR, "div.job-footer a").get_attribute("href")

            available_jobs.append({
                "Title": job_title,
                "Role": job_role,
                "Experience": job_experience,
                "Required Skills": required_skills,
                "Link to Apply":job_link
            })
        
        # Why join us
        benifits_cards = driver.find_elements(By.CSS_SELECTOR, "section.tf-perks div.tf-perk-card h4")
        our_perks_and_benifits = [card.text for card in benifits_cards]

        # hiring process
        hiring_process = []
        hiring_steps_cards = driver.find_elements(By.CSS_SELECTOR, "section.tf-hiring div.tf-hiring-step")
        for card in hiring_steps_cards:
            step_title = card.find_element(By.CSS_SELECTOR, "h4").text
            step_desc = card.find_element(By.CSS_SELECTOR, "p").text

            hiring_process.append({
                "Title" : step_title,
                "Description":step_desc
            })
        
        # we believe in
        our_motto_1 = driver.find_element(By.CSS_SELECTOR, "section.tf-culture h2").text
        our_motto_2 = driver.find_element(By.CSS_SELECTOR, "section.tf-culture p").text
        our_motto = f" {our_motto_1} : {our_motto_2}"

        careers = {
            "Title" : title,
            "Info" : info,
            "Available Jobs" : available_jobs , 
            "Why Joins Us" : our_perks_and_benifits,
            "Hiring Steps" : hiring_process,
            "We Believe in" :our_motto
        }
        print("Career Page Scrapped Succesfully")
        print("-"*50)
        return careers
    
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
    
    careers = scrape_career(driver)
    save_to_json("career_page.json", careers)

    driver.quit()
    

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()
