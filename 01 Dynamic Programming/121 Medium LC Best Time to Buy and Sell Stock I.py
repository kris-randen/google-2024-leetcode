"""

121. Best Time to Buy and Sell Stock
Solved
Easy
Topics
Companies
You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.



Example 1:

Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.
Example 2:

Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.


Constraints:

1 <= prices.length <= 105
0 <= prices[i] <= 104
Seen this question in a real interview before?
1/5
Yes
No
Accepted
5M
Submissions
9.2M
Acceptance Rate
54.0%



"""

from typing import List

def buySell(ps):
    if len(ps) < 2: return 0
    l = r = 0; i = 1; profit = ps[r] - ps[l]
    while i < len(ps):
        if ps[i] <= ps[i - 1]:
            l = i if ps[i] < ps[l] else l
            r = i; i += 1
            continue
        while (i < len(ps)) and ps[i] > ps[i - 1]:
            r += 1;i += 1
        profit = max(profit, ps[r] - ps[l])
    return profit

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        return buySell(prices)

if __name__ == '__main__':
    print("Hello")
