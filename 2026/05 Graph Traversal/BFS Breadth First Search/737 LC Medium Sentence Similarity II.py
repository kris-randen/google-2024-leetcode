"""

737. Sentence Similarity II
Solved
Medium
Topics
conpanies icon
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

"""

from typing import List, Dict


def graph(n: int, edges: List[tuple[int, int]]):
    g = [[] for _ in range(n)]

    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    return g

def vertices(g: List[List[int]]) -> range:
    return range(len(g))

def components(g: List[List[int]]):
    seen = [False] * len(g)
    comps = [-1] * len(g)
    count = 0

    def dfs(v: int):
        seen[v] = True
        comps[v] = count

        for w in g[v]:
            if not seen[w]:
                dfs(w)

    for v in vertices(g):
        if not seen[v]:
            count += 1
            dfs(v)

    return comps

def similar_words(u: int, v: int, comps) -> bool:
    return comps[u] == comps[v]

def similar_sentences(us: List[int], vs: List[int], comps) -> bool:
    return len(us) == len(vs) and all(similar_words(u, v, comps) for u, v in zip(us, vs))

class WordMap:
    def __init__(
            self,
            n: int,
            word_to_node: Dict[str, int],
            edges: List[tuple[int, int]],
            g: List[List[int]],
            us: List[int],
            vs: List[int]
    ):
        self.n = n
        self.word_to_node = word_to_node
        self.edges = edges
        self.g = g
        self.us = us
        self.vs = vs


def map_words(us: List[str], vs: List[str], pairs: List[List[str]]):
    ps = set()
    for u, v in pairs:
        ps.add(u)
        ps.add(v)

    words = set(us).union(set(vs)).union(ps)
    word_to_node = {word: index for index, word in enumerate(words)}
    edges = [(word_to_node[u], word_to_node[v]) for u, v in pairs]
    n = len(words)
    g = graph(n, edges)
    us = [word_to_node[u] for u in us]
    vs = [word_to_node[v] for v in vs]

    return WordMap(
        n,
        word_to_node,
        edges,
        g,
        us,
        vs
    )



class Solution:
    def areSentencesSimilarTwo(self, sentence1: List[str], sentence2: List[str], similarPairs: List[List[str]]) -> bool:
        word_map = map_words(sentence1, sentence2, similarPairs)
        comps = components(word_map.g)
        return similar_sentences(word_map.us, word_map.vs, comps)
