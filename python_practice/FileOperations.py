#File I/O > means reading data from files and writing data to files

#files are useful when we want to store data permanently instead of keeping it only in memory

file=open("notes.txt","r")

content=file.read()

file.readline() #Read one line
file.readlines()
file.close()

print(content)

#For appending content to a file
file=open("notes.txt","a")
file.write("\nHello Python\n")
file.close()


#For writing content to a file
file=open("notes.txt","w")
file.write("\nwriting Hello Python\n")
file.close()


#modes
# "r"
# "w"
# "a"
# "x" > creates a new file, fails if file exists
# "rb" > read binary
# "wb" > write binary

# file=open("image.png","rb")
# data=file.read()
# file.close()

#with statement automatically closes after the file use

with open("notes.txt","r",encoding="utf-8") as file:
    content = file.read()

print(content)

with open("notes.txt","w",encoding="utf-8") as file:
    file.write("Learning file I/O in python")

print(content)

#os.path > helps us work with file and folder paths

import os
path="notes.txt"

print(os.path.exists(path))
print(os.path.abspath(path))

file_path=os.path.join("data","notes.txt")
print(file_path)

#pathlib > modern and cleaner way to work with file paths in python.
#it treats path like objects, so the code becomes easier to understand

from pathlib import Path
path= Path("notes.txt")
print(path.exists())
print(path.absolute())

content = path.read_text(encoding = "utf-8")
print(content)


#Standard Streams > python has three standard streams that handle input, output and errors

#stdin > standard input
#stdout > standard output
#stderr > standard error

#stdin > standard input

name=input("enter your name: ")
print(name)

import sys
data=sys.stdin.readlines()
print(data)

#stdout
print("this is the output")
sys.stdout.write("Hello from std output\n")

#stderr

sys.stderr.write("This is an error msg")

#Serialization

#Converting python data into a format that can be saved in a file or transferred over a network

Student ={
    "name":"Abhishek",
    "age":26
}

#json > readable text format
#csv > tabular data format
#pickle > python specific binary format

#json
import json
with open("student.json","w",encoding="utf-8") as file:
    json.dump(Student,file)

with open("student.json","r",encoding="utf-8") as file:
    data=json.load(file)

print(data)

#csv

import csv

students=[
    ["name","age"],
    ["abhishek",26],
    ["aniket",25]
]

with open("students.csv","w",newline="",encoding="utf-8") as file:
    writer=csv.writer(file)
    writer.writerows(students)

with open("students.csv","r",encoding="utf-8") as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)

#Pickle

import pickle

student={
    "name":"Abhishek",
    "age": 26
}

with open("student.pkl","wb") as file:
    pickle.dump(student, file)

with open("student.pkl","rb") as file:
    data=pickle.load(file)

print(data)