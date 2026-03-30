"""
    It replicates user's action of clicking button
    with selenium .
"""

# -------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------------------------------------------------------

# Load chrome
driver = webdriver.Chrome()
driver.get("https://www.python.org/")
driver.implicitly_wait(5)

# scroll whole page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

print("Title : ",driver.title)

# It redirects to new page
about_btn = driver.find_element("css selector" , "a[href='/about/']").click()

# Explicitly wait
about_btn = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(("css selector", "a[href ='/about/']"))
)

h1_text = driver.find_element("class name", "call-to-action")
print("About python : ",h1_text.text)

driver.close()
