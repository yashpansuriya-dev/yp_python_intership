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
    
    def __str__(self):
        return f"Roll no.: {self.roll_num} Name: {self.name} | Marks: {self.marks} | Grade: {self.get_grade()}"
    
    def to_dict(self):
        return {'roll_num':self.roll_num,
                'name': self.name,
                'marks': self.marks}