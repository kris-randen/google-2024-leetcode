"""

Minimum Window Subsequence

Statement
Given two strings, str1 and str2, find the shortest substring in str1 such that str2 is a subsequence of that substring.

A substring is defined as a contiguous sequence of characters within a string. A subsequence is a sequence that can be derived from another sequence by deleting zero or more elements without changing the order of the remaining elements.

Let’s say you have the following two strings:

str1 = “abbcb”

str2 = “ac”

In this example, “abbc” is a substring of str1, from which we can derive str2 simply by deleting both the instances of the character bb. Therefore, str2 is a subsequence of this substring. Since this substring is the shortest among all the substrings in which str2 is present as a subsequence, the function should return this substring, that is, “abbc”.

If there is no substring in str1 that covers all characters in str2, return an empty string.

If there are multiple minimum-length substrings that meet the subsequence requirement, return the one with the left-most starting index.

"""

def fscan(s, t, k, ns, nt):
    l, m, b, e = k, 0, None, None
    while l < ns and m < nt:
        if s[l] == t[m]:
            b = l if b is None else b
            l += 1; m += 1
        else:
            l += 1
    return (b, l - 1) if m == nt else (None, None)

def rscan(s, t, b, e, nt):
    l, r, m = e, e, nt - 1
    while m >= 0 and l >= b:
        if s[l] == t[m]:
            l -= 1; m -= 1
        else:
            l -= 1
    return l + 1, e

def min_window(s, t):
    if not t or not s or (nt := len(t)) > (ns := len(s)): return ''
    l, m, ml, ms = 0, 0, float('inf'), ''
    while l < ns:
        b, e = fscan(s, t, l, ns, nt)
        if b is None: break
        b, e = rscan(s, t, b, e, nt)
        if (e - b + 1) < ml:
            ml = e - b + 1
            ms = s[b:e+1]
        l = b + 1
    return ms

if __name__ == '__main__':
    s, t = "abcdebdde", "bde"
    print(min_window(s, t))
    s, t = "fgrqsqsnodwmxzkzxwqegkndaa", "kzed"
    print(min_window(s, t))





