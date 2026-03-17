# -------------------------------------------------------------------

from Services.student_manager import StudentManager

# -------------------------------------------------------------------

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
        print("0. Exit")

        choice = int(input("Enter choice: "))
        subjects = ["Physics", "Chemistry", "Maths"]

        # Add Student
        if choice == 1:
            roll_num = int(input("Enter Your roll number : "))
            name = input("Enter name: ")
            marks = []

            for i in range(3):
                marks.append(int(input(f"Enter marks for {subjects[i]}: ")))

                
            manager.add_student(roll_num, name, marks)

        # Delete Student
        elif choice == 2:
            name = input("Enter name to delete: ")
            manager.delete_student(name)

        # Search Student
        elif choice == 3:
            name = input("Enter name to search: ")
            student = manager.search_student(name)
            if(student != None):
                print(f"Roll no.: {student['roll_num']} |\n"
                      f"Name: {student['name']} |\n" 
                      f"Marks['Phy', 'Che.', 'Maths']: {student['marks']} |\n"
                      f"Percentage: {manager.get_percentage(student['marks']):.2f} % |\n"
                      f"Grade: {manager.get_grade(student['marks'])} |\n"
                      f"GPA: {manager.get_gpa(student['marks']):.2f} | \n"
                )
            else:
                print("No such student found")

        # List Students
        elif choice == 4:
            manager.list_students()

        # Highest total marks
        elif choice == 5:
            max_student = manager.highest_total_mark_student()
            print(f"Highest Total Mark student is {max_student['name']} "
                  f"with {sum(max_student['marks'])} marks. out of 300 marks")
        
        # Highest marks by subject
        elif choice == 6:
            print("Enter number accroding to Subject , For")
            idx = int(input("0. Physics\n1. Chemistry\n2. Maths"))
            max_student = manager.highest_mark_by_subject(idx)
            print(f"Highest Marks student in {subjects[idx]} is {max_student['name'] }"
                  f"with {max_student['marks'][idx]} marks. out of 100 marks")

        # Student results
        elif choice == 7:
            name = input("Enter name to search: ")
            student = manager.search_student(name)
            if(student != None):
                print(
                      f"Marks['Phy', 'Che.', 'Maths']: {student['marks']} | "
                      f"Percentage: {manager.get_percentage(student['marks']):.2f} | "
                      f"Grade: {manager.get_grade(student['marks'])} | "
                      f"GPA: {manager.get_gpa(student['marks']):.2f} | "
                )
            else:
                print("No such student found")

        # Update marks
        elif choice == 8:
            roll_num = int(input("Enter roll number of that student"))
            print("Enter number accroding to Subject , For")
            idx = int(input("0. Physics\n1. Chemistry\n2. Maths"))
            marks = int(input("Enter the updated marks"))
            manager.update_student_marks(roll_num, marks, idx)

        # Save to JSON
        elif choice == 9:
            manager.save_to_json()

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