"""
Level 1 – Basic Filtering

Print all employee names.

Print employees whose department is Engineering.

Print employees with salary greater than 80,000.

Print employees whose age is less than 25.
"""

import json 

with open("company_data.json", "r") as f:
    data = json.load(f) # returns pytohn object dict.

print("\nemployee names : ")
for employee in data['employees']:
    print(employee['name'])

print("\nemployee names who are engineers : ")

for employee in data['employees']:
    if employee['department'] == 'Engineering':
        print(employee) 

print("\n\nemployee salary > 80000 : ")

for employee in data['employees']:
    if employee['salary'] > 80000:
        print(employee) 

print("\n\nemployee age < 25 : ")

for employee in data['employees']:
    if employee['age'] < 25:
        print(employee) 
           
"""
Level 2 – List Filtering

Print employees who know Python.

Print employees with more than 2 skills.

Print employees who worked on more than 1 project.
"""
print("\n\nemployee who knows python : ")
for employee in data['employees']:
    if 'Python' in employee['skills']:
        print(employee)


print("\n\nPrint employees with more than 2 skills")

for employee in data['employees']:
    if len(employee['skills']) > 2:
        print(employee)


print("\n\nPrint employees who worked on more than 1 project.")
for employee in data['employees']:
    if len(employee['projects']) > 1:
        print(employee)

"""
Level 3 – Nested Data

Print employees working on projects that are "in-progress".

Print employees who worked with AWS technology.

Print project names of Yash Chauhan.
"""

print("\n\nPrint employees working on projects that are in-progress")
for employee in data['employees']:
    for project in employee['projects']:
        if project['status'] == 'in-progress':
            print(employee)