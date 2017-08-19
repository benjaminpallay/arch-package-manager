from toolz.curried import reduce
from toolz.functoolz import curry
from itertools import takewhile,dropwhile

@curry
def better_reduce(a,b,c):
    return reduce(a,c,b)

@curry
def curried_takewhile(a,b):
    return takewhile(a,b)

@curry
def curried_dropwhile(a,b):
    return dropwhile(a,b)