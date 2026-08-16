"""

2657. Find the Prefix Common Array of Two Arrays
Solved
Medium

You are given two 0-indexed integer permutations A and B of length n.

A prefix common array of A and B is an array C such that C[i] is equal to the count of numbers that are present at or before the index i in both A and B.

Return the prefix common array of A and B.

A sequence of n integers is called a permutation if it contains all integers from 1 to n exactly once.



Example 1:

Input: A = [1,3,2,4], B = [3,1,2,4]
Output: [0,2,3,4]
Explanation: At i = 0: no number is common, so C[0] = 0.
At i = 1: 1 and 3 are common in A and B, so C[1] = 2.
At i = 2: 1, 2, and 3 are common in A and B, so C[2] = 3.
At i = 3: 1, 2, 3, and 4 are common in A and B, so C[3] = 4.
Example 2:

Input: A = [2,3,1], B = [3,1,2]
Output: [0,1,3]
Explanation: At i = 0: no number is common, so C[0] = 0.
At i = 1: only 3 is common in A and B, so C[1] = 1.
At i = 2: 1, 2, and 3 are common in A and B, so C[2] = 3.


Constraints:

1 <= A.length == B.length == n <= 50
1 <= A[i], B[i] <= n
It is guaranteed that A and B are both a permutation of n integers.

"""

from typing import List


def prefix_common_array_sets(us: List[int], vs: List[int]) -> List[int]:
    l, r, n = 0, 0, len(us)
    cs, count = [0] * n, 0
    su, sv, sc = set(), set(), set()

    for i in range(n):
        su.add(us[i])
        sv.add(vs[i])
        if us[i] in sv:
            sc.add(us[i])
        if vs[i] in su:
            sc.add(vs[i])
        cs[i] = len(sc)

    return cs


def mark(seen: List[int], x: int) -> int:
    seen[x] += 1
    return int(seen[x] == 2)

def prefix_common_array(us: List[int], vs: List[int]) -> List[int]:
    seen = [0] * (len(us) + 1) # Permutation arrays going from 1 to n so we need to go up to the nth index
    common, cs = 0, []

    for u, v in zip(us, vs):
        common += mark(seen, u)
        common += mark(seen, v)
        cs.append(common)

    return cs


class Solution:
    def findThePrefixCommonArray(self, A: List[int], B: List[int]) -> List[int]:
        return prefix_common_array_sets(A, B)