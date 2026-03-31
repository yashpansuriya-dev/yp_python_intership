"""
    It Scrapes techforce global website , and

    -list all technologies we've worked with
    -our portfolio , all project done so far
    -list apify actors
    -fill a contact us form
"""

# -------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import time

# -------------------------------------------------------------------

driver = webdriver.Chrome()
driver.get("https://techforceglobal.com/")
driver.implicitly_wait(5)

wait = WebDriverWait(driver, 10)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

print("Title : ", driver.title)

about_us_text = driver.find_element(By.CSS_SELECTOR, ".Hero-text + *")
print(about_us_text.text)



# -------------------------------------------------------------------
# Print All Our Technolgies
# -------------------------------------------------------------------

all_tech_topics = driver.find_elements(By.CSS_SELECTOR , ".homepage-tech-logos-tabs-content > .tab-pane ")

for topic in all_tech_topics:
    print()
    print(topic.get_attribute("id"), ": ")
    techs = topic.find_elements(By.CSS_SELECTOR, "ul li img")
    for tech in techs :
        tech_name = tech.get_attribute("data-src")
        tech_name = tech_name.split("/")[-1].split(".")[0]
        if "-" in tech_name:
            print(tech_name.split("-")[1])
        else:
            print(tech_name)
# -------------------------------------------------------------------




# # -------------------------------------------------------------------
# # Our portfolio - List All Projects
# # -------------------------------------------------------------------
# company_btn = driver.find_element(By.CSS_SELECTOR, "a[title='Company']")
# company_btn.click()


# portfolio_btn = driver.find_element(By.CSS_SELECTOR, "a[title='Our Portfolio']")
# portfolio_btn.click()

# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# time.sleep(5)


# heading= driver.find_element(By.CSS_SELECTOR, ".section-title")
# print("\n\n",heading.text)

# # click load more 5times
# for _ in range(5):
#     load_more_btn = wait.until(
#         EC.element_to_be_clickable((By.CSS_SELECTOR, "#pf-load-more"))
#     )
    
#     driver.execute_script("arguments[0].click();", load_more_btn)
#     # load_more_btn.click()
#     time.sleep(2)

# projects = driver.find_elements(By.CSS_SELECTOR, "div.pf-cards-grid  div.pf-card-wrapper")

# print("Total projects:", len(projects))
# print("\n\n")

# for project in projects:
#     try:
#         title = project.find_element(By.CSS_SELECTOR, ".pf-card-overlay-title").get_attribute("textContent").strip()
#         desc = project.find_element(By.CSS_SELECTOR, ".pf-card-overlay-desc").get_attribute("textContent").strip()
        
#         print("Title:", title)
#         print("Desc:", desc)
#         print("-" * 50)
        
#     except Exception as e:
#         print("Error:", e)
# # -------------------------------------------------------------------




# # -------------------------------------------------------------------
# # List Our Apify Actors
# # -------------------------------------------------------------------

# apify_btn = driver.find_element(By.CSS_SELECTOR, "a[title='Apify Actors']")
# apify_btn.click()

# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# time.sleep(5)

# actors = driver.find_elements(By.CSS_SELECTOR, ".portfolio-grid .portfolio-gridbox")

# print("\nApify Actors : ")
# print(f"We have total {len(actors)} apify actors . ")
# for actor in actors:
#     name = actor.find_element(By.CSS_SELECTOR, "div a h3").get_attribute("textContent").strip()
#     print(name)
#     print("-"*50)
# # -------------------------------------------------------------------




# -------------------------------------------------------------------
# Filing a contact us form
# -------------------------------------------------------------------

company_btn = driver.find_element(By.CSS_SELECTOR, "a[title='Company']")
company_btn.click()

portfolio_btn = driver.find_element(By.CSS_SELECTOR, "a[title='Contact Us']")
portfolio_btn.click()

f_name = driver.find_element(By.CSS_SELECTOR, "#First_Name").send_keys("mihir")
l_name = driver.find_element(By.CSS_SELECTOR, "#Last_Name").send_keys("patel")
email = driver.find_element(By.CSS_SELECTOR, "#Email").send_keys("randommail@gmail.com")
phone = driver.find_element(By.CSS_SELECTOR, "#Phone").send_keys("9856741112")
budget = Select(driver.find_element(By.CSS_SELECTOR, "#LEADCF10")).select_by_value("Between 10K to 50K")
category = Select(driver.find_element(By.CSS_SELECTOR, "#LEADCF9")).select_by_value("Fintech Solution")
description = driver.find_element(By.CSS_SELECTOR, "#Description").send_keys("random text")

submit_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")

driver.execute_script("arguments[0].click()", submit_btn)

# -------------------------------------------------------------------

time.sleep(5)
driver.quit()
