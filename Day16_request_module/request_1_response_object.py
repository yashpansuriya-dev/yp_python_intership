'''
requests is a Python library used to send HTTP requests to servers.

used to communicate through APIs.


A response is box like object ,w it returned by requests.get , post ,
it consists  data with headers, content type
    response.content -> a raw type text in bytes
    response.text -> string like text
    response.status_code -> 200,404,401...
    response.headers -> headers defining content-type, 
                        access-control-allow-methods,
                        access-control,..
'''

# -------------------------------------------------------------------

import requests
import os
from dotenv import load_dotenv

# -------------------------------------------------------------------

# load .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

params = {
    'q':'Mumbai',
    'appid': API_KEY,
    'units':'metric'
}

URL = f"https://api.openweathermap.org/data/2.5/weather?q=Mumbai&appid={API_KEY}&units=metric"

URL2 = "https://api.openweathermap.org/data/2.5/weather"


# -------------------------------------------------------------------

def main() -> None:
    """ Main Function ."""

    response = requests.get(URL2 ,params=params )
    print(requests.get(URL).headers)
    print("\nresponse object : ",response)
    print("\ncontent : ", response.content)
    print("\nheaders : ", response.headers)
    print("\nstatus_code :", response.status_code)
    print("\nText : ", response.text)
    print("\nurl : ", response.url)
    print("\nencoding : ",response.encoding)
    print("\ncookies : ",response.cookies)
    print("\nresponse ok :", response.ok)
    
    data = response.json()
    print("\njson : ",data)

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()

