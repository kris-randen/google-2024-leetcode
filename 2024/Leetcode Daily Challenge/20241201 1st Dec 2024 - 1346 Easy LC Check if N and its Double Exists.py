"""

1346. Check If N and Its Double Exist
Solved
Easy
Topics
Companies
Hint
Given an array arr of integers, check if there exist two indices i and j such that :

i != j
0 <= i, j < arr.length
arr[i] == 2 * arr[j]


Example 1:

Input: arr = [10,2,5,3]
Output: true
Explanation: For i = 0 and j = 2, arr[i] == 10 == 2 * 5 == 2 * arr[j]
Example 2:

Input: arr = [3,1,7,11]
Output: false
Explanation: There is no i and j that satisfy the conditions.


Constraints:

2 <= arr.length <= 500
-103 <= arr[i] <= 103

"""

from collections import defaultdict
from functools import reduce
from typing import List


def nmap(vs):
    return reduce(lambda acc, x: acc[x[1]].append(x[0]) or acc, enumerate(vs), defaultdict(list))


def doubles(vs):
    vm = nmap(vs)
    for v in vm:
        if v == 0:
            if len(vm[v]) > 1:
                return True
            else:
                continue
        if 2 * v in vm: return True
    return False


def double(vs):
    return vs.count(0) > 1 or any(not v == 0 and 2 * v in (vss := set(vs)) for v in vs)


class Solution:
    def checkIfExist(self, vs: List[int]) -> bool:
        return double(vs)
