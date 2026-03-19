from Services.student_manager import (StudentManager,
                                      StudentNotFoundError,
                                      )

import pytest

# ------------------------------------------------------------------


@pytest.fixture
def students():
    manager = StudentManager()
    return manager

# ------------------------------------------------------------------
# Testing Functionality
# ------------------------------------------------------------------

# testing Add Functionality


def test_add_search_student(students):
    students.add_student(1, "yash", [85,74,95])
    assert students.search_student("yash").name == "yash"


def test_add_same_rollno_students(students, capsys):
    students.add_student(1, "yash", [85,74,95])
    students.add_student(1, "rahul", [75,62,89])

    out = capsys.readouterr().out
    assert "this roll no. already exists" in out

def test_add_wrong_rollno(students, capsys):
    students.add_student("y", "yash", [85,41,23])
    out = capsys.readouterr().out
    assert "Roll no. Must be number and positive" in out

def test_add_same_name(students, capsys):
    students.add_student(1, "yash", [85,74,95])
    students.add_student(2, "yash", [75,62,89])

    out = capsys.readouterr().out
    assert "already exists" in out

def test_add_name_notstring(students, capsys):
    students.add_student(1, "785", [85,74,95])

    out = capsys.readouterr().out
    assert "name must be string" in out

def test_add_name_length(students, capsys):
    students.add_student(1, "yashpansuriyaisgoodmanandhonestabouthiswork", [85,74,95])

    out = capsys.readouterr().out
    assert "Length must be less than 20" in out

def test_add_same_rollno_students(students, capsys):
    students.add_student(1, "yash", [85,74,95])
    students.add_student(1, "rahul", [75,62,89])

    out = capsys.readouterr().out
    assert "this roll no. already exists" in out


def test_add_wrong_marks_length(students, capsys):
    students.add_student(1, "yash", [85,41,23,56])

    out = capsys.readouterr().out
    assert "Marks must be list of 3 subjects" in out

def test_add_wrong_marks_number(students, capsys):
    students.add_student(1, "yash", ["y","g",85])

    out = capsys.readouterr().out
    assert "Each mark must be between 0 and 100" in out

# ------------------------------------------------------------------
# Testing Deleting and Search Function
# ------------------------------------------------------------------


def test_delete_student(students):
    students.add_student(1, "yash", [85,74,95])
    students.delete_student("yash")

    with pytest.raises(StudentNotFoundError):
        students.search_student("yash")

def test_search_student_by_rollno(students):
    students.add_student(1, "yash", [85,74,95])
    assert students.search_student_by_roll_no(1).name == "yash"

# Not Found
def test_search_student_by_rollno_not_found(students):
    students.add_student(1, "yash", [85,74,95])

    with pytest.raises(StudentNotFoundError):
        students.search_student_by_roll_no(2)

def test_search_not_found(students):
    students.add_student(1, "yash", [85,74,95])

    with pytest.raises(StudentNotFoundError):
        students.search_student("rahul")


def delete_not_found(students):
    students.add_student(1, "yash", [85,74,95])

    with pytest.raises(StudentNotFoundError):
        students.delete_student("rahul")

# ------------------------------------------------------------------
# Testing Highest Marks and Update Marks
# ------------------------------------------------------------------

def test_highest_total_mark(students):
    students.add_student(1, "yash", [85,74,95])
    students.add_student(2, "rahul", [99,95,91])
    students.add_student(3, "diya", [42,74,80])
    students.add_student(4, "jain", [93,44,65])

    assert students.highest_total_mark_student().name == "rahul"

def test_highest_mark_by_subject(students):
    students.add_student(1, "yash", [85,74,95])
    students.add_student(2, "rahul", [99,95,91])
    students.add_student(3, "diya", [42,74,80])
    students.add_student(4, "jain", [93,44,65])

    assert students.highest_mark_by_subject(2).name == "yash"

def test_update_student_marks(students):
    students.add_student(1, "yash", [85,74,95])
    students.update_student_marks(1,98,1)

    assert students.search_student("yash").marks[1] == 98


