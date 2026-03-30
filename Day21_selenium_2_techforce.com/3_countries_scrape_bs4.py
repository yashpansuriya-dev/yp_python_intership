"""
    It Scrapped a website which has countries data , 
    through BeautifulSoup , and stores data in csv  file .
"""

# -------------------------------------------------------------------

from bs4 import BeautifulSoup
import requests
import pandas as pd

# -------------------------------------------------------------------

r = requests.get("https://www.scrapethissite.com/pages/simple/")
soup = BeautifulSoup(r.text, 'html.parser')

data = {
        'Country': [],
        'Capital': [],
        'Population' : [],
        'Area' : []
    }
countries = soup.select(".country ")

for country in countries:
    name = country.select_one("h3").text
    capital = country.select_one(".country-capital").text
    population = country.select_one(".country-population").text
    area = country.select_one(".country-area").text
    
    data['Country'].append(name.strip())
    data['Capital'].append(capital.strip())
    data['Population'].append(int(population.strip()))
    data['Area'].append(float(area.strip()))

df = pd.DataFrame(data)
try:
    df.to_csv("countries_data_bs4.csv", index=False)
    print("Saved Succesfully")
except Exception as e:
    print("Error Occured : ",e)

# -------------------------------------------------------------------

