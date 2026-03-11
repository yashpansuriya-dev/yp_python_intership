"""
    Recap Of Concepts learned in Week 1 . 
"""

# -------------------------------------------------------------------

def factorial(n: int) -> int:
    return 1 if n==1 else n*factorial(n-1)

# -------------------------------------------------------------------

def main() -> None:

    """ Main Function. """

    print("Factorial of 5 is : ",factorial(5))

    # Varriables
    a = 5
    name = "yash"
    a = " pansuriya"

    full_name = name + a
    print(full_name)

    list_1 = [1,1,2,3,3,3,4,5,5,]
    print("Original List : ",list_1)
    list_1.append(8)
    list_1.remove(2)
    list_1.pop(0)
    list_1.insert(0,9)
    print("Modified List : ",list_1)


    tuple_1 = (1,1,2,3,5,6,2,8)
    tuple_2 = (5,6,8)
    print("\n\nTuple 1 : ",tuple_1)
    print("Tuple 2 : ",tuple_2)

    tuple_3 = tuple_1+tuple_2
    print("Tuple 3 : ",tuple_3)
    


    set_1 = {2,2,3,3,3,4}
    print("\n\nOriginal List : ",set_1)
    set_1.add(5)
    set_1.remove(2)
    print("Modified List : ",set_1)


    dict_1 = {
        "name": "yash",
        "hobby": "Movie",
        "college": "VGEC",
    }

    print("\nOriginal Dict : ",dict_1)

    print(dict_1['name'])
    print(dict_1.get('name'))

    dict_1['cgpa'] = 9.8


    # If Key is not present, it gives key error
    # print(dict_1['movie'])

    print(dict_1.items())
    print(dict_1.keys())
    print(dict_1.values())

    print("\nType of dict.items() is : ",type(dict_1.items()))
    print(type(dict_1.keys()))
    print(type(dict_1.values()))

    for k,v in dict_1.items():
        print(f"{k} , {v} ,  ")

    print("\nOriginal Dict : ",dict_1)

    cube = lambda x : x**3
    print("cube of 3 is : ",cube(3))

    # MAP FILTER
    numbers = [1,2,3,4,5,6,7,8,9]
    cube_nums = list(map(cube , numbers))
    print("Cube of numbers is : ",cube_nums)

    is_odd = lambda x : x%2 != 0
    odd_cubes = list(filter( lambda x: x%2 !=0 ,cube_nums))
    print("Odd in cubes are : ",odd_cubes)

    for i in range(1,10):
        if i in [5,7]:
            continue    
        print(i , end=" , ")
    
    print("\n\n")
    for i in range(1,10):
        if i == 5:
            break    
        print(i , end=" , ")
    
    str = "yash is good "
    x = str.find('a')
    print(x)

    str.__init__

    print(str.endswith("sh"))

# -------------------------------------------------------------------

if __name__ == "__main__" :
    """ Main Function ."""
    main()

