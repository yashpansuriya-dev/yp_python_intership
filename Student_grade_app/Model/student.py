class Student:
    """
        Class that represent Student .

        Attributes :
            roll_num : unique id of student
            name : name of student .
            marks : marks of student . 0 to 100
        
        Methods :
            __str__ : represents as string
            to_dict : convert student to dictionary object.
    """
    def __init__(self, roll_num, name, marks):
        self.roll_num = roll_num
        self.name = name
        self.marks = marks
    
    def get_grade(self):
        """
            It assigns grade accroding to marks
            of student.
        """
        total_marks = sum(self.marks) / 3
        if total_marks <=100 and total_marks >= 90:
            return 'A'
        elif total_marks >=75 and total_marks < 90:
            return 'B'
        elif total_marks >=60 and total_marks < 75:
            return 'B'
        elif total_marks >=34 and total_marks < 60:
            return 'B'
        elif total_marks >=0 and total_marks < 34:
            return 'F'
        else:
            return 'Invalid Marks'
    
    def get_gpa(self) -> float:
        """
            returns GPA out of 10 .

            Formula :
                (obtained mark/ total marks )* 10 + 0.5
        """
        total_marks = sum(self.marks) / 30
        return (total_marks+0.5)

    def get_percentage(self):
        """
            returns percentage out of 100

            Formula :
                (obtained marks/total marks) *100
        """
        total_marks = sum(self.marks) / 3
        return total_marks

   
    
    def __str__(self):
        return (      f"Roll no.: {self.roll_num} |\n"
                      f"Name: {self.name} |\n" 
                      f"Marks['Phy', 'Che.', 'Maths']: {self.marks} |\n"
                      f"Percentage: {self.get_percentage():.2f} % |\n"
                      f"Grade: {self.get_grade()} |\n"
                      f"GPA: {self.get_gpa():.2f} | \n"
                )
                
    
    
    def to_dict(self):
        return {'roll_num':self.roll_num,
                'name': self.name,
                'marks': self.marks}