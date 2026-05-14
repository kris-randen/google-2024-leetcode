"""

Statement
Write an algorithm to determine if a number n is a happy number.

We use the following process to check if a given number is a happy number:

Starting with the given number n, replace the number with the sum of the squares of its digits.
Repeat the process until:
The number equals 1, which will depict that the given number n is a happy number.
The number enters a cycle, which will depict that the given number n is not a happy number.
Return TRUE if n is a happy number, and FALSE if not.

"""

def digits(n):
    return (int(d) for d in str(n))

def sumsq(ds):
    return sum(d**2 for d in ds)

def sqd(n):
    return sumsq(digits(n))

def is_happy_number(n):
    s, f = n, n
    while not f == 1:
        s = sqd(s); f = sqd(sqd(f))
        if s == f: return False
    return True

