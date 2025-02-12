#task1
class SquareGenerator: 
    def __init__(self,n): 
        self.n = n 
        self.a = 1 
    def __iter__(self): 
        return self 
    def __next__(self): 
            x = self.a 
            self.a +=1 
            return x**2 
 
n = int(input("Number: ")) 
myclass = SquareGenerator(n) 
myiter = iter(myclass) 
for i in range(1,n+1): 
    print(next(myiter))

#task2
def even_numbers(n): 
    for i in range(n + 1): 
        if i % 2 == 0: 
            yield i 
n = int(input("Enter number: ")) 
even_numbers(n) 
print(', '.join(map(str,even_numbers(n))))

#task3
def divisible(n): 
    for i in range(n + 1): 
        if i % 3==0 and i % 4 == 0: 
            yield i 
n = int(input("Enter number: ")) 
divisible(n) 
print(', '.join(map(str,divisible(n))))

#task4
def squaress(a,b):
    for i in range(a,b+1):
        yield i**2

a = 2
b = 10
for i in squaress(a,b):
    print(i)

#task5
def to_down(number):
    while number>0:
        yield (number)
        number -= 1

for number in to_down(5):
    print(number)