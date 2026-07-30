#Strings

#String is a sequence of characters used to store text

name="Algocamp"
message="Python is fun"

#Strings are immutable, meaning they cannot be changed directly after creation

s1='hello'
s2="Hello"
s3="""This is a multiline string"""

sentence="I'm learning Python"

quote='He said, "Python is easy"'

text="Python"

#strings are indexed from 0

print(text[0])
print(text[-1])


print(text[0:3]) #Pyt
print(text[:4]) #Pyth
print(text[2:]) #thon
print(text[::-1]) #nohtyp

#slicing does not modify the original 

name= "python programming"

print(name.upper())
print(name.capitalize()) #makes only the first character of entire string uppercase
print(name.title()) #first character of every word uppercase.

text= "I love Python"
print(text.find("Python")) #indexing output
print("Python" in text) #boolean output

email = " test@gmail.com "

print(email.strip())

sentence="Python is powerful"

words = sentence.split()
print(words)

joined="-".join(words)
print(joined)

text="I like Java"
print(text.replace("java","Python")) #Kind of replace all

#String formatting 

name = "Abhishek"
age = 26

print(f"My name is {name} and I am {age} years old.")

print("My name is {} and I am {} years old.".format(name,age))

print("My name is %s and I am %d years old" % (name,age))

message="""Hello,
Welcome to Python Strings.
Let's Learn!"""

#use raw strings when working with file paths or regular expressions
path=r"C:\Users\Abhishek\Documents"
print(path)

#Escape Sequences

print("Hello\nWorld")
print("Hello\tWorld")
print("She said, \"Python is easy\"")
print("C:\\Users\\Abhishek")

# \n > newline
# \t > tab
# \\ backslash
# \" double quote
# \' single quote

#Python strings support unicode by default

text= "Hello ☺️"
print(text)

print(ord("A"))
print(chr(65))

#python string > bytes using UTF-8 encoding

text="Python" #normal string #type > str
encoded = text.encode("utf-8")

print(encoded) #output b'Python' > the b before the python means this is a python object, not a normal string

text= "Hello ☺️"
encode = text.encode("utf-8")

print(encode)
print(encode.decode())

