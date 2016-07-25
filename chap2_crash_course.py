from __future__ import division

print 5 / 2     # new style division
print 5 // 2    # use old default integer division


# backslashes \ are to encode special characters
tab_string = "\t"
print len(tab_string)
# one can create raw string, in which \ is \.
not_tab_string = r"\t"
print len(not_tab_string)

# unpack list
x, y = [1, 2]
print x, y
# use underscore for a value you are going to throw away
_, y = [1, 2]
print y


# use tuples to return multiple values from function
def sum_and_product(x, y):
    return x + y, x * y

sp = sum_and_product(2, 3)
print sp
s, p = sum_and_product(2, 3)
print s, p

from collections import defaultdict

# dd adds a value using a zero-argument function
dd_list = defaultdict(list)
dd_list[2].append(1)
print dd_list

dd_dict = defaultdict(dict)
dd_dict['Joel']["City"] = "Seattle"
print dd_dict

dd_pair = defaultdict(lambda: [0, 0])
dd_pair[2][1] = 1
print dd_pair

for x in range(10):
    if x == 3:
        continue
    if x == 5:
        break
    print x

# sort the list by absolute value from largest to smallest
x = sorted([-4,1,-2,3], key=abs, reverse=True)
print x

# sort the words and counts from highest count to lowest
word_counts = {'a':3, 'b':4, 'c':1}
wc = sorted(word_counts.items(),
            key=lambda (word, count): count,
            reverse=True)
print wc

even_numbers = [x for x in range(5) if x % 2 == 0]
zeros = [0 for _ in even_numbers]
print zeros

# list comprehension can include multiple fors
# later fors can use results of earlier ones
pairs = [(x, y)                     # only pairs with x < y
         for x in range(10)         # range(lo, hi) equals
         for y in range(x + 1, 10)] # [lo, lo + 1, ..., hi - 1]
print pairs

lazy_evens_below_20 = (i for i in range(20) if i % 2 == 0)
print lazy_evens_below_20
for x in lazy_evens_below_20:
    print x,
print

import random

four_uniform_randoms = [random.random() for _ in range(4)]
print four_uniform_randoms

# set random.seed to get reproducible results
#random.seed(10)
print random.random()
#random.seed(10)
print random.random()

# random.shuffle randomly reorders the elements of a list
up_to_ten = range(10)
random.shuffle(up_to_ten)
print up_to_ten

# random.choice randomly pick one element from a list
my_best_friend = random.choice(['alice', 'bob', 'charlie'])
print my_best_friend

# random.sample randomly choose a sample of elements without replacement
# i.e. w/o duplicates
lottery_numbers = range(60)
winning_numbers = random.sample(lottery_numbers, 6)
print winning_numbers

# to choose a sample of elements with replacement (allowing duplicates),
# make multiple calls to random.choice
four_with_replacement = [random.choice(range(10))
                         for _ in range(4)]
print four_with_replacement

# implement my own Set class

class Set:
    def __init__(self, values = None):
        self.dict = {}
        if values is not None:
            for value in values:
                self.add(value)

    def __repr__(self):
        """string representation of a Set object
        e.g. at python prompt or pass it to str()"""
        return "Set: " + str(self.dict.keys())

    # represent membership by being a key in the self.dict with value True
    def add(self, value):
        self.dict[value] = True

    # value is in the Set if it's a key in the dictionary
    def contains(self, value):
        return value in self.dict

    def remove(self, value):
        del self.dict[value]

s = Set([1,3,3,2])
s.add(4)
print s
print s.contains(4)
s.remove(3)
print s.contains(3)

# map with multiple-argument function on multiple lists
def multiply(x, y): return x * y

products = map(multiply, [1, 2], [3, 4])
print products

# argument unpacking, uses elements of paiirs as individual args to zip
# == zip(('a', 1), ('b', 2), ('c', 3))
pairs = [('a', 1), ('b', 2), ('c', 3)]
print zip(*pairs)


# args is a tuple of its unnamed arguments
# kwargs is a dict of its named arguments
def magic(*args, **kwargs):
    print "unnamed args", args
    print "keyword args", kwargs

magic(1, 2, key="word", key2="word2")


# use a list (or tuple) to supply unamed arguments
# use a dict to supply keyword arguments
def other_way_magic(x, y, z):
    return x + y + z

x_y_list = [1, 2]
z_dict = {'z': 3}
print other_way_magic(*x_y_list, **z_dict)  # 6

def f2(x, y): return x + y

# higher order function that takes as input some func f
# and returns a new function
def doubler(f):
    def g(*args, **kwargs):
        """whatever arguments g is supplied, pass them to f"""
        return 2 * f(*args, **kwargs)
    return g

g = doubler(f2)
print g(1, 2)   # 6