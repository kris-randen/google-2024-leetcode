"""

2787. Ways to Express an Integer as Sum of Powers
Medium

Given two positive integers n and x.

Return the number of ways n can be expressed as the sum of the xth power of unique positive integers, in other words, the number of sets of unique integers [n1, n2, ..., nk] where n = n1x + n2x + ... + nkx.

Since the result can be very large, return it modulo 109 + 7.

For example, if n = 160 and x = 3, one way to express n is n = 23 + 33 + 53.

 

Example 1:

Input: n = 10, x = 2
Output: 1
Explanation: We can express n as the following: n = 32 + 12 = 10.
It can be shown that it is the only way to express 10 as the sum of the 2nd power of unique integers.
Example 2:

Input: n = 4, x = 1
Output: 2
Explanation: We can express n in the following ways:
- n = 41 = 4.
- n = 31 + 11 = 4.

Dynamic Programming Approach

Took a long time to figure this one out.

1. Subproblems:
For a given number n and an exponent x the largest number which can be part of the sum is say p.

We know that

p^x ~ n

which implies

x log p ~ log n

therefore 

log p ~ log n / x

to make sure we don't miss out we'll conservatively take the ceiling therefore

p = 2 ^ (ceil(log n / x))

Once we have p we know for the exponents in the sum we can choose from 1, 2, ... p.

Now this gets very similar to the coin change problem (but not exactly).

So the subproblems are of the type

s[p] = number of ways n can be partitioned as a sum of unique exponents from 1, 2, .., p. aka 1^x, 2^x, 3^x, ... p^x

s(n, x, p) represents the number of partitions of n into exponents chosen from 1, 2, ... p.

2. Relationship

Now the ensemble of partitions can either have p in it or not.

The ones in s(n, x, p) that have p in them

= s(n - p ** x, x, p - 1)

note that once we use p ** x we only allow exponents up to p - 1 since we have already used up p and we want all of them to be unique.

The ones in s(n, x, p) that don't have p in them

= s(n, x, p - 1)

Therefore s(n, x, p) = s(n, x, p - 1) + s(n - p ** x, x, p - 1)

3. Topological Order:

We solve in the decreasing order of p recursively while memoizing using the lru_cache decorator

4. Base Cases

if n == 0 we have perfectly summed it up therefore 

s(0, x, p) = 1 for all x and p

if n < 0 or p < 1 we have shot over the edge and we need to return 0

if p == 1: we return 1 if n == 1 else 0 (note if p == 1 then the only way to break n up is n = 1^x)

5. Original Problem

s(n, x, 2 ** ceil(log n / x))

6. Time Complexity

There are p subproblems and with memoization take O(1) time (2 terms to add) per subproblem.

But since p is represented as a single number as input that takes ~ log p words to represent this is a pseudo-polynomial problem in p-input size which is log p. There for it's exponential in p-input size.


Performance

Runtime 47 ms Beats 100.00%
Memory 36.65 MB Beats 27.32%

"""

from math import log, exp

MOD = 10**9 + 7

@lru_cache(None)
def sumps(n, x, p):
    if n == 0:              return 1
    if n < 0 or p < 1:      return 0
    if p == 1:              return 0 if not n == 1 else 1
    return sumps(n, x, p - 1) + \
           sumps(n - p ** x, x, p - 1)

def num(n, x):
    p = 2 ** ceil(log(n, 2)/x)
    return sumps(n, x, p) % MOD

class Solution:
    def numberOfWays(self, n: int, x: int) -> int:
        return num(n, x)


















