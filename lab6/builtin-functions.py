#task1
from functools import reduce

def multiply_list(x,y):
    return x*y
#example
numbers = [2, 3, 4, 5]
red = reduce(multiply_list,numbers)
print("Product of all numbers:", red)

#task2
def up_low(s):
    uppers = 0
    lowers = 0
    for char in s:
        if char.isupper():
            uppers += 1
        elif char.islower():
            lowers += 1
    return  uppers,lowers

s = "Hello World!"
upper,lower = up_low(s)
print("Upper case letters:",upper,"Lower case letters:",lower)
#task3

def palindrome_check(s):
    if s==s[::-1]:
        return "It is palindrome"
    else:
        return "It is not palindrome"

print(palindrome_check("adam"))

#task4 
from math import sqrt
import time
number = int(input("Input number:"))
delay  = int(input("delay time:"))
start_time = time.perf_counter()
def fast_sqrt(number):
    return sqrt(number)

print("Square root of number:",fast_sqrt(number))
time.sleep(delay/1000)
end_time = time.perf_counter()
elapsed = end_time - start_time

print(f"Elapsed time after delay: {elapsed:.1f} seconds")
#task5
def all_true_elements(tpl):
    for i in tpl:
        if i!=True:
            return False
    return True

# Example usage
tuple1 = (True, True, True)
tuple2 = (True, False, True)

print(all_true_elements(tuple1))  # Output: True
print(all_true_elements(tuple2))  # Output: False
