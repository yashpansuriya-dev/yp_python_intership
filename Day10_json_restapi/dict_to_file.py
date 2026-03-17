"""
Convert a Python dict to JSON, save to file, reload it and verify the data
"""
# -------------------------------------------------------------------

import json

# -------------------------------------------------------------------

def dict_to_json(dict : dict) -> str:
    """
    It converts Dict object into
    JSON string.

    dict (dict) : dict object
    """
    data = json.dumps(dict)
    return data

def save_file(filename: str, data :str):
    """
    It Creates/Overwrite the file with given 
    JSON string.

    Args :
        filename (str) : name of file
        data (str) : JSON String.
    """
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def load_file(filename : str) -> dict | list:
    """
        It loads json file and 
        returns data as Python Object.

        Args : 
            filename (str) : name of file to load
    """
    with open(filename, "r") as f:
        data = json.load(f)
    return data

# -------------------------------------------------------------------

def main() -> None:
    """ Main Function . """

    student_details = {
        "name" : "yash pansuriya",
        "age" : 20,
        "marks": {
            "phy" : 98,
            "che" : 88,
            "maths" : 76
        },
        "cgpa" : 8.5
    }

    # Convert Dict to JSON
    student_details_json = dict_to_json(student_details)
    print(student_details_json)

    # Save json to file
    save_file("Files/task3.json", student_details)

    # Reload data
    new_json_data = load_file("Files/task3.json")
    print(new_json_data)

    # Verify the data
    if(student_details == new_json_data):
        print("Data is verified and same")
    else:
        print("Data are not same")

# -------------------------------------------------------------------

if __name__ == '__main__':
    main()
