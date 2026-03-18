class Student:
    """
        Class that represent Student .

        Attributes :
            roll_num : unique id of student
            name : name of student .
            marks : marks of student . 0 to 100
    """

    SUBJECTS = ["Physics", "Chemistry", "Maths"]
    TOTAL_MAX_MARKS = 300


    def __init__(self, roll_num, name, marks):
        self.roll_num = roll_num
        self.name = name
        self.marks = marks
    
    # ------------------------------------------------------------------
    # Academic calculations
    # ------------------------------------------------------------------
    
    def get_grade(self):
        """
            It assigns grade accroding to marks
            of student.

            A  : 90 - 100
            B  : 75 - 89
            C  : 60 - 74
            D  : 34 - 59
            F  : 0  - 33
        """
        total_marks = sum(self.marks) / 3
        if total_marks <=100 and total_marks >= 90:
            return 'A'
        elif total_marks >=75 and total_marks < 90:
            return 'B'
        elif total_marks >=60 and total_marks < 75:
            return 'C'
        elif total_marks >=34 and total_marks < 60:
            return 'D'
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
        total_marks = sum(self.marks) / 300
        return (total_marks*4)


    def get_percentage(self):
        """
            returns overall percentage out of 100

            Formula: (sum of marks / total max marks) * 100
        """
        total_marks = (sum(self.marks) / self.TOTAL_MAX_MARKS)*100
        return total_marks

   
    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self):
        return {'roll_num':self.roll_num,
                'name': self.name,
                'marks': self.marks}
    
    
    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def __str__(self):
        return (      f"Roll no.     : {self.roll_num} \n"
                      f"Name         : {self.name} \n" 
                      f"Marks['Phy', 'Che.', 'Maths']: {self.marks} \n"
                      f"Percentage   : {self.get_percentage():.2f} % \n"
                      f"Grade        : {self.get_grade()} \n"
                      f"GPA          : {self.get_gpa():.2f} / 4.0 \n"
                )
    