# 🎓 Student Grade App

## 🚀 About
A simple Python console application to manage student records and grades.  
This app allows you to add, delete, search, and list students, as well as calculate grades based on marks.

## 🛠 Tech Stack
- Python
- File Handling / In-Memory Storage
- Pytest for testing

## ✨ Features
- ➕ **Add Student**: Insert a new student with name and marks.
- ❌ **Delete Student**: Remove a student by name or ID.
- 🔍 **Search Student**: Find a student’s details quickly.
- 📊 **List Students**: Display all students with their marks and grades.
- 🏆 **Fetch Highest Marks**: Identify the top scorer.
- 🧮 **Calculate Grade**: Convert marks into grades (A, B, C, etc.).

## 🛠️ Installation
1. Clone this repository :

```bash
   git clone https://github.com/yashpansuriya-dev/yp_python_intership/tree/main/Student_grade_app
```

2. Navigate to the project folder:

```bash
    cd student-grade-app
```
3. Run the App

```bash
    python student_grade_app.py
```

## 📖 Usage
When you run the app, you’ll see a menu like this:

Code
```
1. Add Student
2. Delete Student
3. Search Student
4. List Students
5. Fetch Highest Marks
6. Exit
```
Choose an option by entering the corresponding number.
Grades are calculated automatically based on marks.

## 🧮 Grading System

| Marks Range | Grade |
|-------------|-------|
|    90-100   |   A   |
|    75-89    |   B   |
|    60-74    |   C   |
|    40-59    |   D   |
|   Below 40  |   F   |
|    90-100   |   A   |

<!-- ## 📸 Screenshots -->
<!-- ![Screenshot1](class_diagram.png) -->

## 📁 Project Structure
    Student_grade_app/
    │── main.py
    │── Database
        │── student_data.json
    │── Model
        │── student.py
    │── Services
        │── student_manager.py
    │── Test
        │── test_student_manager.py
    │── README.md

## 📂 Example
```
Enter choice: 1
Enter student name: Alice
Enter marks: 85
Student added successfully!

Enter choice: 4
Name: Alice | Marks: 85 | Grade: B
```

## 🚀 Future Enhancements
- Save student data to a file (CSV/JSON).
- Add update functionality for marks.
- Support multiple subjects per student.

## 🤝 Contributing
Contributions are welcome!
Feel free to fork this repo and submit a pull request.

## 📄 License
This project is licensed under the MIT License.

## 👨‍💻 Author
 Yash Pansuriya