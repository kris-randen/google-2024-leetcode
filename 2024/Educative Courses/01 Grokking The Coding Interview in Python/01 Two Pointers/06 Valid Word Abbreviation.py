"""

Statement
Given a string word and an abbreviation abbr, return TRUE if the abbreviation matches the given string. Otherwise, return FALSE.

A certain word "calendar" can be abbreviated as follows:

"cal3ar" ("cal end ar" skipping three characters "end" from the word "calendar" still matches the provided abbreviation)

"c6r" ("c alenda r" skipping six characters "alenda" from the word "calendar" still matches the provided abbreviation)

The following are not valid abbreviations:

"c06r" (has leading zeroes)

"cale0ndar" (replaces an empty string)

"c24r" ("c al enda r" the replaced substrings are adjacent)

"""

import re

def split_alphanumeric(s):
    return re.findall(r'[A-Za-z]+|\d+', s)

def leadingzero(s):
    return s.isdigit() and (s[0] == '0')

def valid_abbr(abbr):
    split = split_alphanumeric(abbr)
    return expand(split) if (not any(leadingzero(s) for s in split)) else None

def amap(split):
    return ((s if s.isalpha() else (' ' * int(s))) for s in split)

def expand(split):
    return ''.join(amap(split))

def equal(cw, ce):
    return ce == ' ' or ce == cw

def compares(word, expr):
    pw, pe, lw, le = 0, 0, len(word), len(expr)
    while pw < lw:
        if not equal(word[pw], expr[pe]): return False
        pw += 1; pe += 1
    return True


def valid_word_abbreviation(word, abbr):
    if not (expr := valid_abbr(abbr)): return False
    if not (lw := len(word)) == (le := len(expr)): return False
    return compares(word, expr)