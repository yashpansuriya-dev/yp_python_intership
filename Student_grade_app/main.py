# -------------------------------------------------------------------

from Services.student_manager import StudentManager

# -------------------------------------------------------------------
# Input Validation Function
# ------------------------------------------------------------------

def safe_int_input(prompt):
    """
        It try fetching int input 
        unless gets valid input.
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Enter Valid name")
    

def safe_name_input(prompt):
    """
        It fetches name untill 
        gets valid name
    """
    while True:
        try:
            return input(prompt)
        except ValueError:
            print("Enter valid name")


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
        print("0. Exit")

        choice = None
        try:
            choice = int(input("Enter choice: "))
        except ValueError as e:
            print("Invalid Input, enter number only")

        subjects = ["Physics", "Chemistry", "Maths"]

        # Add Student
        if choice == 1:
            # roll_num = int(input("Enter Your roll number : "))
            roll_num = safe_int_input("Enter Your roll number : ")
            name = safe_name_input("Enter name: ").strip()
            marks = []

            for i in range(3):
                marks.append(safe_marks_input(f"Enter marks for {subjects[i]}: "))

                
            manager.add_student(roll_num, name, marks)

        # Delete Student
        elif choice == 2:
            name = safe_name_input("Enter name to delete: ")
            manager.delete_student(name)

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
            max_student = manager.highest_total_mark_student()
            print(f"Highest Total Mark student is {max_student.name} "
                  f"with {sum(max_student.marks)} marks. out of 300 marks")
        
        # Highest marks by subject
        elif choice == 6:
            print("Enter number accroding to Subject , For")
            idx = int(input("0. Physics\n1. Chemistry\n2. Maths"))
            max_student = manager.highest_mark_by_subject(idx)
            print(f"Highest Marks student in {subjects[idx]} is {max_student.name }"
                  f"with {max_student.marks[idx]} marks. out of 100 marks")

        # Student results
        elif choice == 7:
            name = safe_name_input("Enter name to search: ")
            student = manager.search_student(name)
            if(student != None):
                print(
                      f"Marks['Phy', 'Che.', 'Maths']: {student.marks} | "
                      f"Percentage: {student.get_percentage():.2f} | "
                      f"Grade: {student.get_grade()} | "
                      f"GPA: {student.get_gpa():.2f} | "
                )
            else:
                print("No such student found")

        # Update marks
        elif choice == 8:
            roll_num = int(input("Enter roll number of that student"))
            print("Enter number accroding to Subject , For")
            idx = int(input("0. Physics\n1. Chemistry\n2. Maths"))
            marks = safe_marks_input("Enter the updated marks")
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

        # Exit application
        elif choice == 0:
            break

        # Invalid choice
        else:
            print("Invalid choice!")

# -------------------------------------------------------------------

def main() -> None:
    """ Main Function . """
    print("hello")
    menu()

# -------------------------------------------------------------------

if __name__ == '__main__':
    main()