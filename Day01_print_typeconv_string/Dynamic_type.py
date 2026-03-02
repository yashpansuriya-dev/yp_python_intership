'''
    Task 2 - dynamic type 
'''
a =5
print(type(a))

a="yash pansuriya" # ' a ' is changed from 'int' to 'string' .
print(type(a))

a=8.5 # to float
print(type(a))

b=None 
print(type(b))

a=True # to bool
print(type(a))

a=0

b = int(a) #9.8 converted to 9
print(b)

c = bool(b) # 9 Converted to True , if 0 -> False
print(c)

d = int(c) # True -> 1 , False -> 0
print(d)

name="Yash Pansuriya"
cgpa = 8.6
passing = True
marks = 81

# Using Format string
print(f"hi , my name is {name} , and i am doing my final year from vgec college and i got {marks} in last semester , so my overall cgpa is {cgpa} , so i am {"passed" if passing else "failed"} ")
