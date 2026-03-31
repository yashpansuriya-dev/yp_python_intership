"""
    It Scrapes techforce global website , and

    -list all technologies we've worked with
    -our portfolio , all project done so far
    - list apify actors
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

URL = "https://techforceglobal.com/"

# -------------------------------------------------------------------
# Setup
# -------------------------------------------------------------------

def setup_driver():
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
# Title and About us
# -------------------------------------------------------------------

def fetch_title(driver):
    print("-"*50)
    return driver.title


def fetch_about_us(wait) -> str:
    print("-"*50)
    print("Fetching About us....")
    try:
        about_us_text = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".Hero-text + *"))
        )
        return about_us_text.text
    except TimeoutException as e:
        print("About us section not found",e)
        return ""


# -------------------------------------------------------------------
# Print All Our Technolgies
# -------------------------------------------------------------------

def fetch_tech_name(src) -> str:
    tech_name = src.split("/")[-1].split(".")[0]
    if "-" in tech_name:
        if "New" in tech_name:
            return tech_name.split("-")[0]
        else:
            return tech_name.split("-")[1]
    else:   
        return tech_name


def fetch_technologies(wait) -> dict:
    print("-"*50)
    print("Fetching Technologies....")
    tech_data = {}
    try:

        all_tech_topics = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR , ".homepage-tech-logos-tabs-content > .tab-pane "))
        )

        for topic in all_tech_topics:
            topic_name = topic.get_attribute("id")
            tech_data[topic_name] = []
            techs = topic.find_elements(By.CSS_SELECTOR, "ul li img")
            for tech in techs :
                src = tech.get_attribute("data-src")
                tech_data[topic_name].append(fetch_tech_name(src))

    except (TimeoutException, NoSuchElementException) as e:
        print("fetching technogies section failed",e)
    
    return tech_data


# -------------------------------------------------------------------
# What we do
# -------------------------------------------------------------------

def fetch_what_we_do(wait) -> dict:
    print("-"*50)
    print("Fetching 'What We Do' section...")

    what_we_do_data = {"title": "", "info": "", "points": []}
    try:
        section = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".section-title"))
        )

        section_title = section.find_element(By.CSS_SELECTOR, "h1")
        section_info = section.find_element(By.CSS_SELECTOR, "p")
        section_points = section.find_elements(By.CSS_SELECTOR, "ul li")

        what_we_do_data["title"] = section_title.text
        what_we_do_data["info"] = section_info.text

        for point in section_points:
            what_we_do_data["points"].append(point.text)
    except (TimeoutException, NoSuchElementException) as e:
        print("What we do section failed", e)
    
    return what_we_do_data


def fetch_trusted_partners(wait):
    our_partners_data = {"name":"", "partners":[] }

    partner_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".awards-section"))
    )

    title = partner_element.find_element(By.CSS_SELECTOR, "div div h6").text
    partners = partner_element.find_elements(By.CSS_SELECTOR, ".marquee-content img")

    our_partners_data["name"] = title
    for src in partners:
        partner_name = src.get_attribute('data-src').split("/")[-1].split(".")[0]
        our_partners_data["partners"].append(partner_name)
    
    return our_partners_data

def fetch_service_we_provides(wait):
    services_data = []

    services_elements = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".service-card-main"))
    )

    for service in services_elements:
        name = service.find_element(By.CSS_SELECTOR, "h3").get_attribute('textContent')
        desc_elements = service.find_elements(By.CSS_SELECTOR, "p")

        desc = ""
        for p in desc_elements:
            if p.get_attribute('textContent').strip() != "":
                desc = p.get_attribute('textContent')
                break

        services_data.append({"name":name, "desc":desc})
    
    return services_data


def our_dev_approch(wait):
    approch_steps_data = []
    title = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h1.light-bg-title"))
    ).text
    print("Title : ")

    approch_steps_card = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".small-devices .container .row .column"))
    )

    for approch_step in approch_steps_card:
        step_name = approch_step.find_element((By.CSS_SELECTOR, "h3"))
        step_desc = approch_step.find_element((By.CSS_SELECTOR, "p"))

        approch_steps_data.append({"name" : step_name, "desc" : step_desc})
    
    return approch_steps_data

def fetch_what_client_says(wait):
    clients_messages_data = []
    clients_cards = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".testimonialAllContent"))
    )

    for client in clients_cards:
        client_name = client.find_element(By.CSS_SELECTOR, "p").get_attribute('textContent')
        client_message = client.find_element(By.CSS_SELECTOR, "div h1").get_attribute('textContent').replace("\n","").strip()

        clients_messages_data.append({"client_name":client_name, "client_message":client_message})
    
    return clients_messages_data

def fetch_final_message(wait):
    final_messsage = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".widegt_about p"))
    )

    return final_messsage.get_attribute("textContent")

def fetch_our_offices(wait):
    all_office_address = []
    office_cards = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".col-md-12.single_info"))
    )
    office_cards = office_cards[1:]


    for office in office_cards:
        country_src = office.find_element(By.CSS_SELECTOR, ".icon-flag img")
        country_name = country_src.get_attribute('data-src').split("/")[-1].split(".")[0]

        address = office.find_element(By.CSS_SELECTOR, ".info").text.replace("\n", " ")

        all_office_address.append({"country" : country_name, "address":address})
    
    return all_office_address


# -------------------------------------------------------------------

def main() -> None:
    driver = setup_driver()
    wait = get_wait(driver)

    scroll_to_bottom(driver)

    # print("Title : ", fetch_title(driver))
    # print("About us : ", fetch_about_us(wait))
    # print("What We do ", fetch_what_we_do(wait))

    # print("Our Trusted Partners : ", fetch_trusted_partners(wait))
    # print("Techs We work with  : ", fetch_technologies(wait))

    # print("Services We provides : ", fetch_service_we_provides(wait))

    # print("What Our client says : ", fetch_what_client_says(wait))

    # print("Final Message : ", fetch_final_message(wait))

    # print("OFFICE addresses : ", fetch_our_offices(wait))

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()