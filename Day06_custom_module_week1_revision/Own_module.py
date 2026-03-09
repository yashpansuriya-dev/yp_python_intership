import Utils
from Utils import generate_password, format_date
from datetime import datetime


print("\nYour Password is : ",generate_password(10))
print("\nFormatted Date is : ",format_date(datetime.now()))

print("\nis Even : ",Utils.is_even(10))

print("\n10 / 0 is : ",Utils.safe_divide(10,0))

print("\nYour Unique list is : ",Utils.unique_list([1,2,2,4,5,5,6,8,8,8,]))
print("Hello")

print()

