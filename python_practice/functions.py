def greet():
    print("hello world")

greet()

#positional arguments are passed based on the order of parameters in the function

def introduce(name,age):
    print(f"{name} is {age} years old")

introduce("abhishek",26)

#keyword arguments passed using parameter names, so the order does not matter

introduce(age=26,name="hrithik")

#Default arguments are used when no value is passed for a parameter

def greet(name="Student"):
    print(f"Hello, {name}")

greet()

# *args allows a function to accept any number of positional arguments. It stores them as a tuple

def add_numbers(*args):
    return sum(args)

print(add_numbers(10,20,30))
print(add_numbers(10,20,30,40))


# **kwargs allows a function to accept any number of keyword arguments. It stores them as a dictionary

def show_profile(**kwargs):
    print(kwargs)

show_profile(name="abhishek",age=26,gender="M")

#the return keyword sends a value back from a function to the place where it is called

def calculate(a,b):
    return a+b,a-b,a*b

add, sub, mul=calculate(10,5)
print(add,sub,mul)

#Scope

#Local > A variable created inside a funcn is local and can only be used inside that function

def greet():
    message="Hello"
    print (message)

#Global > A variable created outside all funcns is global and can be accessed inside funcns

name="abhishek"

def greet():
    print(name)

#global keyword is used when we want to modify a global variable inside a funcn

count=0

def increment():
    global count
    count+=1

#nonlocal keyword is used in nested functions to modify a variable from outer function

def outer():
    count=0

    def inner():
        nonlocal count
        count+=1

#Lambda Expressions > are small anonymous functions used for short one-line operations

square = lambda x: x*x
print(square(3))

#Docstrings > used to describe what a funcn does. They are usually written inside triple quotes

def add(a,b):
    """
    Adds two numbers and return result

    """

    return a+b

# Type annotations > describe the expected input and output types of a funcn

def add(a: int,b: int) -> int:
    return a+b

