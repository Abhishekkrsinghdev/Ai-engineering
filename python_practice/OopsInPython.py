#Object Oriented Programming

#It is a way of organising code around objects

#An object represents a real-world entity that has

#Attributes > data/properties > store data about an object

#Methods > behaviour/actions > are functions defined inside a class

class Student:
    pass

student1=Student()

#Classes > is a blueprint
#An object is an actual instance created from that blueprint

class Student:

    #__init__ is a special method that runs automatically when a obejct is created.
    # def __init__(self,name,age):
    #     self.name=name
    #     self.age=age

    def set_name(self,name):
        self.name=name

    def introduce(self):
        print(f"Hello I am a {self.name} and I am {self.age} years old")

# student1=Student("Abhishek",26)
# student1.introduce()

student1=Student()
student1.set_name("abhishek")

print(student1.name)

#self > refers to the current object


#Instance attributes vs class attributes

#IA > belongs to individual objects
#CA > shared by all the objects of a class

class Student:
    school="st.karen's"

    def __init__(self,name):
        self.name=name

student1=Student("abhishek")
student2=Student("aniket")

print(student1.name)
print(student2.name)

print(student1.school)
print(student2.school)

#Method Overriding

#Method overriding means a class provide its own version of a method already defined in parent class

class Animal:
    def sound(self):
        print("Animal makes a sound")

class Dog(Animal):
    def sound(self):
        print("Dog barks")

dog=Dog()
dog.sound()

#super()

#super() is used to call methods from the parent class

class Person:
    def __init__(self,name):
        self.name=name
    
class Student(Person):
    def __init__(self,name,course):
        super().__init__(name)
        self.course=course
    def __str__(self):
        return f"Student name is {self.name}"

student1=Student("abhishek","Python")
print(student1)
print(student1.name)
print(student1.course)


#Encapsulation

class BankAccount:
    def __init__(self,balance):
        self._balance=balance

    def get_balance(self):
        return self._balance

# _name     -> Protected by convention (meant for internal use)
# __name    -> Name mangling (makes accidental access harder, not truly private)
# name      -> Public attribute
# Python uses conventions and name mangling, not true private members.

#Dunder/magic methods

#special methods that start and end with double underscores

#__init__
#__str__
#__len__
#__eq__
#__add__

class Course:
    def __init__(self,students):
        self.students=students

    def __len__(self):
        return len(self.students)

course = Course(["abhishek","aniket","arjun"])

print(len(course))

class Student:
    def __init__(self,marks):
        self._marks=marks
    
    @property
    def marks(self):
        return self._marks

    @marks.setter
    def marks(self,value):
        if value < 0:
            raise ValueError("Marks cannot be negative")
        self._marks=value

student1=Student(90)
print(student1.marks)
student1.marks = 95
print(student1.marks)

class Student:
    school="Algocamp"

    def __init__(self,name):
        self.name=name
        
    @classmethod
    def change_school(cls,new_school):
        cls.school=new_school

Student.change_school("Algocamp pro")

student1=Student("abhishek")
print(student1.school)

#Static methods > utility methods inside a class for logical grouping

class MathUtils:
    @staticmethod
    def add(a,b):
        return a+b

print(MathUtils.add(10,20))

#Dataclasses > help us create classes mainly used for storing data

#They reduce boilerplate code like writing __init__ manually.

from dataclasses import dataclass

@dataclass
class Student:
    name:str
    age:int
    course:str="Python"

student1=Student("Abhishek",26)
print(student1)

