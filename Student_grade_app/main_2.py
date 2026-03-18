from Services.student_manager_2 import StudentManager, StudentNotFoundError

SUBJECTS = ["Physics", "Chemistry", "Maths"]

# ------------------------------------------------------------------
# Safe input helpers — format/range only, no business logic
# ------------------------------------------------------------------

def safe_int_input(prompt: str) -> int:
    """Keep prompting until the user enters a valid positive integer."""
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("  Please enter a positive number.")
        except ValueError:
            print("  Please enter a whole number (no letters or symbols).")


def safe_name_input(prompt: str) -> str:
    """
    Keep prompting until the user enters a valid name.
    Rules: letters only, non-empty, max 20 characters.
    Does NOT check duplicates — that is done separately via manager.
    """
    while True:
        name = input(prompt).strip()
        if not name:
            print("  Name cannot be empty.")
        elif not name.isalpha():
            print("  Name must contain letters only (no numbers or symbols).")
        elif len(name) > 10:
            print("  Name must be 10 characters or fewer.")
        else:
            return name


def safe_marks_input(prompt: str) -> int:
    """Keep prompting until the user enters an integer between 0 and 100."""
    while True:
        try:
            mark = int(input(prompt))
            if 0 <= mark <= 100:
                return mark
            print("  Please enter a value between 0 and 100.")
        except ValueError:
            print("  Please enter a whole number.")


def safe_subject_input() -> int:
    """Keep prompting until the user picks a valid subject index (0/1/2)."""
    print("  0. Physics")
    print("  1. Chemistry")
    print("  2. Maths")
    while True:
        try:
            idx = int(input("  Enter subject number: "))
            if idx in (0, 1, 2):
                return idx
            print("  Please enter 0, 1, or 2.")
        except ValueError:
            print("  Please enter a number.")


# ------------------------------------------------------------------
# Menu
# ------------------------------------------------------------------

def menu():
    manager = StudentManager()

    while True:
        print("\n--- Student Grade App ---")
        print(" 1.  Add Student")
        print(" 2.  Delete Student")
        print(" 3.  Search Student by Name")
        print(" 4.  Search Student by Roll Number")
        print(" 5.  List Students")
        print(" 6.  Highest Total Marks")
        print(" 7.  Highest Marks by Subject")
        print(" 8.  Student Overall Result")
        print(" 9.  Update Marks")
        print(" 10. Save to JSON")
        print(" 11. Load from JSON")
        print(" 12. Top Performers")
        print(" 0.  Exit")

        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("  Please enter a number.")
            continue

        # ── Add Student ──────────────────────────────────────────────
        if choice == 1:

            # Step 1: get roll number and check duplicate IMMEDIATELY
            roll_num = safe_int_input("  Roll number: ")
            if manager.is_roll_exists(roll_num):
                print(f"  [Error] Roll number {roll_num} already exists.")
                continue                          # ← go back to menu, skip name/marks

            # Step 2: get name and check duplicate IMMEDIATELY
            name = safe_name_input("  Name: ")
            if manager.is_name_exists(name):
                print(f"  [Error] Student '{name}' already exists.")
                continue                          # ← go back to menu, skip marks

            # Step 3: only ask marks if roll and name are both valid
            marks = [
                safe_marks_input(f"  Mark for {subj} (0-100): ")
                for subj in SUBJECTS
            ]
            manager.add_student(roll_num, name, marks)

        # ── Delete Student ───────────────────────────────────────────
        elif choice == 2:
            name = safe_name_input("  Name to delete: ")
            confirm = input(f"  Are you sure you want to delete '{name}'? (y/n): ").strip().lower()
            if confirm == "y":
                manager.delete_student(name)
            else:
                print("  Deletion cancelled.")

        # ── Search by Name ───────────────────────────────────────────
        elif choice == 3:
            name = safe_name_input("  Name to search: ")
            try:
                print(manager.search_student(name))
            except StudentNotFoundError as e:
                print(f"  [Error] {e}")

        # ── Search by Roll Number ────────────────────────────────────
        elif choice == 4:
            roll_no = safe_int_input("  Roll number to search: ")
            try:
                print(manager.search_student_by_roll_no(roll_no))
            except StudentNotFoundError as e:
                print(f"  [Error] {e}")

        # ── List Students ────────────────────────────────────────────
        elif choice == 5:
            manager.list_students()

        # ── Highest Total Marks ──────────────────────────────────────
        elif choice == 6:
            try:
                student = manager.highest_total_mark_student()
                print(f"\n  Highest total: {student.name} with {sum(student.marks)} / 300 marks.")
            except ValueError as e:
                print(f"  [Error] {e}")

        # ── Highest Marks by Subject ─────────────────────────────────
        elif choice == 7:
            idx = safe_subject_input()
            try:
                student = manager.highest_mark_by_subject(idx)
                print(f"\n  Highest in {SUBJECTS[idx]}: {student.name} with {student.marks[idx]} / 100.")
            except ValueError as e:
                print(f"  [Error] {e}")

        # ── Student Overall Result ───────────────────────────────────
        elif choice == 8:
            name = safe_name_input("  Name: ")
            try:
                print(manager.search_student(name))
            except StudentNotFoundError as e:
                print(f"  [Error] {e}")

        # ── Update Marks ─────────────────────────────────────────────
        elif choice == 9:
            roll_num = safe_int_input("  Roll number: ")
            if not manager.is_roll_exists(roll_num):          # ← early check
                print(f"  [Error] No student with roll number {roll_num}.")
                continue
            idx = safe_subject_input()
            new_mark = safe_marks_input(f"  New mark for {SUBJECTS[idx]} (0-100): ")
            manager.update_student_marks(roll_num, new_mark, idx)

        # ── Save to JSON ─────────────────────────────────────────────
        elif choice == 10:
            manager.save_to_json()

        # ── Load from JSON ───────────────────────────────────────────
        elif choice == 11:
            manager.load_from_json("Database/student_data.json")

        # ── Top Performers ───────────────────────────────────────────
        elif choice == 12:
            manager.top_performers()

        # ── Exit ─────────────────────────────────────────────────────
        elif choice == 0:
            print("  Goodbye!")
            break

        else:
            print("  Invalid choice — please try again.")


def main():
    try:
        menu()
    except KeyboardInterrupt:
        print("\n\n  Interrupted. Goodbye!")


if __name__ == "__main__":
    main()
