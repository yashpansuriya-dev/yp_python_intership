from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------------------------------------------------------

from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless=new")  # latest headless mode

driver = webdriver.Chrome(options=options)

# driver.get("https://example.com")
# print(driver.title)
# driver = webdriver.Chrome()

driver.get("https://www.python.org/")

driver.implicitly_wait(5)

# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

about_btn = driver.find_element("css selector" , "a[href='/about/']").click()

# about_btn = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.CLASS_NAME, "call-to-action"))
# )

about_btn = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(("css selector", "a[href ='/about/']"))
)

h1_text = driver.find_element("class name", "call-to-action")
print(h1_text.text)

driver.close()
