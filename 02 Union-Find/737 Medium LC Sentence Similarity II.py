"""

737. Sentence Similarity II
Medium
Topics
Companies
Hint
We can represent a sentence as an array of words, for example, the sentence "I am happy with leetcode" can be represented as arr = ["I","am",happy","with","leetcode"].

Given two sentences sentence1 and sentence2 each represented as a string array and given an array of string pairs similarPairs where similarPairs[i] = [xi, yi] indicates that the two words xi and yi are similar.

Return true if sentence1 and sentence2 are similar, or false if they are not similar.

Two sentences are similar if:

They have the same length (i.e., the same number of words)
sentence1[i] and sentence2[i] are similar.
Notice that a word is always similar to itself, also notice that the similarity relation is transitive. For example, if the words a and b are similar, and the words b and c are similar, then a and c are similar.



Example 1:

Input: sentence1 = ["great","acting","skills"], sentence2 = ["fine","drama","talent"], similarPairs = [["great","good"],["fine","good"],["drama","acting"],["skills","talent"]]
Output: true
Explanation: The two sentences have the same length and each word i of sentence1 is also similar to the corresponding word in sentence2.
Example 2:

Input: sentence1 = ["I","love","leetcode"], sentence2 = ["I","love","onepiece"], similarPairs = [["manga","onepiece"],["platform","anime"],["leetcode","platform"],["anime","manga"]]
Output: true
Explanation: "leetcode" --> "platform" --> "anime" --> "manga" --> "onepiece".
Since "leetcode is similar to "onepiece" and the first two words are the same, the two sentences are similar.
Example 3:

Input: sentence1 = ["I","love","leetcode"], sentence2 = ["I","love","onepiece"], similarPairs = [["manga","hunterXhunter"],["platform","anime"],["leetcode","platform"],["anime","manga"]]
Output: false
Explanation: "leetcode" is not similar to "onepiece".


Constraints:

1 <= sentence1.length, sentence2.length <= 1000
1 <= sentence1[i].length, sentence2[i].length <= 20
sentence1[i] and sentence2[i] consist of lower-case and upper-case English letters.
0 <= similarPairs.length <= 2000
similarPairs[i].length == 2
1 <= xi.length, yi.length <= 20
xi and yi consist of English letters.
Seen this question in a real interview before?
1/5
Yes
No
Accepted
71.5K
Submissions
142.8K
Acceptance Rate
50.1%

Runtime 610 ms Beats 5.42%
Memory 18.49 MB Beats 26.78%

"""

from functools import reduce
from typing import List


class UnionFindSet:
    def __init__(self, items):
        self.items = items; self.n = len(items)
        self.map = {item: ind for ind, item in enumerate(items)}
        self.id = [i for i in range(self.n)]
        self.comps = {i: {i} for i in range(self.n)}
        self.max = 1

    def size(self, i):
        return len(self.comps[i])

    def is_root(self, i):
        return i == self.id[i]

    def not_root(self, i):
        return not self.is_root(i)

    def parent(self, i):
        return self.id[i]

    def make_parent(self, i, p):
        self.id[i] = p

    def path(self, i):
        p = [i]
        while self.not_root(i):
            i = self.parent(i)
            p += [i]
        return p

    def compress(self, path):
        root = path[-1]
        for p in path: self.make_parent(p, root)
        return root

    def find(self, i):
        return self.compress(self.path(i))

    def split(self, p, q):
        return (p, q) if self.size(p) > self.size(q) else (q, p)

    def union(self, i, j):
        p, q = self.find(i), self.find(j)
        if p == q: return
        return self.join(p, q)

    def connect(self, a, b):
        self.union(self.map[a], self.map[b])

    def merge_comp(self, s, l):
        self.comps[l] = self.comps[l].union(self.comps.pop(s))

    def join(self, p, q):
        l, s = self.split(p, q)
        self.make_parent(s, l)
        self.merge_comp(s, l)
        self.max = max(self.max, len(self.comps[l]))
        return l

    def connected(self, a, b):
        return self.find(self.map[a]) == self.find(self.map[b])


def similaritys(sentence1, sentence2, similarPairs):
    if len(sentence1) != len(sentence2): return False
    pairs = reduce(lambda x, y: x + y, similarPairs, [])
    words = set(pairs + sentence1 + sentence2)
    uf = UnionFindSet(words)
    for a, b in similarPairs:
        uf.connect(a, b)
    for word1, word2 in zip(sentence1, sentence2):
        if not uf.connected(word1, word2): return False
    return True


# 20241130 30th Nov 2024 Re-solved.

class UnionFindDict:
    def __init__(self, vs):
        self.n = len(vs)
        self.vm = {v: i for i, v in enumerate(vs)}
        self.id = [i for i in range(self.n)]
        self.sz = {i: 1 for i in range(self.n)}

    def root(self, p):
        if not p == self.id[p]:
            self.id[p] = self.root(self.id[p])
        return self.id[p]

    def find(self, p, q):
        return self.root(p) == self.root(q)

    def split(self, p, q):
        s, l = self.root(p), self.root(q)
        return (s, l) if self.sz[s] < self.sz[l] else (l, s)

    def union(self, p, q):
        if self.find(p, q): return
        s, l = self.split(p, q)
        self.id[s] = l
        self.sz[l] += self.sz.pop(s)

    def similar(self, u, v):
        return self.find(self.vm[u], self.vm[v])

    def join(self, u, v):
        self.union(self.vm[u], self.vm[v])


def similarity(s, t, ps):
    if not (n := len(s)) == len(t): return False
    ws = set(
        reduce(lambda acc, vs: acc + vs, ps, []) + s + t
    )
    uf = UnionFindDict(ws)
    for p in ps: uf.join(p[0], p[1])
    for i in range(n):
        if not uf.similar(s[i], t[i]): return False
    return True


class Solution:
    def areSentencesSimilarTwo(self, s: List[str], t: List[str], ps: List[List[str]]) -> bool:
        return similarity(s, t, ps)

