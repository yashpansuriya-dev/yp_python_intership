"""
    Validation file : 
    It validates user input with different mathods

    safe_input_noduplicte -> It takes input where , input does not match
                        with existing students.

    safe_input_unless_duplicate -> here, input should contain in students data.
                                used to, search and delete.
                
    safe_update_input -> it uses in update function to it also accepts
                        input such as blank(for not changing data).
"""


class Validation:
    # -------------------------------------------------------------------
    # Roll no. Validation
    # -------------------------------------------------------------------
    def safe_int_input(self, prompt):
        """
            It try fetching int input 
            unless gets valid input.
        """
        while True:
            try:
                value = int(input(prompt))
                if(value > 0):
                    return value
                print("             please enter positive number")
            except ValueError:
                print("             Roll no. can only be number")

    def safe_rollno_input_noduplicate(self, prompt, manager):
        """ It fetches roll no. unless user enters 
            valid roll no. and it is unique
        """         
        while True:
            try:
                value = int(input(prompt))
                if(manager.is_roll_exists(value)):
                    print(f"            Roll no: {value} Already exists")
                    continue
                if(value > 0):
                    return value
                print("             please enter positive number")

            except ValueError:
                print("             Roll no. can only be number")

    def safe_rollno_input_unless_duplicate(self, prompt, manager):
        """ It fetches roll no. unless user enters 
            valid roll no. and it should contain in manager.
        """
        while True:
            try:
                value = int(input(prompt))
                if(not manager.is_roll_exists(value)):
                    print(f"            No such student exists with roll no. {value} .")
                    continue
                if(value > 0):
                    return value
                print("             please enter positive number")

            except ValueError:
                print("             Roll no. can only be number")
        

    # -------------------------------------------------------------------
    # Name Validation
    # -------------------------------------------------------------------

    def safe_name_input(self,prompt):
        """
            It fetches name untill 
            gets valid name
        """
        while True:
            name = input(prompt).strip()
            if(len(name) > 20):
                print("             name must be less than 20 characters")
            elif(not name.isalpha()):
                print("             name can only be in letters .")
            elif not name:
                print("             name can not be empty")
            else:
                return name
            
    def safe_name_input_noduplicate(self,prompt, manager):
        """
            It fetches name untill gets valid 
            name and it should be unique
        """
        while True:
            name = input(prompt).strip()
            if name == "" or name == " ":
                print("             name can not be empty .")
            elif(len(name) > 20):
                print("             name must be less than 20 characters")
            elif manager.is_name_exists(name):
                print(f"            name : {name} already exists")
            elif not self.is_valid_name(name):
                print("             Name can only be letters , _ or spaces .")
            else:
                return name
            
    def safe_name_input_unless_duplicate(self,prompt, manager):
        """
            It fetches name untill gets valid 
            name and it should be unique
        """
        while True:
            name = input(prompt).strip()
            if(len(name) > 20):
                print("             name must be less than 20 characters")
            elif(not name.isalpha()):
                print("             name can only be in letters .")
            elif not name:
                print("             name can not be empty")
            elif not manager.is_name_exists(name):
                print(f"            No such student exists with name :  {name} .")
            else:
                return name


    # -------------------------------------------------------------------
    # Marks Validation
    # -------------------------------------------------------------------

    def safe_marks_input(self, prompt):
        """
            It fetches marks untill 
            gets valid marks
        """
        while True:
            try:
                mark = int(input(prompt))
                if 0 <= mark <= 100:
                    return mark
                else:
                    print("             Enter Value between 0 and 100")
            except ValueError:
                print("             Enter valid number")


    def safe_subject_input(self) -> int:
        """ keep prompting until the user picks a valid subject index (0/1/2)."""
        print("  0. Physics")
        print("  1. Chemistry")
        print("  2. Maths")
        while True:
            try:
                idx = int(input("  Enter subject number: "))
                if idx in (0, 1, 2):
                    return idx
                print("  Please enter 0, 1, or 2.")
            except ValueError:
                print("  Please enter a number.")



    # -------------------------------------------------------------------
    # Updates Validation
    # -------------------------------------------------------------------

    def update_safe_rollno_input_noduplicate(self,prompt, manager):
        """ It fetches roll no. unless user enters 
            valid roll no. and it is unique
        """
        while True:
            try:
                val = input(prompt)
                if val == "":
                    return val
                
                value = int(val)
                if(manager.is_roll_exists(value)):
                    print(f"Roll no: {value} Already exists")
                    continue
                if(value > 0):
                    return value
                print("enter positive number")
            except ValueError:
                print("Roll no. can only be number")

    def update_safe_marks_input(self,prompt):
        """
            It fetches marks untill 
            gets valid marks
        """
        while True:
            try:
                ma = input(prompt)
                if ma == "":
                    return ma
                mark = int(ma)
                if 0 <= mark <= 100:
                    return mark
                else:
                    print("Enter Value between 0 and 100")
            except ValueError:
                print("Enter valid number")

    def update_safe_name_input_noduplicate(self,prompt, manager):
        while True:
            name = input(prompt).strip()

            if name == "":
                return name

            if len(name) > 20:
                print("name must be less than 20 characters")

            elif not is_valid_name(name):
                print("name can only contain letters, spaces, or underscore.")

            elif manager.is_name_exists(name):
                print(f"name : {name} already exists")

            else:
                return name
            
    def is_valid_name(self,name):
        for ch in name:
            if not (ch.isalpha() or ch == " " or ch == "_"):
                return False
        return True