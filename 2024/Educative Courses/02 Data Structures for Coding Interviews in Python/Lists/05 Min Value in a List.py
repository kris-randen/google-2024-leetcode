from functools import reduce

def find_minimum(lst):
    return reduce(min, lst, float('inf'))
