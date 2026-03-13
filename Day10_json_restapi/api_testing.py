"""
requests library: GET and POST requests, headers, status codes, parsing JSON responses

Status codes :-
200 - Success
201 - Resource Created
204 - Success but no response

301 — Moved Permanently
302 — Found (Temporary Redirect)

400 — Bad Request
401 — Unauthorized
403 — Forbidden
404 - Not Found

500 - Internal server errror

Headers :- Metadata about request and response , that helps 
client to understand how to process message
key-value pair
ex.,  "content-type": "application/json" 
      "authorization": BEARER token 

"""
# -------------------------------------------------------------------

import requests

# -------------------------------------------------------------------

def get_objects(url : str) -> dict | list:
    """
        fetches all data from provided
        url , returns it.

        Args :
            url (str) : REST APIs url
    """
    try:
        response = requests.get(f"{url}")
        data = response.json()
    except Exception:
        print("Error Code : ", response.status_code)
    else:
        return data


def get_object(url :str , id : int | str) -> dict | None:
    """
        fetches  data from provided
        url , and with provided id .
        and returns it.

        Args :
            url (str) : REST APIs url
            id (str | int) : id of object
    """
    try:
        response = requests.get(f"{url}/{id}")
        data = response.json()
    except Exception:
        print("Error Code : ", response.status_code)
    else:
        return data


def add_object(url: str, data: dict, header: dict={}):
    """
        sends data to server with post
        request.

        Args :
            url (str) : url of API
            data (dict) : data to send
            header : headers if any
    """
    try:
        response = requests.post(url, json=data, headers=header)
        obj = response.json()
    except Exception:
        print("Error Code : ", response.status_code)
    else:
        print("Status Code : ",response.status_code)
        print("Headers : ",response.headers)
        return obj

# -------------------------------------------------------------------

def main() -> None:
    """ Main Function . """
    # GET - retrive information from server
    url = 'https://api.restful-api.dev/objects/'

    for i in range(1,6):
        print(f"Object {i} :- " ,get_object(url, i))
    
    print("\n")
    
    # POST - sends to data to server
    data = {
        "name": "Yash Laptop",
        "data": {
            "year": 2024,
            "price": 120000,
            "CPU model": "Intel i7",
            "Hard disk size": "1 TB"
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    print("\nNew Object Created :- ", add_object(url, data, headers))

# -------------------------------------------------------------------

if __name__ == '__main__':
    main()