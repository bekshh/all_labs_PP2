#task1
import math
def to_radiance(number):
    x = math.pi
    return number * (x / 180)

print(to_radiance(15))

#task2
def area_of_trapezoid(height,a,b):
    return (a+b)*height/2
print(area_of_trapezoid(5,5,6))
#task3
def regular_area(sides,length):
    area = (sides * length**2) / (4 * math.tan(math.pi / sides))
    return (f"{area:.0f}")
print(regular_area(4,25))
#task4
def area_of_parallelogram(base,heihgt):
    return base * heihgt
    