""" 
Dictionaries
CRUD operations, nested dicts, .get(), .items(), .keys(), .values(), dict comprehension
Build a phonebook: add, search, delete contacts and list all entries.
"""
# -----------------------------------------------------------------

import string

# ----------------------------------------------------------------


def dict_sqaure(nums : list) -> dict :
    """
        Return Dictionary containing key as numbers 
        and value as their squares . 

        Args :
            nums (list) : list of numbers 
        
        Returns :
            Dict containing numbers and their squares
    """
    dict1 = { l : l*l for l in nums } # Dictionary comprehension
    #        key : value

    return dict1

# ------------------------------------------------------------

def main() -> None :
    print("Hello")

    # Dictionary Basic Operations
    dict_1 = {"name": "yash" , "collge" : "vgec" , "cgpa" : 8.7 }

    # Fetching value by key - two ways
    print("\nName by get : ",dict_1.get('name'))
    print("\nName by  method : " , dict_1['name'])

    print("\nKeys of Dict : ",dict_1.keys())
    print("\nValues of Dict : ",dict_1.values())
    print("\nItems of Dict : ",dict_1.items())
    print("\nDict : ",dict_1)


    # List containing dict. as elements
    students = [{"name": "yash" , "college" : "vgec" , "cgpa" : 8.7 } ,
                 {"name" : "brijraj" , "college" : "vgec" , "cgpa" : 9.2 },
                 {"name": "gopal" , "college" : "ld" , "cgpa" : 7.6}]
    
    print("\n Here is List of dicts , Students : ", students)

    # Two methods for iterating
    for s in students :
        print(f"{s['name']} studies in {s['college']} and he got {s['cgpa']} cgpa . ")

    for s in students:
        print("Here detail of : " , s['name'])
        for k in s.keys():
            print(s[k])
    
    # Nested Dict.
    dict_2 = {"name":"chintan" , 'marks' : {'phy' : 98 ,
                                            'che' : 74 ,
                                             'maths' : 86}}

    print("\n Nested Dict , " ,dict_2)

    print(dict_sqaure([1,2,3,4,5,6]))

    
# --------------------------------------------------------------------

if __name__ == "__main__":
    main()