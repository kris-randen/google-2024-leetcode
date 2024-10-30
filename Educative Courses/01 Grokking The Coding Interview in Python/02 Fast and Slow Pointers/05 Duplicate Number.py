"""

Statement
Given an array of positive numbers, nums, such that the values lie in the range [1,n], inclusive, and that there are n+1 numbers in the array, find and return the duplicate number present in nums. There is only one repeated number in nums.

Note: You cannot modify the given array nums. You have to solve the problem using only constant extra space.

"""


def step(ns, s):
    return ns[s]


def steps(ns, f):
    return ns[ns[f]]


def intersect(ns):
    s, f = 0, 0
    while not s == step(ns, s):
        s = step(ns, s)
        f = steps(ns, f)
        if s == f: return s


def find(ns, ip):
    s, f = 0, ip
    while not s == f:
        s = step(ns, s)
        f = step(ns, f)
    return s


def find_duplicate(ns):
    return find(ns, intersect(ns))
