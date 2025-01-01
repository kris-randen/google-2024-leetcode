"""

983. Minimum Cost For Tickets
Medium

You have planned some train traveling one year in advance. The days of the year in which you will travel are given as an integer array days. Each day is an integer from 1 to 365.

Train tickets are sold in three different ways:

a 1-day pass is sold for costs[0] dollars,
a 7-day pass is sold for costs[1] dollars, and
a 30-day pass is sold for costs[2] dollars.
The passes allow that many days of consecutive travel.

For example, if we get a 7-day pass on day 2, then we can travel for 7 days: 2, 3, 4, 5, 6, 7, and 8.
Return the minimum number of dollars you need to travel every day in the given list of days.

 

Example 1:

Input: days = [1,4,6,7,8,20], costs = [2,7,15]
Output: 11
Explanation: For example, here is one way to buy passes that lets you travel your travel plan:
On day 1, you bought a 1-day pass for costs[0] = $2, which covered day 1.
On day 3, you bought a 7-day pass for costs[1] = $7, which covered days 3, 4, ..., 9.
On day 20, you bought a 1-day pass for costs[0] = $2, which covered day 20.
In total, you spent $11 and covered all the days of your travel.
Example 2:

Input: days = [1,2,3,4,5,6,7,8,9,10,30,31], costs = [2,7,15]
Output: 17
Explanation: For example, here is one way to buy passes that lets you travel your travel plan:
On day 1, you bought a 30-day pass for costs[2] = $15 which covered days 1, 2, ..., 30.
On day 31, you bought a 1-day pass for costs[0] = $2 which covered day 31.
In total, you spent $17 and covered all the days of your travel.
 

Constraints:

1 <= days.length <= 365
1 <= days[i] <= 365
days is in strictly increasing order.
costs.length == 3
1 <= costs[i] <= 1000

Performance

Runtime 0 ms Beats 100.00%
Memory 17.72 MB Beats 29.23%

"""

"""

Dynamic Programming Approach

We maintain the dp array as the cost at each calendar day starting at day 0 going up to the last day of travel ds[-1]. 

cost at day d = dp[d] is

a. if d is not in the travel days then it's the same as previous day.
b. otherwise we take the minimum of 
    i.   dp[d - 1]  + cs[0] (previous day's cost + single day ticket)
    ii.  dp[d - 7]  + cs[1] (cost 8 days ago + weekly ticket)
    iii. dp[d - 30] + cs[2] (cost 31 days ago + monthly ticket)

But this assumes that it can't be profitable to use the weekly or the monthly ticket before day 7 and day 30 respectively and that's simply not true. If the cost of a weekly ticket is say the same as 3 daily tickets it makes sense to use the weekly ticket even after 4 continuous days of travel. In fact if the weekly ticket is less expensive than the daily ticket (which happens to be true in one of the test cases which violated the false assumption of monotonicity of the increasing ticket prices) it makes sense to always use weekly ticket instead of using a daily ticket.

So even in the first 7 and 30 days we do check if it's profitable to insted buy the weekly or the monthly ticket on day 1

The key insight here is to keep track of all calendar days as the weekly and monthly tickets are valid for a week and 30 days since the date of purchase.

"""

def cost(ds, cs):
    dp, sd = [0] * ((ld := ds[-1]) + 1), set(ds)
    for d in range(1, ld + 1):
        if d not in sd: 
            dp[d] = dp[d - 1]
        else:
            dp[d] = min(
                        (dp[d - 1]) + cs[0], 
                        (dp[d - 7]  if d >= 7  else dp[0]) + cs[1], 
                        (dp[d - 30] if d >= 30 else dp[0]) + cs[2]
                       )
    return dp[ld]



































