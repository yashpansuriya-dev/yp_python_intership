"""
    It Scrapped a website which has countries data , 
    through selenium .and stores data in csv  file
    and applies filter like, 
    
        country with highest population
        country with less than 1 milion population .
"""

# -------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import pandas as pd

# -------------------------------------------------------------------

def save_to_csv(filename):
    driver = webdriver.Chrome()
    driver.get("https://www.scrapethissite.com/pages/simple/")
    driver.implicitly_wait(5)

    wait = WebDriverWait(driver, 10)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    data = {
        'Country': [],
        'Capital':[],
        'Population' : [],
        'Area' : []
    }

    # print all countries name
    countries = driver.find_elements(By.CSS_SELECTOR, ".country")

    for country in countries:
        name = country.find_element(By.CSS_SELECTOR, "h3").text
        capital = country.find_element(By.CLASS_NAME, "country-capital").text
        population = country.find_element(By.CLASS_NAME, "country-population").text
        area = country.find_element(By.CLASS_NAME, "country-area").text
        # print(name)

        data['Country'].append(name)
        data['Capital'].append(capital)
        data['Population'].append(int(population))
        data['Area'].append(float(area))

    df = pd.DataFrame(data)
    try:
        df.to_csv(filename, index=False)
        print("Saved Succesfully")
    except Exception as e:
        print("Error Occured : ",e)

# -------------------------------------------------------------------

def main() -> None:
    save_to_csv("countries_data.csv")

    df = pd.read_csv("countries_data.csv")

    # Find Highest Populated Country .
    highest_populated_country = df.sort_values(by="Population", ascending=False).iloc[0]
    print(f"Country WIth Highest Population is : {highest_populated_country['Country']} with {highest_populated_country['Population']} Population .")

    # Country with population under 1 milion
    low_populate_countries = df[df['Population'] < 1000000]
    print(f"\n\nThere are {len(low_populate_countries)} Countries with population under 1 milion")
    print(low_populate_countries.head())

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()


