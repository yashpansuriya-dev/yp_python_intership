"""
    A registration form , that fetches details
    from user , such as name, age, email and raises
    error if invalid format . 
    
    and with the use of try-except-else-finally it 
    cathces the error . 
"""

# -------------------------------------------------------------------

class InvalidAgeError(Exception):
    pass

class NameError(Exception):
    pass

class InvalidEmailError(Exception):
    pass

# -------------------------------------------------------------------

def age() -> int:
    """
        It fetches age from user , and raise error if age is
        invalid .

        Returns :
            int : age
    """
    try:
        age = int(input("\nEnter Your age : "))
        if age < 0:
            raise InvalidAgeError("Age Can not be negative")
    except ValueError:
        print("It needs to be number")
    except InvalidAgeError as e:
        print(e)
    else:
        return age
    finally:
        print("Input process finished\n")


def name() -> str:
    """
        It fetches name from user , and raise 
        error if name is too long .

        Returns :
            str : name
    """
    try:
        name = input("Enter Your name : ")
        if(len(name) > 10):
            raise NameError("name too long")
    except NameError:
        print("Name is too long , try shorten")
    else:
        return name
    finally:
        print("Name process finished ")


def email() -> str:
    """
        It fetches email from user , and raise 
        error if email is invalid .

        Format for Valid Email :
            username@domain
            yashpansuriya@gmail.com

        Returns :
            str : email
    """
    try:
        email = input("Enter your email : ")
        email = email.strip()
        if(email.count('@') != 1 or email.find('@') in [-1, 0, len(email)-1]):
            raise InvalidEmailError("It has must be one @")
        if(email.find('.') == -1):
            raise InvalidEmailError("It must has domain ")
    except InvalidEmailError:
        print("Enter valid email")
    else:
        return email
    finally:
        print("Email operation succesfull")


def registration():
    """
        It fetch input data from user such as
        email ,age, name .
    """
    user_name = name()
    user_email = email()
    user_age = age()

    print("\nHere's Detail of user : ")
    print("Name : " , user_name)
    print("Email : " , user_email)
    print("Age : " , user_age)


# -------------------------------------------------------------------

def main() -> None:
    """ Main Function . """
    print("Hello")
    registration()

# -------------------------------------------------------------------

if __name__ == '__main__':
    main()