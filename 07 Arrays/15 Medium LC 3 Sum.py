"""

15. 3Sum
Solved
Medium
Topics
Companies
Hint
Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.



Example 1:

Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation:
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.
Example 2:

Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.
Example 3:

Input: nums = [0,0,0]
Output: [[0,0,0]]
Explanation: The only possible triplet sums up to 0.


Constraints:

3 <= nums.length <= 3000
-105 <= nums[i] <= 105

"""

from collections import defaultdict
from functools import reduce

def map_nums(ps):
    return reduce(lambda dic, ip: dic[ip[1]].add(ip[0]) or dic, enumerate(ps), defaultdict(set))

def map_set(a, b, cs):
    return set((tuple(sorted((a, b, c))) for c in cs))

def map_tuples(ts, ps):
    return set((
        tuple(
        sorted(
            (ps[k] for k in ks)
            )
        ) for ks in ts))

def sum_3(ps):
    n, dic, ts = len(ps), map_nums(ps), set()
    for i in range(n):
        for j in range(i + 1, n):
            t = -(ps[i] + ps[j])
            ds = dic.get(t, set())
            ds = ds.difference({i, j})
            ts = ts.union(map_set(i, j, ds))
    return map_tuples(ts, ps)

if __name__ == '__main__':
    ps = [-7,-4,-6,6,4,-6,-9,-10,-7,5,3,-1,-5,8,-1,-2,-8,-1,5,-3,-5,4,2,-5,-4,4,7]
    print(map_nums(ps))
    bs = [[-1,-1,2],[-9,2,7],[-10,2,8],[-5,2,3],[-6,-2,8],[-8,3,5],[-8,2,6],[-4,-2,6],[-6,-1,7],[-5,-2,7],[-7,-1,8],[-10,5,5],[-2,-1,3],[-7,3,4],[-3,-1,4],[-6,2,4],[-5,-3,8],[-7,2,5],[-10,4,6],[-4,-3,7],[-9,3,6],[-9,4,5],[-4,-4,8],[-4,-1,5],[-5,-1,6],[-10,3,7],[-8,4,4]]
    cs = [[-10,2,8],[-10,3,7],[-10,4,6],[-10,5,5],[-9,2,7],[-9,3,6],[-9,4,5],[-8,2,6],[-8,3,5],[-8,4,4],[-7,-1,8],[-7,2,5],[-7,3,4],[-6,-2,8],[-6,-1,7],[-6,2,4],[-5,-3,8],[-5,-2,7],[-5,-1,6],[-5,2,3],[-4,-4,8],[-4,-3,7],[-4,-2,6],[-4,-1,5],[-3,-2,5],[-3,-1,4],[-2,-1,3],[-1,-1,2]]
    bss = set(map(tuple, bs))
    css = set(map(tuple, cs))
    print(css.difference(bss))
