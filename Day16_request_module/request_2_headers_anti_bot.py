'''
    headers are essential information abot communication b/w client and
    server .
    (metadata sent in request and response.)

    headers = {
        Content-Type : application/json     -> which type of content you're sending
        Accept : application/json          -> what response format expects
        User-Agent : "python-request/2.x" -> who is requesting,(python-script,chrome,edge)(client)
        Authorization : Bearer TOKEN        -> authorization token (JWT, API tokens)
    }

    Basic Anti Bot awareness techniques :
        -User Agent : python script(usually bot) , mozila , chrome , edge
        -too many request : block if one IP send too many request at a time
        -Authorization header token : ex. JWT Token
        -Custom specific header : checks specific key-value provided
        -API Key
       - CAPTCHA
'''

# -------------------------------------------------------------------

import requests

# -------------------------------------------------------------------

def is_bot(response):
    """
        Returns True if request suspects as bot.

        It checks that the user making request is a python script or not ,
        it it is python script then it consider it as bot.
    """
    if 'python-requests' in response.request.headers.get("User-Agent"):
        return True
    else:
        return False

# -------------------------------------------------------------------

def main() -> None:
    """ Main Function ."""

    metadata = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0",
        "Accept" : "application/josn"
    }

    # --------------------------------------------
    # User Agent
    # --------------------------------------------

    # Default User agent
    response = requests.get("https://httpbin.org/user-agent")
    if(not is_bot(response)):
        data = response.json()
        print("\nIt is not bot and  User agent : ",data)
    else:
        print("this is bot")
        
    
    # Custom User agent 
    response  = requests.get("https://httpbin.org/user-agent", headers=metadata)
    if(not is_bot(response)):
        data = response.json()
        print("\nIt is not bot and  User agent : ",data)
    else:
        print("this is bot")


    # ---------------------------------------------------
    # User Agent( Default and Custom) and their comparison
    # ---------------------------------------------------

    # Default User agent
    response = requests.get("https://httpbin.org/user-agent")
    data = response.json()
    print("\Default User agent : ",data)        

    # Custom User agent 
    response  = requests.get("https://httpbin.org/user-agent", headers=metadata)
    data = response.json()
    print("\Custom User agent : ",data)


    # -------------------------------------------------
    # Headers (Default and Custom) and their comparison
    # -------------------------------------------------
    new_metadata = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0",
        "X-Custom-Header" : "yash-app",
        "Accept" : "application/json"
    }

    # Without Headers
    response = requests.get("https://httpbin.org/headers")
    data = response.json()
    print("\n\nDefault headers : ",data)

    # Custom Headers
    response = requests.get("https://httpbin.org/headers", headers=new_metadata)
    data = response.json()
    print("\n\nCustom Headers : ",data)

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()

    

