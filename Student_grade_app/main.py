# -------------------------------------------------------------------

from Services.student_manager import StudentManager, StudentNotFoundError

# -------------------------------------------------------------------
# Input Validation Function

class LengthError(Exception):
    pass
# ------------------------------------------------------------------

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
            print("roll no. can only be number")
    

def safe_name_input(prompt):
    """
        It fetches name untill 
        gets valid name
    """
    while True:
        name = input(prompt)
        if(len(name) > 10):
            print("name must be less than 10 characters")
        elif(not name.isalpha()):
            print("name can only be in letters .")
        elif not name:
            print("name can not be empty")
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
    """Keep prompting until the user picks a valid subject index (0/1/2)."""
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

# def safe_rollno_input_with_no_duplicate(prompt):
#     rollno = safe_int_input(prompt)


# ------------------------------------------------------------------
# Main Menu 
# ------------------------------------------------------------------

def menu():
    manager = StudentManager()

    # Loop Iterates until user exit
    while True:
        print("\n--- Student Grade App ---")
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Search Student")
        print("4. List Students")
        print("5. Highest Total Marks")
        print("6. Highest Marks By Subject")
        print("7. Student Overall Result")
        print("8. Update Marks of subject")
        print("9. Save to JSON File")
        print("10. Load data from JSON File")
        print("11. Top Performers Student")
        print("12. Search Student by roll number")
        print("0. Exit")

        choice = None
        try:
            choice = int(input("Enter choice: "))
        except ValueError as e:
            print("Please enter number only")
            continue

        subjects = ["Physics", "Chemistry", "Maths"]

        # Add Student
        if choice == 1:
            # roll_num = int(input("Enter Your roll number : "))
            roll_num = safe_int_input("Enter Your roll number : ")
            if manager.is_roll_exists(roll_num):
                print("Roll number already exits")
                continue

            name = safe_name_input("Enter name: ").strip()
            if manager.is_name_exists(name):
                print("name already exists")
                continue

            marks = []

            for i in range(3):
                marks.append(safe_marks_input(f"Enter marks for {subjects[i]} (0-100): "))

            manager.add_student(roll_num, name, marks)

        # Delete Student
        elif choice == 2:
            name = safe_name_input("Enter name to delete: ")
            if not manager.is_name_exists(name):
                print(f"Student with name {name} doesn't exist")
                continue

            confirm = input(f"Are you sure you want to delete '{name}' (y/n) :").strip().lower()
            if confirm == "y":
                manager.delete_student(name)
                print(f"{name} Deleted succesfully")
            else:
                print("Deletion cancelled")
            
        # Search Student
        elif choice == 3:
            name = safe_name_input("Enter name to search: ")
            try:
                student = manager.search_student(name)
            except StudentNotFoundError as e:
                print(e)
            else:
                print(student)


        # List Students
        elif choice == 4:
            manager.list_students()

        # Highest total marks
        elif choice == 5:
            try:
                max_student = manager.highest_total_mark_student()
                print(f"Highest Total Mark student is {max_student.name} "
                    f"with {sum(max_student.marks)} marks. out of 300 marks")
            except ValueError as e:
                print(e)
        
        # Highest marks by subject
        elif choice == 6:
            idx = safe_subject_input()
            try:
                max_student = manager.highest_mark_by_subject(idx)
                print(f"Highest Marks student in {subjects[idx]} is {max_student.name } "
                    f"with {max_student.marks[idx]} marks out of 100 marks")
            except ValueError as e:
                print(e)

        # Student results
        elif choice == 7:
            name = safe_name_input("Enter name to search: ")
            try:
                student = manager.search_student(name)
                print(
                        f"Marks['Phy', 'Che.', 'Maths']: {student.marks} | "
                        f"Percentage: {student.get_percentage():.2f} | "
                        f"Grade: {student.get_grade()} | "
                        f"GPA: {student.get_gpa():.2f} | "
                    )
            except StudentNotFoundError as e:
                print(e)

        # Update marks
        elif choice == 8:
            # try:
            #     roll_num = int(input_rollno_check_duplicates("Enter roll number of that student"))
            # except:
            roll_num = safe_int_input("Enter roll number of that student")
            if not manager.is_roll_exists:
                print(f"No such student exists with roll no. {roll_num}")
                continue
            idx = safe_subject_input()
            marks = safe_marks_input(f"Enter the updated marks for {subjects[idx]}")
            manager.update_student_marks(roll_num, marks, idx)

        # Save to JSON
        elif choice == 9:
            manager.save_to_json()
        
        # Load to JSON
        elif choice ==10:
            manager.load_from_json("Database/student_data.json")
        
        # Fetching top performer student
        elif choice ==11:
            manager.top_performers()

        # search student by roll number
        elif choice == 12:
            roll_no = safe_int_input("Enter roll number to search: ")
            try:
                student = manager.search_student_by_roll_no(roll_no)
            except StudentNotFoundError as e:
                print(e)
            else:
                print(student)

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