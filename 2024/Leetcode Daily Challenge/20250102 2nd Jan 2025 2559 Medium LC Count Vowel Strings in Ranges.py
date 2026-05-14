"""

2559. Count Vowel Strings in Ranges
Medium

You are given a 0-indexed array of strings words and a 2D array of integers queries.

Each query queries[i] = [li, ri] asks us to find the number of strings present in the range li to ri (both inclusive) of words that start and end with a vowel.

Return an array ans of size queries.length, where ans[i] is the answer to the ith query.

Note that the vowel letters are 'a', 'e', 'i', 'o', and 'u'.

 

Example 1:

Input: words = ["aba","bcb","ece","aa","e"], queries = [[0,2],[1,4],[1,1]]
Output: [2,3,0]
Explanation: The strings starting and ending with a vowel are "aba", "ece", "aa" and "e".
The answer to the query [0,2] is 2 (strings "aba" and "ece").
to query [1,4] is 3 (strings "ece", "aa", "e").
to query [1,1] is 0.
We return [2,3,0].
Example 2:

Input: words = ["a","e","i"], queries = [[0,2],[0,1],[2,2]]
Output: [3,2,1]
Explanation: Every string satisfies the conditions, so we return [3,2,1].
 

Constraints:

1 <= words.length <= 105
1 <= words[i].length <= 40
words[i] consists only of lowercase English letters.
sum(words[i].length) <= 3 * 105
1 <= queries.length <= 105
0 <= li <= ri < words.length

Performance countsd (without prefix sum) ~ O(N * Q)
Time Limit Exceeded


Performance counts (with prefix sum) ~ O(N) Time and Space

Runtime 19 ms Beats 71.40%
Memory 51.14 MB Beats 8.17%

"""



def countsd(wm, qs):
    def count(q):   return sum(1 for i in range(q[0], q[1] + 1) if wm[i])
    return [count(q) for q in qs]

def countsdd(ss, qs):
    def count(q):   return ss[q[0]] - ss[q[1] + 1]
    return [count(q) for q in qs]

def suffixs(wm, n):
    ss = [0] * (n + 1)
    for i in reversed(range(n)):
        ss[i] = ss[i + 1] + wm[i]
    return ss

from itertools import accumulate as acc

def wmap(ws, vs):
    def vowel(w):   return 1 if w[0] in vs and w[-1] in vs else 0
    return [vowel(w) for w in ws]

def prefixs(wm):    return [0] + list(acc(wm))

def counts(ps, qs):
    def count(q):   return ps[q[1] + 1] - ps[q[0]]
    return [count(q) for q in qs]

class Solution:
    def vowelStrings(self, ws: List[str], qs: List[List[int]]) -> List[int]:
        return counts(
                        prefixs(
                                wmap(ws, vs={'a', 'e', 'i', 'o', 'u'})
                               ), qs
                     )































