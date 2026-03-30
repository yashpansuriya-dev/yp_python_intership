import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------------------------------------------------------

def save_jobs_to_csv(num_of_jobs, query):
    try:
        driver = webdriver.Chrome()
        data = {
                'Role': [],
                'Company': [],
                'Location': [],
                'Posted Time': []
            }

        query = query.replace(" ", "-")
        driver.get(f"https://in.linkedin.com/jobs/{query}-jobs?position=1&pageNum=0")
        driver.implicitly_wait(2)


        wait = WebDriverWait(driver, 10)

        while len(data['Role']) < num_of_jobs:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            jobs = wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li div div.base-search-card__info"))
                )

            for job in jobs:
                role = job.find_element("tag name", "h3").text
                company = job.find_element(By.CSS_SELECTOR, "h4 > a").text
                location = job.find_element(By.CSS_SELECTOR,"div > span").text
                timed = job.find_element(By.CSS_SELECTOR, "div > time").text
            
                data['Role'].append(role)
                data['Company'].append(company)                
                data['Location'].append(location)
                data['Posted Time'].append(timed)

                if len(data['Role']) >= num_of_jobs:
                    break


        df = pd.DataFrame(data)
        print(f"Saved {len(df)} Jobs Succesfully")
        df.to_csv("linkedin_jobs_data.csv", index=False)

        driver.quit()
    except Exception as e:
        print("Error Occured : ",e)

# -------------------------------------------------------------------

def main() -> None:
    save_jobs_to_csv(10, "Java Developer")

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()
