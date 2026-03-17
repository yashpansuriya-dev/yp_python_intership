"""
simple example showing how to store and read contacts using json.
"""

# -------------------------------------------------------------------

import json

# -------------------------------------------------------------------

def save_contacts(contacts: list) -> None:
    """save contacts list into a json file."""
    # write python list to json file
    with open("Files/contacts.json", "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)


def read_contacts() -> list:
    """read contacts from json file."""
    # read json file and convert it to python object
    with open("Files/contacts.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    return data

# -------------------------------------------------------------------

def main() -> None:
    """Main function ."""
    print("hello")

    contacts = []

    contacts.append({"name": "yash", "number": "9856414523"})
    contacts.append({"name": "vinay", "number": "9856414432"})
    contacts.append({"name": "rahul", "number": "9854355223"})
    contacts.append({"name": "brijraj", "number": "7854125441"})
    contacts.append({"name": "hiren", "number": "9856414523"})

    # save contacts to file
    save_contacts(contacts)

    # read contacts back from file
    data = read_contacts()

    print(data)
    print(type(data))

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()