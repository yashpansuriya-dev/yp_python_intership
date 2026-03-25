"""
    find -> find first match only
    find_all -> find all matches

    soup.find("p")  # by tag
    soup.find("p", class_="price_color")  # by class
    soup.find("a", href=True)  # by attribute
"""

# -------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup

# -------------------------------------------------------------------

def main() -> None:
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
    }

    url = "https://www.w3schools.com/js/js_htmldom_methods.asp"
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    # Title
    print("Title : ")
    print("\n\n\nTitle:", soup.find("title").text)

    # Links
    print("\n\n\nLinks:")
    for link in soup.find_all("a"):
        print(link.get("href"))

    # Headings
    print("\n\n\n\nHeadings:")
    for i in range(1, 7):
        for h in soup.find_all(f"h{i}"):
            print(h.text)

# -------------------------------------------------------------------

if __name__ == '__main__':
    main()