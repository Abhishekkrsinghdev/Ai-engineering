#Iterables > An iterable in any object that can be looped over using a for loop

numbers=[1,2,3]
name="Python"
student={"name":"Abhishek","age":26}

for item in numbers:
    print(item)

# list, tuple, string, dictionary

#Iterables vs Iterators

#An iterator is the actual object that gives values one by one.

numbers=[10,20,30]

iterator = iter(numbers)

print(next(iterator))
print(next(iterator))
print(next(iterator))

#__iter__() > return iterator object
#__next__() > return the next value

numbers = [10,20,30]
iterator=iter(numbers)

print(iterator.__next__())
print(iterator.__next__())

#StopIteration is triggered if there are no more values

#Generators > are a simple way to create iterators

def count_up_to(limit):
    current=1

    while current <= limit:
        yield current
        current+=1

for num in count_up_to(3):
    print(num)

# why to use generators because they are memory efficient they produce one value at a time

def simple_generator():
    yield 1
    yield 2
    yield 3

gen=simple_generator()

print(next(gen))
print(next(gen))
print(next(gen))

#Generator Expressions

#Typical way
squares = [x*x for x in range(5)]
print(squares)

#using generator expressions

squares=(x*x for x in range(5))
print(squares)
print(next(squares))
print(next(squares))

#map() > applies a function to every item in an iterable

numbers = [1,2,3,4]

squares = map(lambda x:x*x,numbers)
print(list(squares))


#filter() keeps only the items that match a condition

numbers=[1,2,3,4,5,6]
even_numbers = filter(lambda x:x %2 == 0, numbers)

print(list(even_numbers))

#reduce()

from functools import reduce

numbers=[1,2,3,4]

product=reduce(lambda a,b: a*b, numbers)

print(product)

#functional programming

#functions can be stored in variables passed as arguments returned from other functions used inside data transformation

def sq(x):
    return x*x

operation = sq

print(operation(5))

#HOF(Higher order funcn)

def apply_operation(func,value):
    return func(value)

def sq(x):
    return x*x

print(apply_operation(sq,5))

#Closures > a closure is when an inner funcn remembers variables from the outer funcn even after the outer funcn is finished

def multiplier(factor):
    def multiply(number):
        return number*factor

    return multiply
double = multiplier(2)
triple = multiplier(3)

print(double(10))
print(triple(10))

#functools provides tools for working with functions

#reduce, partial, lru_cache, wraps

#functools.partial > partial() lets us create a new function by fixing some arguments of an existing function

from functools import partial

def power(base,exponent):
    return base**exponent

square = partial(power,exponent=2)
cube = partial(power, exponent=3)

print(square(5))
print(cube(5))

#itertools provides efficient tools for working with iterators 
#chain() > combines multiple iterables into one sequence

from itertools import chain
list1 = [1, 2, 3]
list2 = [4, 5, 6]

combined = chain(list1, list2)
print(list(combined))

#combinations() > gives possible selections using repeating order
from itertools import combinations

items = ["A","B","C"]

result = combinations(items,2)

print(list(result))
