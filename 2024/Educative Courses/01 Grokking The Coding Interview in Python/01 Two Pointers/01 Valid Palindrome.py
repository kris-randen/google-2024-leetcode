def is_palindrome(s):
    if not s: return True
    l, r = 0, len(s) - 1
    while r >= l:
        if not s[l] == s[r]: return False
        l += 1; r -= 1
    return True