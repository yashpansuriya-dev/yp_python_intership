# -------------------------------------------------------------------
# main.py
# -------------------------------------------------------------------



from Services.student_manager import StudentManager, StudentNotFoundError

# -------------------------------------------------------------------
# Input Validation Function

class LengthError(Exception):
    pass
# -------------------------------------------------------------------

def safe_int_input(prompt):
    """
        It try fetching int input 
        unless gets valid input.
    """
    while True:
        try:
            value = int(input(prompt))
            if(value > 0):
                return value
            print("please enter positive number")
        except ValueError:
            print("Roll no. can only be number")

def safe_rollno_input_noduplicate(prompt, manager):
    """ It fetches roll no. unless user enters 
        valid roll no. and it is unique
    """
    while True:
        try:
            value = int(input(prompt))
            if(manager.is_roll_exists(value)):
                print(f"Roll no: {value} Already exists")
                continue
            if(value > 0):
                return value
            print("please enter positive number")

        except ValueError:
            print("Roll no. can only be number")

def safe_rollno_input_unless_duplicate(prompt, manager):
    """ It fetches roll no. unless user enters 
        valid roll no. and it should contain in manager.
    """
    while True:
        try:
            value = int(input(prompt))
            if(not manager.is_roll_exists(value)):
                print(f"No such student exists with roll no. {value} .")
                continue
            if(value > 0):
                return value
            print("please enter positive number")

        except ValueError:
            print("Roll no. can only be number")
    

def safe_name_input(prompt):
    """
        It fetches name untill 
        gets valid name
    """
    while True:
        name = input(prompt).strip()
        if(len(name) > 20):
            print("name must be less than 20 characters")
        elif(not name.isalpha()):
            print("name can only be in letters .")
        elif not name:
            print("name can not be empty")
        else:
            return name
        
def safe_name_input_noduplicate(prompt, manager):
    """
        It fetches name untill gets valid 
        name and it should be unique
    """
    while True:
        name = input(prompt).strip()
        if(len(name) > 20):
            print("name must be less than 20 characters")
        elif(not name.isalpha()):
            print("name can only be in letters .")
        elif not name:
            print("name can not be empty")
        elif manager.is_name_exists(name):
            print(f"name : {name} already exists")
        else:
            return name
        
def safe_name_input_unless_duplicate(prompt, manager):
    """
        It fetches name untill gets valid 
        name and it should be unique
    """
    while True:
        name = input(prompt).strip()
        if(len(name) > 20):
            print("name must be less than 20 characters")
        elif(not name.isalpha()):
            print("name can only be in letters .")
        elif not name:
            print("name can not be empty")
        elif not manager.is_name_exists(name):
            print(f"No such student exists with name :  {name} .")
        else:
            return name


def safe_marks_input(prompt):
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
                print("Enter Value between 0 and 100")
        except ValueError:
            print("Enter valid number")


def safe_subject_input() -> int:
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


# ------------------------------------------------------------------
# Main Menu 
# ------------------------------------------------------------------

def menu():
    manager = StudentManager()
    manager.load_from_json("Database/student_data.json")
    print("\n---Welcome To Student Grade App ---")

    # Loop Iterates until user exit
    while True:
        print("=================================================")

        """
        Add
        List -> all , top performers
        Update -> student -> all upadete , blank if dont
        Delete -> by name, roll no
        Search -> by name, roll no
        Highest -> total , subject topper
        
        """

        print("||  ---Select Operation to Perform ---          ||")
        print("||  1. Add Student                              ||")
        print("||  2. Delete Student                           ||")
        print("||  3. Search Student By name                   ||")
        print("||  4. Search Student by roll number            ||")
        print("||  5. List Students                            ||")
        print("||  6. Update Marks of subject                  ||")
        print("||  7. Highest Total Marks                      ||")
        print("||  8. Highest Marks By Subject                 ||")
        print("||  9. Student Overall Result                   ||")
        print("||  10. Top Performers Student                  ||")
        print("||  0. Exit                                     ||")

        # new
        print("||  ---Select Operation to Perform ---          ||")
        print("||  1. Add Student                              ||")
        print("||  2. List Students                           ||")
        print("||  3. Update Student                   ||")
        print("||  4. Delete Student            ||")
        print("||  5. Search Student                         ||")
        print("||  5. Fetch Highest Marks Student                         ||")

        print("=================================================")


        choice = None
        try:
            choice = int(input("Enter choice: "))
        except ValueError as e:
            print("Please enter number only")
            continue

        subjects = ["Physics", "Chemistry", "Maths"]

        # Add Student
        if choice == 1:
            # Fetches Valid roll no.
            roll_num = safe_rollno_input_noduplicate("        Enter Your roll number : ", manager)
            if manager.is_roll_exists(roll_num):
                print("Roll number already exits")
                continue
            
            # Fetches valid name
            name = safe_name_input_noduplicate("        Enter name: ",manager).strip()
            if manager.is_name_exists(name):
                print("name already exists")
                continue

            # Fetches Valid SUbject marks
            marks = []
            for i in range(3):
                marks.append(safe_marks_input(f"            Enter marks for {subjects[i]} (0-100): "))

            manager.add_student(roll_num, name, marks)
            manager.save_to_json()

        # Delete Student
        elif choice == 2:
            # Check If Students empty
            if manager.is_empty():
                print("No Student added yet")
                continue

            # Asks valid roll no.
            id = safe_rollno_input_unless_duplicate("       Enter roll no. to delete : ", manager)
            confirm = input(f"Are you sure you want to delete student with id:'{id}' (y/n) :").strip().lower()
            if confirm == "y":
                manager.delete_student(id)
                print(f"Roll no. : {id} Deleted succesfully")
                manager.save_to_json()
            else:
                print("Deletion cancelled")
            
        # Search Student
        elif choice == 3:
            if manager.is_empty():
                print("No Student added yet")
                continue

            # name = safe_name_input("        Enter name to search: ")
            name = safe_name_input_unless_duplicate("       Enter name to search",manager)
            student = manager.search_student(name)
            print(student)
        
        # search student by roll number
        elif choice == 4 :
            if manager.is_empty():
                print("No Student added yet")
                continue

            roll_no = safe_rollno_input_unless_duplicate("      Enter roll number to search", manager)
            student = manager.search_student_by_roll_no(roll_no)
            print(student)


        # List Students
        elif choice == 5:
            if manager.is_empty():
                print("No Student added yet")
                continue

            manager.list_students()
        
        # Update marks
        elif choice == 6:
            if manager.is_empty():
                print("No Student added yet")
                continue

            roll_no = safe_rollno_input_unless_duplicate("      Enter roll number to Update : ", manager)
            idx = safe_subject_input()
            marks = safe_marks_input(f"        Enter the updated marks for {subjects[idx]} : ")

            manager.update_student_marks(roll_num, marks, idx)
            manager.save_to_json()


        # Highest total marks
        elif choice == 7:
            if manager.is_empty():
                print("No Student added yet")
                continue

            try:
                max_student = manager.highest_total_mark_student()
                print(f"        Highest Total Mark student is '{max_student.name}' "
                    f"with '{sum(max_student.marks)}' marks out of 300 marks")
            except ValueError as e:
                print(e)
        
        # Highest marks by subject
        elif choice == 8:
            if manager.is_empty():
                print("No Student added yet")
                continue

            idx = safe_subject_input()
            try:
                max_student = manager.highest_mark_by_subject(idx)
                print(f"        Highest Marks student in '{subjects[idx]}' is '{max_student.name }' "
                    f"with '{max_student.marks[idx]}' marks out of 100 marks")
            except ValueError as e:
                print(e)

        # Student results
        elif choice == 9:
            if manager.is_empty():
                print("No Student added yet")
                continue

            # Asks valid roll no.
            id = safe_rollno_input_unless_duplicate("       Enter roll no. of student to get result : ", manager)

            student = manager.search_student_by_roll_no(id)
            print(
                        f"\nMarks['Phy', 'Che.', 'Maths']: {student.marks}                 "
                        f"\nPercentage:                    {student.get_percentage():.2f}  "
                        f"\nGrade:                         {student.get_grade()}           "
                        f"\nGPA:                           {student.get_gpa():.2f}        "
                    )

        
        # Fetching top performer student
        elif choice ==10:
            if manager.is_empty():
                print("No Student added yet")
                continue
            manager.top_performers()

        # Exit application
        elif choice == 0:
            print("Goodbye !")
            break

        # Invalid choice
        else:
            print("Invalid choice! - Please try Again") 

# -------------------------------------------------------------------

def main() -> None:
    """ Main Function . """
    print("hello")
    menu()

# -------------------------------------------------------------------

if __name__ == '__main__':
    main()
