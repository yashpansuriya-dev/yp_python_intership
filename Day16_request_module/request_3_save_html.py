'''
    Here, It Saves HTML code of a website and saves it in provided 
    path .
'''

import requests

# -------------------------------------------------------------------

def save_html_page(filename: str, url: str) -> None:
    """
        It save website's html code in a file.

        Args:
            filename (str) : name of file where to save code
            url (str) : URL of website .

    """
    try:
        response = requests.get(url)
        with open(filename, "w") as f:
            f.write(response.text)
    except FileNotFoundError as e:
        print("Error : ",e)
    except Exception as e:
        print("Error : ",e)
    else:
        print("Saved Successfully...")


# -------------------------------------------------------------------

def main() -> None:
    """ Main Function ."""

    url = "https://www.geeksforgeeks.org/python/python-programming-language-tutorial/?_gl=1*179eg4z*_up*MQ..*_gs*MQ..&gclid=Cj0KCQjwpv7NBhCzARIsADkIfWxqRTEoPTXHFpL0eN3YBERG-dKLAQiMKtvSRk4vWBMVd05UvkaEPIwaAp3MEALw_wcB&gbraid=0AAAAAC9yBkDhO38f8OPfCBmCwL2rynRMR"
    save_html_page("pages/page1.html", url)

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()

# -------------------------------------------------------------------









