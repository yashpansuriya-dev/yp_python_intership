import requests
from bs4 import BeautifulSoup

# -------------------------------------------------------------------


def main() -> None:
    """ Main Function ."""

    url = "https://www.w3schools.com/js/js_htmldom_methods.asp"
    response = requests.get(url)

    # Without BeautifulSoup HTML
    with open("pages/w3page.txt", "w") as f:
        f.write(response.text)

    # With BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    with open("pages/preetyw3page.txt", "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    print("Done")

# -------------------------------------------------------------------

if __name__ == '__main__':
    main()