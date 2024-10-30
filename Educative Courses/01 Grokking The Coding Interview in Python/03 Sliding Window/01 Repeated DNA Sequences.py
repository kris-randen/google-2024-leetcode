"""

Repeated DNA Sequences

Statement
Given a string, dna, that represents a DNA subsequence, and a number k
, return all the contiguous subsequences (substrings) of length k
 that occur more than once in the string. The order of the returned subsequences does not matter. If no repeated substring is found, the function should return an empty set.

The DNA sequence is composed of a series of nucleotides abbreviated as
A, C, G, and T
. For example, ACGAATTCCG
 is a DNA sequence. When studying DNA, it is useful to identify repeated sequences in it.

"""

from functools import reduce


def find_repeated_sequences0(dna, k):
    if (n := len(dna)) <= k: return set()
    hashes, reps = set(), set()
    l, r = 0, k - 1
    while r < n:
        if (s := dna[l:r + 1]) in hashes:
            reps.add(s)
        else:
            hashes.add(s)
        l += 1; r += 1
    return

def find_repeated_sequences(dna, k):
    if (n := len(dna)) <= k: return set()

    h = {'A': 1, 'T': 2, 'C': 3, 'G': 4}
    num = [h[d] for d in dna]
    def hmap(i):
        return num[i] * (5 ** i)
    def hmaps(i, j):
        return reduce(lambda acc, n: acc + hmap(n), num[i: j + 1], 0)

    hs, rs = set(), set()
    l, r = 0, k - 1
    hm = hmaps(l, r); hs.add(hm)
    while r < n:
        if hm in hs:
            rs.add(dna[l: r + 1])
        else:
            hs.add(hm)
        hm = hm - (hmap(l)) + (hmap(r + 1))
        l += 1; r += 1
    return rs