import requests
from bs4 import BeautifulSoup

url = "https://www.w3schools.com/js/js_htmldom_methods.asp"


response = requests.get(url)


with open("w3page.txt", "w") as f:
    f.write(response.text)

soup = BeautifulSoup(response.text, 'html.parser')

with open("preetyw3page.txt", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print("done")

