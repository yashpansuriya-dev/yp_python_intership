import json
from Model.student import Student

# ------------------------------------------------------------------
# Custom Exceptions
# ------------------------------------------------------------------

class InputValidationError(Exception):
    pass

class StudentNotFoundError(Exception):
    pass

# ------------------------------------------------------------------
# Student Manager
# ------------------------------------------------------------------

class StudentManager:

    def __init__(self):
        self.students = []

    # ------------------------------------------------------------------
    # Public duplicate checks
    # Called by main.py IMMEDIATELY after roll/name is entered,
    # so the user is not asked unnecessary questions first.
    # ------------------------------------------------------------------

    def is_roll_exists(self, roll_num: int) -> bool:
        """Returns True if roll number is already taken."""
        return any(s.roll_num == roll_num for s in self.students)

    def is_name_exists(self, name: str) -> bool:
        """Returns True if name is already taken (case-insensitive)."""
        return any(s.name.lower() == name.strip().lower() for s in self.students)

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def add_student(self, roll_num: int, name: str, marks: list):
        try:
            self._validate_roll(roll_num)
            self._validate_name(name)
            self._validate_marks(marks)
        except InputValidationError as e:
            print(f"  [Validation Error] {e}")
            return
        self.students.append(Student(roll_num, name, marks))
        print(f"  Student '{name}' added successfully.")

    def search_student(self, name: str):
        for student in self.students:
            if student.name.lower() == name.lower():
                return student
        raise StudentNotFoundError(f"No student found with name '{name}'.")

    def search_student_by_roll_no(self, roll_no: int):
        for student in self.students:
            if student.roll_num == roll_no:
                return student
        raise StudentNotFoundError(f"No student found with roll number {roll_no}.")

    def list_students(self):
        if not self.students:
            print("  No students added yet.")
            return
        for student in self.students:
            print(student)

    def delete_student(self, name: str):
        try:
            student = self.search_student(name)
            self.students.remove(student)
            print(f"  Student '{name}' deleted successfully.")
        except StudentNotFoundError as e:
            print(f"  [Error] {e}")

    # ------------------------------------------------------------------
    # Academic
    # ------------------------------------------------------------------

    def highest_total_mark_student(self):
        if not self.students:
            raise ValueError("No students available.")
        return max(self.students, key=lambda s: sum(s.marks))

    def highest_mark_by_subject(self, idx: int):
        if not self.students:
            raise ValueError("No students available.")
        return max(self.students, key=lambda s: s.marks[idx])

    def top_performers(self):
        performers = [s for s in self.students if s.get_gpa() >= 3.5]
        if not performers:
            print("  No top performers found (GPA >= 3.5).")
            return
        print("\n  Top Performers (GPA >= 3.5):")
        for s in performers:
            print(s)

    def update_student_marks(self, roll_num: int, new_mark: int, idx: int):
        try:
            student = self.search_student_by_roll_no(roll_num)
            student.marks[idx] = new_mark
            print("  Marks updated successfully.")
        except StudentNotFoundError as e:
            print(f"  [Error] {e}")

    # ------------------------------------------------------------------
    # JSON
    # ------------------------------------------------------------------

    def save_to_json(self):
        try:
            data = [s.to_dict() for s in self.students]
            with open("./Database/student_data.json", "w") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"  [File Error] {e}")
        else:
            print("  Saved successfully.")

    def load_from_json(self, filename):
        self.students.clear()
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            for d in data:
                self.students.append(Student(d['roll_num'], d['name'], d['marks']))
        except FileNotFoundError:
            print(f"  [Error] File not found: '{filename}'.")
        except (IOError, json.JSONDecodeError) as e:
            print(f"  [File Error] {e}")
        else:
            print("  Data loaded successfully.")

    # ------------------------------------------------------------------
    # Private validators
    # These only validate FORMAT and RANGE.
    # Duplicate checks happen in main.py via is_roll_exists()
    # and is_name_exists() BEFORE the user is asked further questions.
    # ------------------------------------------------------------------

    def _validate_roll(self, roll_no: int):
        """Roll must be a positive integer and not already taken."""
        if not isinstance(roll_no, int) or roll_no <= 0:
            raise InputValidationError("Roll number must be a positive integer.")
        if self.is_roll_exists(roll_no):
            raise InputValidationError(f"Roll number {roll_no} already exists.")

    def _validate_name(self, name: str):
        """Name must be letters only, non-empty, max 20 chars, and not already taken."""
        if not isinstance(name, str) or not name.strip():
            raise InputValidationError("Name cannot be empty.")
        if not name.strip().isalpha():
            raise InputValidationError("Name must contain letters only (no numbers or symbols).")
        if len(name.strip()) > 20:
            raise InputValidationError("Name must be 20 characters or fewer.")
        if self.is_name_exists(name):
            raise InputValidationError(f"Student '{name}' already exists.")

    def _validate_marks(self, marks: list):
        """Marks must be a list of exactly 3 numbers each between 0 and 100."""
        if not isinstance(marks, list) or len(marks) != 3:
            raise InputValidationError("Marks must be a list of exactly 3 subjects.")
        for m in marks:
            if not isinstance(m, (int, float)) or not (0 <= m <= 100):
                raise InputValidationError(f"Each mark must be between 0 and 100 (got {m}).")
