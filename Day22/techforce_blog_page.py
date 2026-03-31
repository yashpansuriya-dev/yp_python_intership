
"""
    It Scrapes techforce global website's blog page , 
    and

    - visit each blog's page and
    scrap blog's details such as blog info,
    topic name , author name, created date .
"""

# -------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import time


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
# Title and Blogs details
# -------------------------------------------------------------------

def fetch_title(driver):
    print("-"*50)
    return driver.title

def fetch_blogs(pages):
    blogs_data = []


    for i in range(1,pages+1):
        URL = f"https://techforceglobal.com/blog/?page={i}"
        driver = setup_driver(URL)
        wait = get_wait(driver)

        scroll_to_bottom(driver)

        blogs_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR , ".row .col-md-8 .col-md-12.box-shado"))
        )

        links = []

        for blog in blogs_elements:
            link = blog.find_element(By.CSS_SELECTOR, "b > a").get_attribute("href")
            links.append(link)
        

        for link in links:
            driver = setup_driver(link)
            wait = get_wait(driver)

            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".row.details-page.single-blog-content")
            ))
    

            blog_element = driver.find_element(By.CSS_SELECTOR, ".row.details-page.single-blog-content .col-md-8")

            blog_name = blog_element.find_element(By.CSS_SELECTOR, "h2").text
            blog_desc_p_elements =  blog_element.find_elements(By.TAG_NAME, "p")
            blog_desc = []

            for p in blog_desc_p_elements:
                text = p.text.strip()
                if text:
                    blog_desc.append(text)
            blog_author = blog_element.find_element(By.CSS_SELECTOR, "p.mt-3 b").text
            blog_date = blog_element.find_element(By.CSS_SELECTOR, "p.mt-3 font").text


            blogs_data.append({
                "title": blog_name,
                "info": blog_desc,
                "author": blog_author,
                "date": blog_date
            })

            driver.quit()


    return blogs_data



def main() -> None:
    print("hello")

    blogs_data = fetch_blogs(1)
    for blog in blogs_data:
        print(f" blog name : {blog['title']} , blog_author : {blog['author']}")

if __name__ == "__main__":
    main()




        

