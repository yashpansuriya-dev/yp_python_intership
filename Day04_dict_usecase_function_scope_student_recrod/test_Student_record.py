import pytest

from Student_record import (
    student_add,
    student_del,
    student_list,
    student_search,
    highest_marks
)

# ------------------------------------------------------------------

@pytest.fixture
def stu_record():
    return []


# Testing student_add function
def test_student_add(stu_record):
    student_add(1, "yash", 85, stu_record)

    assert len(stu_record) == 1
    assert stu_record[0]['name'] == "yash"
    assert stu_record[0]['marks'] == 85


def test_student_add_multiple(stu_record):
    student_add(1, "yash", 85, stu_record)
    student_add(2, "rahul", 90, stu_record)
    student_add(3, "vinay", 74, stu_record)
    student_add(4, "brijraj", 76, stu_record)

    assert len(stu_record) == 4


# Testing student_delete function
def test_student_del(stu_record):
    student_add(1, "yash", 85, stu_record)
    student_del("yash", stu_record)

    assert student_search("yash", stu_record) == None
    assert len(stu_record) == 0


def test_student_delete_not_exist(stu_record):
    student_add(1, "yash", 85, stu_record)
    deleted = student_del("rahul", stu_record)

    assert deleted is None
    assert len(stu_record) == 1


# Testing student_search function
def test_student_search(stu_record):
    student_add(1, "yash", 85, stu_record)
    student = student_search("yash",stu_record)

    assert student['name'] == "yash"


def test_student_search_not_found(stu_record):
    student_add(1, "yash", 85, stu_record)

    assert student_search("rahul", stu_record) is None


# Testing student_list function
def test_student_list(stu_record):
    student_add(1, "yash", 95, stu_record)
    student_add(2, "rahul", 80, stu_record)

    assert student_list(stu_record) != None


def test_student_list_empty(stu_record):
    assert student_list(stu_record) == None


# Testing student Highest mark function
def test_student_highest_mark(stu_record):
    student_add(1, "yash", 85, stu_record)
    student_add(2, "nigam", 10, stu_record)
    student_add(3, "rahul", 58, stu_record)

    highest_student = highest_marks(stu_record)

    assert highest_student['name'] == "yash"
    assert highest_student['marks'] == 85


def test_highest_mark_empty(stu_record):
    highest_student = highest_marks(stu_record)

    assert highest_student is None


# ------------------------------------------------------------------






