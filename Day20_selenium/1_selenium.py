"""

It opens broweser and replacalte user's activity , used when broweser blocks request .
"""

from selenium import webdriver
from selenium.webdriver.common.by import By

# Start session
driver = webdriver.Chrome()

#take action on browser
driver.get("https://www.selenium.dev/selenium/web/web-form.html")

# request browser info
title = driver.title

driver.implicitly_wait(50)

# find element
text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")



# take action
text_box.send_keys("Selenium")
submit_button.click()

# request element info
message = driver.find_element(by=By.ID, value="message")
text = message.text
print(text)

driver.quit()
