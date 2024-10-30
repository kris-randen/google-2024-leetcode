"""

Statement
Write a function that takes a string as input and checks whether it can be a valid palindrome by removing at most one character from it.

"""

def palindrome0(s, lo, hi):
    if (n := len(s)) < 2 or hi <= lo: return True
    l, r = lo, hi
    while l < r:
        if not s[l] == s[r]: return False
        l += 1; r -= 1
    return True

def is_palindrome0(s):
    if (n := len(s)) < 2: return True
    l, r = 0, n - 1
    while l < r:
        if not s[l] == s[r]:
            return palindrome0(s, l + 1, r) or palindrome0(s, l, r - 1)
        l += 1; r -= 1
    return True

def palindrome(s, lo, hi, k):
    if (n := len(s)) < 2 or hi <= lo: return True
    l, r = lo, hi
    while l < r:
        if not s[l] == s[r]:
            if k == 0:
                return False
            else:
                return palindrome(s, l + 1, r, k - 1) or palindrome(s, l, r - 1, k - 1)
        l += 1; r -= 1
    return True

def is_palindrome(s):
    return palindrome(s, 0, len(s) - 1, 1)