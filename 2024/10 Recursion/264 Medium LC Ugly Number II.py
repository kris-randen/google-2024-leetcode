"""

264. Ugly Number II
Medium
Topics
Companies
Hint
An ugly number is a positive integer whose prime factors are limited to 2, 3, and 5.

Given an integer n, return the nth ugly number.



Example 1:

Input: n = 10
Output: 12
Explanation: [1, 2, 3, 4, 5, 6, 8, 9, 10, 12] is the sequence of the first 10 ugly numbers.
Example 2:

Input: n = 1
Output: 1
Explanation: 1 has no prime factors, therefore all of its prime factors are limited to 2, 3, and 5.


Constraints:

1 <= n <= 1690
Seen this question in a real interview before?
1/5
Yes
No
Accepted
397.4K
Submissions
834.4K
Acceptance Rate
47.6%


"""

from functools import reduce

def pf(n, p):
    if n % p != 0: return 0, n
    c, m = pf(n // p, p)
    return 1 + c, m

def expf(n, p):
    if not n % p == 0: return 0
    return 1 + expf(n // p, p)

def resf(n, p):
    if not n % p == 0: return n
    return resf(n // p, p)

# def ugly(n):
#     return reduce(resf, [2, 3, 5], n) == 1

def nth_ugly(n):
    c, s = 0, 0
    while c < n:
        s += 1
        if ugly(s): c += 1
    return s

import math
from bisect import bisect_left

def ugly_next(us):
    un = float('inf'); ps = [2, 3, 5]
    for p in ps:
        ceil = math.ceil(us[-1] / p) if us[-1] % p != 0 else (us[-1] // p) + 1
        ind = bisect_left(us, ceil)
        un = min(us[ind] * p, un)
    return un

def ugly_n(n):
    ps = [0, 1]
    if n < 2: return ps[n]
    dp = ps
    for i in range(2, n + 1):
        dp += [ugly_next(dp)]
    return dp[n]

if __name__ == '__main__':
    from itertools import count, islice


    def resn(n, p):
        if n % p != 0: return n
        return resn(n // p, p)


    """
    Ugly Number
    If the residue after eliminating the exponents 
    of primes ps is 1 the number is ugly.
    """

    def isugly(n, ps=[2, 3, 5]):
        return reduce(resn, ps, n) == 1


    def nth(generator, n):
        return next(
            islice(generator, n, n + 1)
        )


    def ugly(n):
        return nth(
            filter(isugly, count(1)), n - 1
        )

    from itertools import count


    def sieve(nums):
        p = next(nums)
        yield p
        yield from sieve(x for x in nums if not x % p == 0)


    def primes():
        return sieve(count(2))


    def nps(n):
        gen, ps = primes(), []
        while (m := next(gen)) < n:
            ps += [m]
        return ps

    gen = primes()
    print([next(gen) for _ in range(10)])
    print(list(nps(25)))

