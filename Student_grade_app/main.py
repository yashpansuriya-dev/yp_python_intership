# -------------------------------------------------------------------

from Services.student_manager import StudentManager

# -------------------------------------------------------------------

def menu():
    manager = StudentManager()

    # Loop Iterates untill user exit
    while True:
        print("\n--- Student Grade App ---")
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Search Student")
        print("4. List Students")
        print("5. Highest Marks")
        print("6. Update Marks")
        print("7. Save to JSON File")
        print("8. Exit")

        choice = int(input("Enter choice: "))

        if choice == 1:
            roll_num = int(input("Enter Your roll number : "))
            name = input("Enter name: ")
            marks = int(input("Enter marks: "))
            manager.add_student(roll_num, name, marks)


        elif choice == 2:
            name = input("Enter name to delete: ")
            manager.delete_student(name)


        elif choice == 3:
            name = input("Enter name to search: ")
            student = manager.search_student(name)
            if(student != None):
                print(f"Roll no.: {student['roll_num']} |"
                      f"Name: {student['name']} |" 
                      f"Marks: {student['marks']} |"
                      f"Grade: {manager.get_grade(student['marks'])}"
                )
            else:
                print("No such student found")


        elif choice == 4:
            manager.list_students()


        elif choice == 5:
            max_student = manager.highest_mark_student()
            print(f"Highest Mark student is {max_student['name']}"
                  f"with {max_student['marks']} marks.")
        

        elif choice == 6:
            roll_num = int(input("Enter roll number of that student"))
            marks = int(input("Enter the updated marks"))
            manager.update_student_marks(roll_num, marks)
        

        elif choice == 7:
            manager.save_to_json()


        elif choice == 8:
            break


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