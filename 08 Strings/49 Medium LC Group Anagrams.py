"""

49. Group Anagrams
Solved
Medium
Topics
Companies
Given an array of strings strs, group the anagrams together. You can return the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.



Example 1:

Input: strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
Example 2:

Input: strs = [""]
Output: [[""]]
Example 3:

Input: strs = ["a"]
Output: [["a"]]


Constraints:

1 <= strs.length <= 104
0 <= strs[i].length <= 100
strs[i] consists of lowercase English letters.
Seen this question in a real interview before?
1/5
Yes
No
Accepted
3.1M
Submissions
4.4M
Acceptance Rate
69.1%

Runtime 85 ms Beats 78.12%
Memory 21.98 MB Beats 25.67%

"""

from collections import defaultdict
from functools import reduce

def sort(word):
    return ''.join(sorted(word))

def group(words):
    return reduce(lambda dic, iw: dic[sort(iw[1])].add(iw[0]) or dic, enumerate(words), defaultdict(set))

def anagrams(words):
    return ([words[ind] for ind in inds] for inds in group(words).values())

if __name__ == '__main__':
    words = ["eat","tea","tan","ate","nat","bat"]
    print(group(words))
    print(anagrams(words))