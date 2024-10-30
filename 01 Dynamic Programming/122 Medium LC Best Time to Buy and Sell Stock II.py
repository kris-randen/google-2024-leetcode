"""

122. Best Time to Buy and Sell Stock II
Solved
Medium
Topics
Companies
You are given an integer array prices where prices[i] is the price of a given stock on the ith day.

On each day, you may decide to buy and/or sell the stock. You can only hold at most one share of the stock at any time. However, you can buy it then immediately sell it on the same day.

Find and return the maximum profit you can achieve.



Example 1:

Input: prices = [7,1,5,3,6,4]
Output: 7
Explanation: Buy on day 2 (price = 1) and sell on day 3 (price = 5), profit = 5-1 = 4.
Then buy on day 4 (price = 3) and sell on day 5 (price = 6), profit = 6-3 = 3.
Total profit is 4 + 3 = 7.
Example 2:

Input: prices = [1,2,3,4,5]
Output: 4
Explanation: Buy on day 1 (price = 1) and sell on day 5 (price = 5), profit = 5-1 = 4.
Total profit is 4.
Example 3:

Input: prices = [7,6,4,3,1]
Output: 0
Explanation: There is no way to make a positive profit, so we never buy the stock to achieve the maximum profit of 0.


Constraints:

1 <= prices.length <= 3 * 104
0 <= prices[i] <= 104
Seen this question in a real interview before?
1/5
Yes
No
Accepted
2M
Submissions
3M

Runtime 50 ms Beats 91.94%
Memory 20.35 MB Beats 5.03%

"""

"""
Haskell Solution

rBestTimeToBuyAndSell :: (Num a, Ord a) => [a] -> a
rBestTimeToBuyAndSell []  = 0
rBestTimeToBuyAndSell [p] = 0
rBestTimeToBuyAndSell (p : q : qs)
 | p <= q    = rBestTimeToBuyAndSell (q : qs)
 | otherwise = (p - q) + rBestTimeToBuyAndSell (q : qs)

bestTimeToBuyAndSell :: (Num a, Ord a) => [a] -> a
bestTimeToBuyAndSell ps = rBestTimeToBuyAndSell (reverse ps)

"""


from typing import List

def bestTime(ps):
    if len(ps) < 2: return 0
    last = ps.pop()
    return ((last - ps[-1]) if last > ps[-1] else 0) + bestTime(ps)

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        return bestTime(prices)