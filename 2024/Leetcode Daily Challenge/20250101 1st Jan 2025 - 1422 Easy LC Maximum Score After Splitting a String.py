"""

1422. Maximum Score After Splitting a String
Easy

Given a string s of zeros and ones, return the maximum score after splitting the string into two non-empty substrings (i.e. left substring and right substring).

The score after splitting a string is the number of zeros in the left substring plus the number of ones in the right substring.

 

Example 1:

Input: s = "011101"
Output: 5 
Explanation: 
All possible ways of splitting s into two non-empty substrings are:
left = "0" and right = "11101", score = 1 + 4 = 5 
left = "01" and right = "1101", score = 1 + 3 = 4 
left = "011" and right = "101", score = 1 + 2 = 3 
left = "0111" and right = "01", score = 1 + 1 = 2 
left = "01110" and right = "1", score = 2 + 1 = 3
Example 2:

Input: s = "00111"


Output: 5
Explanation: When left = "00" and right = "111", we get the maximum score = 2 + 3 = 5
Example 3:

Input: s = "1111"
Output: 3
 

Constraints:

2 <= s.length <= 500
The string s consists of characters '0' and '1' only.


Performance

Runtime 0 ms Beats 100.00%
Memory 17.75 MB Beats 15.52%

"""


"""

Dynamic Programming Approach

What we quickly realize by trying a DP solution is you initialize at index 1 since both splits have to be non-empty. The score at this split is the number of 1s in vs[1:] and plus 1 if the first element is 0. So we initialize with this score.

Now every time we move the split index forward observe that if the new element is 0 we end up passing a 0 from right to left. This doesn't affect the score of right but increases the score of left and therefore the total score by 1.

Similarly if the new element is 1 we end up passing a 1 from right to left which decrements the score by 1. So we keep moving the index till the last - 1 index and see where we find the max score across all possible splits.

"""


def start(vs):
    return sum(vs[1:]) + (1 if not vs[0] else 0)

def score(vs):
    maxs = sc = start(vs)
    for i in range(1, len(vs) - 1):
        sc = sc + (1 if not vs[i] else -1)
        maxs = max(maxs, sc)
    return maxs

class Solution:
    def maxScore(self, s: str) -> int:
        return score([int(v) for v in s])
























