import pytest 
from Model.student import Student

# ------------------------------------------------------------------

@pytest.fixture
def student():
    student = Student(1,"yash",[98,74,96])
    return student

# ------------------------------------------------------------------

def test_get_grade(student):
    assert student.get_grade() == "B"

def test_get_percentage(student):
    assert student.get_percentage() == 89.33333333333333

def test_get_gpa(student):
    assert student.get_gpa() == 3.5733333333333333

