"""

loads()  -> convert JSON string to Python object
dumps()  -> convert Python object to JSON string , indent = 4

load()   -> read JSON file and convert to Python object
dump()   -> write Python object to a file in JSON format , indent=4


"""

# -------------------------------------------------------------------

import json

# -------------------------------------------------------------------

# loads
def json_string_to_python() -> None:
    """convert a JSON string into a Python dictionary."""

    json_data = """
    {
        "name": "yash",
        "age": 20,
        "marks": [98, 90, 45],
        "education": {
            "degree": "IT Engineering",
            "year": 4
        }
    }
    """

    python_obj = json.loads(json_data)

    print("\nJSON string -> Python object")
    print(type(python_obj))
    print(type(python_obj["marks"]))
    print(python_obj)
    print()

# dumps
def python_to_json_string() -> None:
    """ convert a Python dictionary to
        a JSON string."""
    
    python_obj = {
        "name": "yash",
        "age": 20,
        "skills": ["python", "mern"],
        "projects": {
            "expense_tracker": True,
            "chat_app": True
        }
    }

    json_string = json.dumps(python_obj, indent=4)

    print("Python object -> JSON string")
    print(type(json_string))
    print(json_string)
    print()

# dump
def write_json_file() -> None:
    """Write Python data into a JSON file."""
    data = {
        "name": "yash",
        "city": "Surat",
        "hobby": ["movies", "coding"],
        "profile": {
            "role": "IT Engineering Student",
            "year": 4
        }
    }

    with open("yash_info.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Data written to yash_info.json\n")

# load
def read_json_file() -> None:
    """Read JSON data from a file."""
    try:
        with open("yash_info.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        print("JSON file -> Python object")
        print(data)
        print()
    except FileNotFoundError:
        print("File not found.\n")

# -------------------------------------------------------------------

def main() -> None:
    """Main Function ."""
    json_string_to_python()
    python_to_json_string()
    write_json_file()
    read_json_file()

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()

