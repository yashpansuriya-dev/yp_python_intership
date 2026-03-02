'''
    Task - 3 : String
'''

import time

print("\n\n\nTask-3\n")
name = "Yash Pansuriya"

print(name.lower()) # Converts to Lower case
print(name.upper()) # Upper case
print(name.capitalize()) # Yash Pansuriya - like this 

print(name[2:7]) # includes 2 to 6 .
print(name[::-1]) # reverse string
print(name[-5:-2]) 
print(name[-2:-5:-1]) # -2 to -5 , with step -1


txt = "  Hello World "
print(txt.strip()) # removes whitespaces from start or end


names = name.split(" ") # returns list with splits with " "
for n in names:
    print(n)

newname = name.replace('a','x')    
print(newname)

# first occurence of word find
text = "i joined in Techforce Global as a python intern"
print("the first occurence of letter e is ", text.find('e'))

# count vowels
# vowel = ['a','e','i','o','u','A','E','I','O','U']
vowel = "aeiouAEIOU"
count=0
for n in "Yasheoh":
   if n in vowel:
       count = count+1

print("vowels in text are :",count)

#greeting and f-string
fullname = "Yash Pravinbhai Pansuriya"
f_name = fullname.split(" ")[0]
m_name = fullname.split(" ")[1]
l_name = fullname.split(" ")[2]
print(f"full name is , {l_name} {f_name} {m_name}")
print(f"hello ! , {f_name} {l_name}")


#time with fstring
ctime = time.ctime()
times = ctime.split(" ")
print(f"Todays is {times[2]} {times[1]} and {times[0]} and year is {times[3]} ")

t = times[4].split(":")
print(f"currently hour is {t[0]} , minute is {t[1]} , and second is {t[2]}")

