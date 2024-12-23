"""

1101. The Earliest Moment When Everyone Become Friends
Medium
Topics
Companies
Hint
There are n people in a social group labeled from 0 to n - 1. You are given an array logs where logs[i] = [timestampi, xi, yi] indicates that xi and yi will be friends at the time timestampi.

Friendship is symmetric. That means if a is friends with b, then b is friends with a. Also, person a is acquainted with a person b if a is friends with b, or a is a friend of someone acquainted with b.

Return the earliest time for which every person became acquainted with every other person. If there is no such earliest time, return -1.



Example 1:

Input: logs = [[20190101,0,1],[20190104,3,4],[20190107,2,3],[20190211,1,5],[20190224,2,4],[20190301,0,3],[20190312,1,2],[20190322,4,5]], n = 6
Output: 20190301
Explanation:
The first event occurs at timestamp = 20190101, and after 0 and 1 become friends, we have the following friendship groups [0,1], [2], [3], [4], [5].
The second event occurs at timestamp = 20190104, and after 3 and 4 become friends, we have the following friendship groups [0,1], [2], [3,4], [5].
The third event occurs at timestamp = 20190107, and after 2 and 3 become friends, we have the following friendship groups [0,1], [2,3,4], [5].
The fourth event occurs at timestamp = 20190211, and after 1 and 5 become friends, we have the following friendship groups [0,1,5], [2,3,4].
The fifth event occurs at timestamp = 20190224, and as 2 and 4 are already friends, nothing happens.
The sixth event occurs at timestamp = 20190301, and after 0 and 3 become friends, we all become friends.
Example 2:

Input: logs = [[0,2,0],[1,0,1],[3,0,3],[4,1,2],[7,3,1]], n = 4
Output: 3
Explanation: At timestamp = 3, all the persons (i.e., 0, 1, 2, and 3) become friends.


Constraints:

2 <= n <= 100
1 <= logs.length <= 104
logs[i].length == 3
0 <= timestampi <= 109
0 <= xi, yi <= n - 1
xi != yi
All the values timestampi are unique.
All the pairs (xi, yi) occur at most one time in the input.
Seen this question in a real interview before?
1/5
Yes
No
Accepted
97.2K
Submissions
149K
Acceptance Rate
65.2%

Runtime 84 ms Beats 98.89%
Memory 17.20 MB Beats 10.89%

"""

class UnionFind:
    def __init__(self, n):
        self.id = [i for i in range(n)]; self.max = 1
        self.comps = {i: {i} for i in range(n)}

    def size(self, p):
        return len(self.comps[p])

    def is_greater(self, p, q):
        return self.size(p) > self.size(q)

    @property
    def count(self):
        return len(self.comps)

    def parent(self, i):
        return self.id[i]

    def assign(self, i, p):
        self.id[i] = p

    def merge(self, s, l):
        self.comps[l].update(self.comps.pop(s))

    def is_root(self, i):
        return i == self.parent(i)

    def is_not_root(self, i):
        return not self.is_root(i)

    def path(self, i):
        p = [i]
        while self.is_not_root(i):
            i = self.parent(i)
            p += [i]
        return p

    def compress(self, path):
        root = path[-1]
        for p in path: self.assign(p, root)
        return root

    def find(self, i):
        return self.compress(self.path(i))

    def split(self, p, q):
        return (p, q) if self.is_greater(p, q) else (q, p)

    def union(self, i, j):
        p, q = self.find(i), self.find(j)
        if not p == q: self.join(p, q)

    def join(self, p, q):
        l, s = self.split(p, q)
        self.assign(s, l)
        self.merge(s, l)
        self.max = max(self.max, self.size(l))

def earliest_friends(logs, n):
    uf = UnionFind(n)
    logs = sorted(logs, key=lambda x: x[0])
    for time, u, v in logs:
        uf.union(u, v)
        if uf.count == 1: return time
    return -1