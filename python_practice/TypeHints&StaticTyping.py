#Type Hints

#Type hints allows us to mention the expected type of variables, function parameters and return values.

#Python is still dynamically typed, so type hints do not enforce types at runtime by default.

def greet(name: str) -> str:
    return f"Hello, {name}"

message=greet("abhishek")

print(message)

name: str = "Abhishek"
age: int = 25
height: float = 5.3

marks: int = "ninety"

def add(a :int, b: int):
    return a+b

result=add(10,20)
print(result)

def print_message(message: str) -> None:
    print(message)

#The typing module

#provides many useful types for writing better type hints

from typing import Optional, Union, Any

#Generics: list[T]

#Generics allows us to mention what type of data a collection contains

numbers: list[int] = [1,2,3,4]
names: list[str] = ["Abhishek","Aniket"]

def total(numbers: list[int]) -> int:
    return sum(numbers)

print(total([10,20,30]))

#Generics: dict[K,V]

student: dict[str,int] = {
    "math":90,
    "science":85
}

def print_scores(scores: dict[str,int]) -> None:
    for subject, marks in scores.items():
        print(subject, marks)

coordinates: tuple[int,int] = (10,20)
unique_numbers: set[int] = {1,2,3}

#Optional is used when a value can either be of a specific type or None.

from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Abhishek"
    return None

def find_user(user_id: int) -> str | None:
    if user_id == 1:
        return "Abhishek"
    return None

#Union is used when a value can be one of the multiple types

from typing import Union

def format_id(user_id: Union[int,str]) -> str:
    return f"User-{user_id}"

def format_id(user_id: int | str) -> str:
    return f"User-{user_id}"

#Any

#Any means the value can be of any type

from typing import Any

def print_value(value: Any) -> None:
    print(value)

data: Any = "Python"
data = 120
data = True

#TypedDict is used to define the expected structure of a dictionary

from typing import TypedDict

class Student(TypedDict):
    name:str
    age:int
    course:str

student: Student = {
    "name" : "abhishek",
    "age": 26,
    "course": "Python"
}

def print_student(student: Student) -> None:
    print(student["name"])
    print(student["course"])


from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None:
        ...

class Circle:
    def draw(self) -> None:
        print("Drawing circle")

class Square:
    def draw(self) -> None:
        print("Drawing Square")

def render(shape: Drawable) -> None:
    shape.draw()

render(Circle())
render(Square())

#Static type checking means checking type errors before running the program

def add(a: int, b: int) -> int:
    return a+b

add("10","20")

# we can install static type checker like mypy using pip
# To check we need to run mypy followed by filename
#we can install pyright using npm install -g pyright