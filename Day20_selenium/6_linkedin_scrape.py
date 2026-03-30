"""
    It Scrapes Linkedin Webisite and extract Job role,
    company and location as role searched in query and
    extract it into CSV file.
"""

# -------------------------------------------------------------------

import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------------------------------------------------------

def save_jobs_to_csv(num_of_jobs=10, query="Java Developer"):
    try:
        driver = webdriver.Chrome()
        driver.get(f"https://www.linkedin.com/jobs/search/?keywords={query}")

        wait = WebDriverWait(driver, 10)

        data = {
            'Role': [],
            'Company': [],
            'Location': [],
            'Posted Time': []
        }

        last_count = 0
        time.sleep(2)

        # cls_btn = wait.until(
        #         EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Dismiss']"))
        #     )
        cls_btn = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Dismiss']")
        driver.execute_script("arguments[0].click()", cls_btn)
        # print(cls_btn)

        # cls_btn.click()

        while len(data['Role']) < num_of_jobs:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # click "see more jobs" if exists
            try:
                button = driver.find_element(By.CSS_SELECTOR, "button.infinite-scroller__show-more-button")
                button.click()
            except:
                pass

            jobs = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".base-search-card__info"))
            )

            if len(jobs) == last_count:
                break

            last_count = len(jobs)

            for job in jobs[len(data['Role']):]:
                role = job.find_element(By.TAG_NAME, "h3").text
                company = job.find_element(By.CSS_SELECTOR, "h4 > a").text
                location = job.find_element(By.CSS_SELECTOR, "div > span").text
                timed = job.find_element(By.CSS_SELECTOR, "div > time").text

                data['Role'].append(role)
                data['Company'].append(company)
                data['Location'].append(location)
                data['Posted Time'].append(timed)

                if len(data['Role']) >= num_of_jobs:
                    break

        df = pd.DataFrame(data)
        df.to_csv("linkedin_jobs_data.csv", index=False)

        print(f"Saved {len(df)} Jobs Successfully")

        driver.quit()

    except Exception as e:
        print("Error Occurred:", e)

# -------------------------------------------------------------------

def main():
    role = input("Which Role do you want to search for : ")
    num_of_jobs = int(input("How Many no. of jobs do you want : "))
    save_jobs_to_csv(num_of_jobs, role)

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()