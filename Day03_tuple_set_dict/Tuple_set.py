"""
Utility functions for tuple operations, unique elements, and vector math.
"""

#-------------------------------------------------------------------

def concatenate_tuples(tuple_a : tuple, tuple_b : tuple ) -> tuple : 
    """
    Concatenate two tuples.

    Args:
        tuple_a (tuple): First tuple.
        tuple_b (tuple): Second tuple.

    Returns:
        tuple: Combined tuple.
    """
    return tuple_a + tuple_b

def get_unique_elements(data : list) -> list :
    """
    Return unique elements from a list using a set (order not guaranteed).

    Args:
        data (list): Input list.

    Returns:
        list: List of unique elements.
    """
    return list(set(data))


def add_3d_vectors(point_a : tuple ,  point_b : tuple) -> tuple :
    """
    Add two 3D vectors represented as tuples.

    Args:
        point_a (tuple): First 3D point (x, y, z).
        point_b (tuple): Second 3D point (x, y, z).

    Returns:
        tuple: Resultant 3D vector.
    """
    return (
        point_a[0] + point_b[0],
        point_a[1] + point_b[1],
        point_a[2] + point_b[2],
    )

def getting_names() -> list:
    """
        Takes names as input from user , 
        and return list containing all names .

        Args :
            None

        Returns :
            list : Resultat list containing names entered by user.

    """
    names = []
    name = ""
    
    while(name != 'None'):
        name = input("Enter name , type 'None' to stop : ")
        if name != 'None':
            names.append(name)

    return names

def find_duplicate(names : list) -> list :
    """
        Find Duplicate elements from a list and returns
        new list containing duplicate elements.

        Args:
            names (list) : Input list containing duplicate or non duplicate elements.

        Returns :
            list : Resultant list containg duplicate elements.
    """
    set1 = set()

    for n in names:
        names.remove(n)
        if n in names:
            set1.add(n)

    return list(set1)


def main() -> None :
    """Run sample operations."""

    # Tuple operations
    tuple_1 = (1, 2, 3, 4, 2, 2, 9, 8)
    tuple_2 = (10, 11, 12)

    print("Original tuple:", tuple_1)
    print("Concatenated tuple:", concatenate_tuples(tuple_1, tuple_2))

    # Unique elements
    data_list = [43, 1, 4, 5, 8, 7, 4, 1, 2, 2, 6, 9, 4, 4, 3, 15, 25, 8, 41]

    print("Unique (set):", get_unique_elements(data_list))

    # Vector addition
    point_1 = (2, 3, -1)
    point_2 = (-1, 2, 1)

    print("Vector sum:", add_3d_vectors(point_1, point_2))
    
    # Finding Duplicate names
    names  = getting_names()
    print("Your entered names : " ,names)
    print(find_duplicate(names))


if __name__ == "__main__":
    main()
   

