"""

309. Best Time to Buy and Sell Stock with Cooldown
Attempted
Medium
Topics
Companies
You are given an array prices where prices[i] is the price of a given stock on the ith day.

Find the maximum profit you can achieve. You may complete as many transactions as you like (i.e., buy one and sell one share of the stock multiple times) with the following restrictions:

After you sell your stock, you cannot buy stock on the next day (i.e., cooldown one day).
Note: You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).



Example 1:

Input: prices = [1,2,3,0,2]
Output: 3
Explanation: transactions = [buy, sell, cooldown, buy, sell]
Example 2:

Input: prices = [1]
Output: 0


Constraints:

1 <= prices.length <= 5000
0 <= prices[i] <= 1000
Seen this question in a real interview before?
1/5
Yes
No
Accepted
536.5K
Submissions
912.8K
Acceptance Rate
58.8%

SRTBOT
1. Subproblems
Prefixes
But we keep track of Pn and the last sale day

2. Relationship
We are at day n. Possibilities
a. You don't sell on Day n: Pn = Pn-1
b. You do sell on Day n:
 Pn = max(Pn-1, Pn-3 + ps[n] - ps[n -1], Pn-4 + ps[n] - ps[n - 2],
 Pn-5 + ps[n] - ps[n - 3],..., P1 + ps[n] - ps[3], P0 + ps[n] - ps[2], ps[n] - ps[1])
 Pn-1 = max(Pn-2, Pn-4 + ps[n - 1] - ps[n - 2], Pn-5 + ps[n - 1] - ps[n - 3]
4. Base Case

5. Orginal Problem
Pn

6. Time
O(n) subproblems with constant time for each so O(n)

"""

def get(P, i):
    return P[i] if i >= 0 else 0

def max_profit_cool_down(ps):
    n = len(ps)
    if n < 2: return 0
    P = [0] * n
    for i in range(1, n):
        P[i] = get(P, i - 1)
        for k in range(3, i + 3):
            P[i] = max(P[i], get(P, i - k) + ps[i] - ps[i - k + 2])
    return P[n - 1]