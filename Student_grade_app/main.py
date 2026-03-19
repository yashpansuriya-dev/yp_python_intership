# -------------------------------------------------------------------
# main.py
# -------------------------------------------------------------------

"""
        Add
        List -> all , top performers
        Update -> student -> all upadete , blank if dont
        Delete -> by name, roll no
        Search -> by name, roll no
        Highest -> total , subject topper
"""


from Services.student_manager import StudentManager, StudentNotFoundError

from validation import (safe_int_input,safe_marks_input,safe_name_input,
                        safe_rollno_input_noduplicate, safe_rollno_input_unless_duplicate,
                        safe_name_input_noduplicate, safe_name_input_unless_duplicate , 
                        safe_subject_input,
                        update_safe_marks_input,
                        update_safe_name_input_noduplicate,
                        update_safe_rollno_input_noduplicate)

# -------------------------------------------------------------------
# Input Validation Functions
# -------------------------------------------------------------------

class LengthError(Exception):
    pass

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
        print("||  ---Select Operation to Perform ---        ||")
        print("||  1. Add Student                            ||")
        print("||  2. List Students                          ||")
        print("||  3. Update Student                         ||")
        print("||  4. Search Student                         ||")
        print("||  5. Delete Student                         ||")
        print("||  6. Fetch Highest Marks Student's          ||")
        print("||  0. Exit Application                       ||")
        print("=================================================")

        choice = None
        try:
            choice = int(input("Enter choice: "))
        except ValueError as e:
            print("Please enter number only")
            continue

        subjects = ["Physics", "Chemistry", "Maths"]

        # Add Student
        # -------------------------------------------------------------------
        if choice == 1:
            # Fetches Valid roll no.
            roll_num = safe_rollno_input_noduplicate("        Enter Your roll number : ", manager)
            if manager.is_roll_exists(roll_num):
                print("Roll number already exits")
                continue
            
            # Fetches valid name
            name = safe_name_input_noduplicate("        Enter name : ",manager).strip()
            if manager.is_name_exists(name):
                print("name already exists")
                continue

            # Fetches Valid SUbject marks
            marks = []
            for i in range(3):
                marks.append(safe_marks_input(f"            Enter marks for {subjects[i]} (0-100) : "))

            manager.add_student(roll_num, name, marks)
            manager.save_to_json()

        # List Student
        # ------------------------------------------------------------------
        elif choice == 2:
            print("     Select Operation")
            print("     1.List All Students")
            print("     2.List Top Performance Students(GPA > 3.5)")

            while True:
                c = int(input("Select Operation : "))
                if c in [1,2]:
                    break
                print("Enter Valid Choice ")

            # List Students
            if c == 1:
                if manager.is_empty():
                    print("No Student added yet")
                    continue

                manager.list_students()

            # Fetching top performer student
            else:
                if manager.is_empty():
                    print("No Student added yet")
                    continue
                manager.top_performers()

        #Update Student
        # ------------------------------------------------------------------
        elif choice == 3:
            id = safe_rollno_input_unless_duplicate("Enter Roll number to Update Student : ", manager)

            new_roll = update_safe_rollno_input_noduplicate("        Enter New roll number(Leave Blank if not want update) : ", manager)
            if manager.is_roll_exists(new_roll):
                print("Roll number already exits")
                continue
            
            # Fetches valid name
            name = update_safe_name_input_noduplicate("        Enter name: ",manager).strip()
            if manager.is_name_exists(name):
                print("name already exists")
                continue

            # Fetches Valid SUbject marks
            marks = []
            for i in range(3):
                marks.append(update_safe_marks_input(f"            Enter marks for {subjects[i]} (0-100): "))


            manager.update_student(id, new_roll, name, marks)
            manager.save_to_json()
        
        # Search Student
        # ------------------------------------------------------------------
        elif choice == 4: 
            if manager.is_empty():
                print("No Student added yet")
                continue

            print(" --   Search Student ---")
            print("     1.By Name")
            print("     2.By Roll number")

            while True:
                c = int(input("Select Operation : "))
                if c in [1,2]:
                    break
                print("Enter Valid Choice ")
            
            if c == 1:
                name = safe_name_input_unless_duplicate("       Enter name to search : ",manager)
                student = manager.search_student(name)
                print(student)
            else:
                roll_no = safe_rollno_input_unless_duplicate("      Enter roll number to search : ", manager)
                student = manager.search_student_by_roll_no(roll_no)
                print(student)

        # Delete Student
        # ------------------------------------------------------------------
        elif choice == 5:
            if manager.is_empty():
                print("No Student added yet")
                continue

            print(" --   Delete Student ---")
            print("     1.By Name")
            print("     2.By Roll number")

            while True:
                c = int(input("Select Operation : "))
                if c in [1,2]:
                    break
                print("Enter Valid Choice ")

            if c == 1:
                #cc
                name = safe_name_input_unless_duplicate("       Enter name to delete : ", manager)
                confirm = input(f"Are you sure you want to delete student with name:'{name}' (y/n) :").strip().lower()
                if confirm == "y":
                    manager.delete_student_by_name(name)
                    print(f"Name : {name} Deleted succesfully")
                    manager.save_to_json()
                else:
                    print("Deletion cancelled")  
                
            else:
                id = safe_rollno_input_unless_duplicate("       Enter roll no. to delete : ", manager)
                confirm = input(f"Are you sure you want to delete student with id:'{id}' (y/n) :").strip().lower()
                if confirm == "y":
                    manager.delete_student(id)
                    print(f"Roll no. : {id} Deleted succesfully")
                    manager.save_to_json()
                else:
                    print("Deletion cancelled")

        # highest marks
        # ------------------------------------------------------------------
        elif choice == 6:
            if manager.is_empty():
                print("No Student added yet")
                continue

            print(" --   Highest Student ---")
            print("     1. Highest Total Mark")
            print("     2. Topper of Subject")
            print("     3. Print a Student's Overall Result")

            while True:
                c = int(input("Select Operation : "))
                if c in [1,2,3]:
                    break
                print("Enter Valid Choice ")
            
            if c == 1:
                try:
                    max_student = manager.highest_total_mark_student()
                    print(f"        Highest Total Mark student is '{max_student.name}' "
                        f"with '{sum(max_student.marks)}' marks out of 300 marks")
                except ValueError as e:
                    print(e)
            # Highest marks by subject
            elif c == 2:
                idx = safe_subject_input()
                try:
                    max_student = manager.highest_mark_by_subject(idx)
                    print(f"        Highest Marks student in '{subjects[idx]}' is '{max_student.name }' "
                        f"with '{max_student.marks[idx]}' marks out of 100 marks")
                except ValueError as e:
                    print(e)

            # Student results
            elif c == 3:
                # Asks valid roll no.
                id = safe_rollno_input_unless_duplicate("       Enter roll no. of student to get result : ", manager)
                student = manager.search_student_by_roll_no(id)
                print(
                            f"\nMarks['Phy', 'Che.', 'Maths']: {student.marks}                 "
                            f"\nPercentage:                    {student.get_percentage():.2f}  "
                            f"\nGrade:                         {student.get_grade()}           "
                            f"\nGPA:                           {student.get_gpa():.2f}        "
                        )


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
