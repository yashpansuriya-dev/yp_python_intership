'''
    Here , It has Class StudentManager, who demonstrates list of
    student . and operations , on it like,

    Add_student -> it adds student .
    Search_student -> search student by given name
    Delete_student -> delete student record by name
    List_students -> list all student's details.
    highest_mark_student -> returns student who got highest marks
    update_mark -> it updates marks of student by given roll number
    get_grade -> calculate grade accroding to marks
    save_to_json -> create or overwrite file with updated student details
'''

# -------------------------------------------------------------------

import json
from Model.student import Student

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
    
    def add_student(self, roll_num: int, name: str, marks: int):
        """
            It takes input such as name, marks, roll number
            from student , and add it to list as dict.
        """
        self.students.append({'roll_num': roll_num , 
                              'name': name,
                              'marks': marks})
    
    def search_student(self, name: str):
        """
            It searches student by name , and
            returns none if not found it.
        """
        for student in self.students:
            if student['name'] == name:
                return student
        
        print("No such student found")
        return None
    
    
    def list_students(self):
        """
            It prints list of all students and 
            their details.
        """
        print("\nHere List of all students : ")
        for student in self.students:
            # print(student)
            print(f"Roll no.: {student['roll_num']} | "
                f"Name: {student['name']} | "
                f"Marks: {student['marks']} |"
                f"Grade: {self.get_grade(student['marks'])}"
                )
    
    
    def delete_student(self, name: str):
        """
            It deletes record of student by 
            name.
        """
        del_student = self.search_student(name)

        if(del_student != None):
            self.students.remove(del_student)
        else:
            print("No such student found")
        
    def highest_mark_student(self):
        """
            It returns students who got highest
            marks.
        """
        max_marks = 0

        for student in self.students:
            if(student['marks'] > max_marks):
                max_marks = student['marks']
                max_student = student
        
        return max_student
    
    def update_student_marks(self, roll_num: int, new_mark: int):
        """
            It updates student's marks by given their
            roll number and new marks .

            Args:
                self : currrent instance of class
                roll_num : of student to get updated.
                new_mark : updated marks
        """
        for student in self.students:
            if student['roll_num'] == roll_num:
                student['marks'] = new_mark

    def get_grade(self, marks: int):
        """
            It assigns grade accroding to marks
            of student.
        """
        if marks <=100 and marks >= 90:
            return 'A'
        elif marks >=75 and marks < 90:
            return 'B'
        elif marks >=60 and marks < 75:
            return 'B'
        elif marks >=34 and marks < 60:
            return 'B'
        elif marks >=0 and marks < 34:
            return 'F'
        else:
            return 'Invalid Marks'
    
    def save_to_json(self):
        """
            It overwrite or create file by adding 
            student's details as json .
        """
        try:
            with open("./Database/student_data.json", "w") as f:
                json.dump(self.students, f, indent=4)
        except:
            print("Error occured")
        else:
            print("Saved succesfully")



