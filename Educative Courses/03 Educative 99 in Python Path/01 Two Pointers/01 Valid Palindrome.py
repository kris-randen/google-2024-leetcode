"""

01 Valid Palindrome

"""

def is_palindrome(s):
    if (n := len(s)) == 0:      return True
    l, r = 0, n - 1
    while l <= r:
        if not s[l] == s[r]:    return False
        l += 1; r -= 1
    return True