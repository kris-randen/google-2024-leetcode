"""

128. Longest Consecutive Sequence
Solved
Medium
Topics
Companies
Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.

You must write an algorithm that runs in O(n) time.



Example 1:

Input: nums = [100,4,200,1,3,2]
Output: 4
Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.
Example 2:

Input: nums = [0,3,7,2,5,8,4,6,0,1]
Output: 9


Constraints:

0 <= nums.length <= 105
-109 <= nums[i] <= 109

Runtime 763 ms Beats 35.95%
Memory 45.24 MB Beats 5.05%

"""


class UnionFind:
    def __init__(self, ns):
        self.ns = list(ns); n = len(self.ns)
        self.id = [i for i in range(n)]
        self.sz = [1 for _ in range(n)]
        self.map = {num: ind for ind, num in enumerate(ns)}
        self.count = n

    def path_ind(self, i):
        p = [i]
        while i != self.id[i]:
            i = self.id[i]
            p.append(i)
        return p

    def compress_ind(self, path):
        root = path[-1]
        for p in path: self.id[p] = root
        return root

    def find_ind(self, i):
        return self.compress_ind(self.path_ind(i))

    def find(self, a):
        return self.find_ind(self.map[a])

    def split(self, p, q):
        return (p, q) if self.sz[p] > self.sz[q] else (q, p)

    def union_ind(self, i, j):
        p, q = self.find_ind(i), self.find_ind(j)
        if p == q: return
        self.union_roots(p, q)

    def union(self, a, b):
        self.union_ind(self.map[a], self.map[b])

    def union_roots(self, p, q):
        l, s = self.split(p, q)
        self.id[s] = l
        self.sz[l] += self.sz[s]
        self.count -= 1

    def max_size(self):
        return max(self.sz)


def longest_cons_seq(nums):
    unique = set(nums)
    uf = UnionFind(unique)
    for num in unique:
        if (num - 1) in unique:
            uf.union(num, num - 1)
        if (num + 1) in unique:
            uf.union(num, num + 1)
    return uf.max_size()
