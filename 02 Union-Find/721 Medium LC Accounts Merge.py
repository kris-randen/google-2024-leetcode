"""

721. Accounts Merge
Medium
Topics
Companies
Hint
Given a list of accounts where each element accounts[i] is a list of strings, where the first element accounts[i][0] is a name, and the rest of the elements are emails representing emails of the account.

Now, we would like to merge these accounts. Two accounts definitely belong to the same person if there is some common email to both accounts. Note that even if two accounts have the same name, they may belong to different people as people could have the same name. A person can have any number of accounts initially, but all of their accounts definitely have the same name.

After merging the accounts, return the accounts in the following format: the first element of each account is the name, and the rest of the elements are emails in sorted order. The accounts themselves can be returned in any order.



Example 1:

Input: accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],["John","johnsmith@mail.com","john00@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]
Output: [["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]
Explanation:
The first and second John's are the same person as they have the common email "johnsmith@mail.com".
The third John and Mary are different people as none of their email addresses are used by other accounts.
We could return these lists in any order, for example the answer [['Mary', 'mary@mail.com'], ['John', 'johnnybravo@mail.com'],
['John', 'john00@mail.com', 'john_newyork@mail.com', 'johnsmith@mail.com']] would still be accepted.
Example 2:

Input: accounts = [["Gabe","Gabe0@m.co","Gabe3@m.co","Gabe1@m.co"],["Kevin","Kevin3@m.co","Kevin5@m.co","Kevin0@m.co"],["Ethan","Ethan5@m.co","Ethan4@m.co","Ethan0@m.co"],["Hanzo","Hanzo3@m.co","Hanzo1@m.co","Hanzo0@m.co"],["Fern","Fern5@m.co","Fern1@m.co","Fern0@m.co"]]
Output: [["Ethan","Ethan0@m.co","Ethan4@m.co","Ethan5@m.co"],["Gabe","Gabe0@m.co","Gabe1@m.co","Gabe3@m.co"],["Hanzo","Hanzo0@m.co","Hanzo1@m.co","Hanzo3@m.co"],["Kevin","Kevin0@m.co","Kevin3@m.co","Kevin5@m.co"],["Fern","Fern0@m.co","Fern1@m.co","Fern5@m.co"]]


Constraints:

1 <= accounts.length <= 1000
2 <= accounts[i].length <= 10
1 <= accounts[i][j].length <= 30
accounts[i][0] consists of English letters.
accounts[i][j] (for j > 0) is a valid email.
Seen this question in a real interview before?
1/5
Yes
No
Accepted
402.3K
Submissions
699.6K

Runtime 306 ms Beats 9.06%
Memory 23.92 MB Beats 11.54%

"""

import random
from functools import reduce
from collections import defaultdict
from typing import List


def split(accs):
    names = list(map(lambda x: x[0], accs))
    emails = list(map(lambda x: set(x[1:]), accs))
    return names, emails


def invert(emails_list):
    inverted = defaultdict(set)
    for index, emails in enumerate(emails_list):
        for email in emails:
            inverted[email].add(index)
    return inverted


class UnionFind:
    def __init__(self, n):
        self.id = [i for i in range(n)]
        self.comps = {i: {i} for i in range(n)}

    def size(self, r):
        return len(self.comps[r])

    def path(self, i):
        p = [i]
        while not i == self.id[i]:
            i = self.id[i]
            p.append(i)
        return p

    def compress(self, path):
        root = path[-1]
        for p in path: self.id[p] = root
        return root

    def find(self, i):
        return self.compress(self.path(i))

    def split(self, p, q):
        return (p, q) if self.size(p) > self.size(q) else (q, p)

    def union(self, i, j):
        p, q = self.find(i), self.find(j)
        if p == q: return
        self.join(p, q)

    def join(self, p, q):
        l, s = self.split(p, q)
        self.id[s] = l
        self.comps[l] = self.comps[l].union(self.comps.pop(s))


def connect(edges, uf):
    for email in edges:
        indices = edges[email]
        ind = random.choice(list(indices))
        for other in indices:
            uf.union(ind, other)


def list_union(sets):
    return reduce(lambda x, y: x.union(y), sets)


def extract_emails(emails, uf):
    return map(lambda sets:
               sorted(
                   reduce(lambda x, y: x.union(y), sets)),
               map(lambda indices: [emails[i] for i in indices],
                   uf.comps.values())
               )


def extract_names(names, uf):
    return map(lambda root: [names[root]], uf.comps.keys())


def assemble(names, emails, uf):
    return list(map(lambda x: x[0] + x[1],
                    zip(extract_names(names, uf),
                        extract_emails(emails, uf))
                    )
                )

def merge(accs):
    names, emails = split(accs)
    edges = invert(emails)
    uf = UnionFind(len(names))
    connect(edges, uf)
    return assemble(names, emails, uf)

# 20241130 30th Nov 2024 Re-solved

class UnionFindDict:
    def __init__(self, es):
        self.n = len(es)
        self.em = {e: i for i, e in enumerate(es)}
        self.me = {i: e for e, i in self.em.items()}
        self.id = [i for i in range(self.n)]
        self.sz = {i: {self.me[i]} for i in range(self.n)}

    def size(self, p):
        return len(self.sz[p])

    def root(self, p):
        if not p == self.id[p]:
            self.id[p] = self.root(self.id[p])
        return self.id[p]

    def find(self, p, q):
        return self.root(p) == self.root(q)

    def split(self, p, q):
        s, l = self.root(p), self.root(q)
        return (s, l) if self.size(s) < self.size(l) else (l, s)

    def union(self, p, q):
        if self.find(p, q): return
        s, l = self.split(p, q)
        self.id[s] = l
        self.sz[l].update(self.sz.pop(s))

    def similar(self, v, w):
        return self.find(self.em[v], self.em[w])

    def join(self, v, w):
        self.union(self.em[v], self.em[w])


def merge(acs):
    es = set(
        reduce(
            lambda acc, x: acc + x,
            (ac[1:] for ac in acs),
            []
        )
    )
    en = {}
    for ac in acs:
        for a in ac[1:]:
            en[a] = ac[0]

    uf = UnionFindDict(es)
    for ac in acs:
        for e in ac[1:]:
            uf.join(ac[1], e)
    mcs = []
    for i in uf.sz:
        ems = sorted(list(uf.sz[i]))
        mc = [en[ems[0]]]
        mc += ems
        mcs.append(mc)
    return mcs


class Solution:
    def accountsMerge(self, acs: List[List[str]]) -> List[List[str]]:
        return merge(acs)

