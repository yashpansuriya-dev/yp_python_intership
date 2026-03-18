'''
    StudentManager
    ==============

    Manages student objects and performing operations on it.

    Add_student -> it adds student .
    Search_student -> search student by given name
    Delete_student -> delete student record by name
    List_students -> list all student's details.
    highest_mark_student -> returns student who got highest total marks
    highest_mark_by_subject -> return student with highest marks in particular
    subject
    update_mark -> it updates marks of student by given roll number and subject
    get_percentage -> returns percentage of student 
    get_gpa -> calculate GPA of student
    get_grade -> calculate grade accroding to marks
    save_to_json -> create or overwrite file with updated student details
    top_performer_student -> prints list of student with gpa > 3.5
'''

# ------------------------------------------------------------------
# Starting of program
# ------------------------------------------------------------------

import json
from Model.student import Student

# -------------------------------------------------------------------
# Custom Exception
# ------------------------------------------------------------------


class InputValidationError(Exception):
    pass

class StudentNotFoundError(Exception):
    pass

# -------------------------------------------------------------------
# Student Manager
# -------------------------------------------------------------------


class StudentManager:
    """
        StudentManager class that represent a list of student , 
        and it has functionality of add, delete, list, update marks,
        seach students .
    """

    def __init__(self):
        """
            Constructor that initializes , list of 
            students.
        """
        self.students = []

    # ------------------------------------------------------------------
    # CRUD Functions
    # ------------------------------------------------------------------
        
    # ADD
    def add_student(self, roll_num: int, name: str, marks: list):
        """
            It takes input such as name, marks, roll number
            from student , and add it to list as dict.
        """

        try:
            self._validate_name(name)
            self._validate_roll(roll_num)
            self._validate_marks(marks)
            student = Student(roll_num, name, marks)
            self.students.append(student)
        except InputValidationError as e:
            print("Validation Error:", e)
        except Exception as e:
            print("Unexpected Error:", e)
        else:
            print("Student Added Succesfully")

    # SEARCH
    def search_student(self, name: str):
        """
            It searches student by name , and
            returns none if not found it.
        """
        for student in self.students:
            if student.name == name:
                return student
        raise StudentNotFoundError(f"{name} not found .")

    # DISPLAY
    def list_students(self):
        """
            It prints list of all students and 
            their details.
        """
        print("\nHere List of all students : ")
        for student in self.students:
            # print(student)
            print(student)
    
    # DELETE
    def delete_student(self, name: str):
        """
            It deletes record of student by 
            name.
        """
        try:
            del_student = self.search_student(name)
            self.students.remove(del_student)
        except StudentNotFoundError as e:
            print(e)
        else:
            print("Student deleted succesfully")
            
    # ------------------------------------------------------------------
    # Academic Functions
    # ------------------------------------------------------------------
    
    def highest_total_mark_student(self):
        """
            It returns students who got highest 
            total marks of 3 subjects.
        """
        max_marks = -1

        for student in self.students:
            total_mark = sum(student.marks)
            if(total_mark > max_marks):
                max_marks = total_mark
                max_student = student
        
        return max_student
    

    def highest_mark_by_subject(self, idx):
        """
            returns student with highest mark in
            given subject
        """
        max_marks = -1

        for student in self.students:
            total_mark = student.marks[idx]
            if(total_mark > max_marks):
                max_marks = total_mark
                max_student = student
        
        return max_student
    

    def top_performers(self):
        """
            It list students with GPA >3.5 .
        """
        print("\n Top Performance Students : ")
        for student in self.students:
            if student.get_gpa() >= 3.5:
                print(student)
        

    def update_student_marks(self, roll_num: int, new_mark: int, idx: int):
        """
            It updates student's marks by given their
            roll number and new marks .

            Args:
                self : currrent instance of class
                roll_num : of student to get updated.
                new_mark : updated marks
        """
        
        for student in self.students:
            if student.roll_num == roll_num:
                student.marks[idx] = new_mark
            

    # ------------------------------------------------------------------
    # Save and Load from JSON File
    # ------------------------------------------------------------------

    def save_to_json(self):
        """
            It overwrite or create file by adding 
            student's details as json .
        """
        try:
            data = [student.to_dict() for student in self.students]

            with open("./Database/student_data.json", "w") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print("File error",e)
        except Exception as e:
            print("Unexpected error", e)
        else:
            print("Saved succesfully")
    

    def load_from_json(self , filename):
        """
            It loads students data from JSON file , 
            and store in students.

            Args:
                filename : name of file to fetched data
        """
        try:
            with open(filename, "r") as f:
                data = json.load(f)

                for d in data:
                    student = Student(d['roll_num'], d['name'], d['marks'])
                    self.students.append(student)
        except IOError as e:
            print("File error",e)
        except Exception as e:
            print("Unexpected error", e)
        else:
            print("Data Loaded succesfully")


    # ------------------------------------------------------------------
    # Validate input and raises errors
    # ------------------------------------------------------------------

    def _validate_roll(self, roll_no):
        """
            It validates roll number enterd by user and
            raises error if rollno. is not number , negative
            and if already added by other.

            Raises:
                InputValidationError
        """
        if not isinstance(roll_no, int) or roll_no<=0:
            raise InputValidationError("Roll no. Must be number and positive")
        
        if any(s.roll_num == roll_no for s in self.students):
            raise InputValidationError("this roll no. already exists")
    
    def _validate_name(self, name):
        """
            It validates name given by user and raises error
            if name is not string .
        """
        if not isinstance(name, str):
            raise InputValidationError("Name must be String")
    
    def _validate_marks(self, marks):
        """
            It validates marks given by user and marks must be
            list containing exactly 3 subjects marks where each marks 
            must be number and between 0 to 100.
        """
        if not isinstance(marks, list) or len(marks) != 3:
            raise InputValidationError("Marks must be list of 3 subjects")

        for m in marks:
            if not isinstance(m, (int, float)) or not (0 <= m <= 100):
                raise InputValidationError("Each mark must be between 0 and 100")
            


# ------------------------------------------------------------------
# End
# ------------------------------------------------------------------

