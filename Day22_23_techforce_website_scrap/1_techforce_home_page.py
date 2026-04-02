"""
    It Scrapes techforce global website , and

    -list all technologies we've worked with
    -our portfolio , all project done so far
    - list apify actors
    -fill a contact us form

"""

# -------------------------------------------------------------------

import json

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
# Title and About us
# -------------------------------------------------------------------

def fetch_title(driver):
    print("-"*50)
    print("Fetching Title....")
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
    print("-"*50)
    print("Fetching Our Reviews....")
    try:
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
    except Exception as e:
        print("Error occured while fetching partners reviews",e)

def fetch_service_we_provides(wait):
    print("-"*50)
    print("Fetching Services....")
    try:
        services_data = []

        services_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".service-card-main"))
        )

        for service in services_elements[0:7]:
            name = service.find_element(By.CSS_SELECTOR, "h3").get_attribute('textContent')
            desc_elements = service.find_elements(By.CSS_SELECTOR, "p")

            desc = ""
            for p in desc_elements:
                if p.get_attribute('textContent').strip() != "":
                    desc = p.get_attribute('textContent')
                    break

            services_data.append({"name":name, "desc":desc})
        
        return services_data
    except Exception as e:
        print("Error occured while teching services", e)


def our_dev_approch(wait):
    print("-"*50)
    print("Fetching Our development approch....")
    try:
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
    except Exception as e:
        print("Error occured while fetching development approch")

def fetch_what_client_says(wait):
    print("-"*50)
    print("Fetching Client Reviews....")
    try:
        clients_messages_data = []
        clients_cards = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".testimonialAllContent"))
        )

        for client in clients_cards:
            client_name = client.find_element(By.CSS_SELECTOR, "p").get_attribute('textContent')
            client_message = client.find_element(By.CSS_SELECTOR, "div h1").get_attribute('textContent').replace("\n","").strip()

            clients_messages_data.append({"client_name":client_name, "client_message":client_message})
        
        return clients_messages_data
    except Exception as e:
        print("Error occured while fetching client reviews",e)

def fetch_final_message(wait):
    print("-"*50)
    print("Fetching Final message....")
    try:
        final_messsage = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".widegt_about p"))
        )

        return final_messsage.get_attribute("textContent")
    except Exception as e:
        print("Failed to fetch final message",e)

def fetch_our_offices(wait):
    print("-"*50)
    print("Fetching Office Addresses....")
    try:
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
    except Exception as e:
        print("Error occured while fetching office addresses",e)

def filing_contact_us_form(driver):
    print("-"*50)
    print("Filing Contact us Form....")
    try:
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
        print("Form filled Succesfully")
        print("-"*50)
    except Exception as e:
        print("Error occured while filing form ",e)


def save_to_json(data: list):
    """save list into a json file."""
    # write python list to json file
    try:
        with open("Extracted_data/Our_home_page.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print("Data Saved to Our_home_page.json Succesfully")
    except Exception as e:
        print("Failed To Save into json file : ",e)



# -------------------------------------------------------------------

def main() -> None:
    driver = setup_driver(URL)
    wait = get_wait(driver)

    scroll_to_bottom(driver)

    # Fetch data
    title = fetch_title(driver)
    about_us = fetch_about_us(wait)
    what_we_do = fetch_what_we_do(wait)
    trusted_partners = fetch_trusted_partners(wait)
    technologies = fetch_technologies(wait)
    services = fetch_service_we_provides(wait)
    client_reviews = fetch_what_client_says(wait)
    final_message = fetch_final_message(wait)
    offices = fetch_our_offices(wait)

    # store in dict
    home_page_data = {
        "title": title,
        "about_us": about_us,
        "what_we_do": what_we_do,
        "trusted_partners": trusted_partners,
        "technologies": technologies,
        "services": services,
        "client_reviews": client_reviews,
        "final_message": final_message,
        "offices": offices,
    }

    save_to_json(home_page_data)

    # filing_contact_us_form(driver)

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()