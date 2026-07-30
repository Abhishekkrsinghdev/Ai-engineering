#Exception
#Exception are errors that occur while the program is running.
#If they are not handled, the program stops execution

# num=int('abc')

#ValueError
#FileNotFoundError
#IndexError
#KeyError
#TypeError
#ZeroDivisionError

#Traceback

#A traceback shows where the error happened and what type of error occured

# def divide(a,b):
#     return a/b

# divide(10,0)

#try and except

#try is used to write risky code. except handles the error if something goes wrong.


# try:
#     num=int(input("Enter a number: "))
#     print(num)
# except ValueError:
#     print("Invalid input. Please enter a number")
# else:
#     print("Conversion successful: ",num)
# finally:
#     print("This always runs")

#Broad exception catches almost every error

# try:
#     result=10/0
# except Exception as e:
#     print("Error: ",e)

#Raising a exception

# def withdraw(balance,amount):
#     if amount > balance:
#         raise ValueError("Insufficient Balance")
#     return balance - amount

# print(withdraw(1000,1500))

#Custom Exception helps us to create meaningful errors for our own app

# class InsufficientBalanceError(Exception):
#     pass

# def withdraw(balance,amount):
#     if amount > balance:
#         raise InsufficientBalanceError("Not enough balance")
#     return balance - amount

# try:
#     withdraw(1000,1500)
# except InsufficientBalanceError as e:
#     print(e)

#Exception chaining is used when one exception happens because of another exception

def convert_to_int(value):
    try:
        return int(value)
    except ValueError as e:
        raise ValueError("Failed to convert value to integer") from e

convert_to_int("abc")

#finally

#finally > cleanup

file=None

try:
    file=open("data.txt","r")
    content=file.read()
except FileNotFoundError:
    print("File not found")
finally:
    if file:
        file.close()