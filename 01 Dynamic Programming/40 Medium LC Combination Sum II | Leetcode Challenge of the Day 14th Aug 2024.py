"""

40. Combination Sum II
Solved
Medium
Given a collection of candidate numbers (candidates) and a target number (target), find all unique combinations in candidates where the candidate numbers sum to target.

Each number in candidates may only be used once in the combination.

Note: The solution set must not contain duplicate combinations.



Example 1:

Input: candidates = [10,1,2,7,6,1,5], target = 8
Output:
[
[1,1,6],
[1,2,5],
[1,7],
[2,6]
]
Example 2:

Input: candidates = [2,5,2,1,2], target = 5
Output:
[
[1,2,2],
[5]
]


"""

from functools import reduce


def combine(c, cs):
    return tuple(sorted((c,) + cs))


def combines(c, css):
    def join(vss, vs): return vss.add(combine(c, vs)) or vss

    return reduce(join, css, set())


def c_sum(cs, t, memo):
    if not cs or t <= 0: return {}
    if cs[0] == t: return {(cs[0],)}
    key = (cs, t)
    if key in memo: return memo[key]
    pr = c_sum(cs[1:], t - cs[0], memo)
    ar = c_sum(cs[1:], t, memo)
    cr = combines(cs[0], pr)
    memo[key] = ar.union(cr)
    return memo[key]
# if not cs or t <= 0:
#     return set()
# if cs[0] == t:
#     return {(cs[0],)}
# key = (cs, t)
# if key in memo:
#     return memo[key]
# pr  = c_sum(cs[1:], t - cs[0], memo)			# When cs[0] is present in the combination
# ar  = c_sum(cs[1:], t, memo)					# When cs[0] is not present in the combintion
# cr  = combines(cs[0], pr)
# memo[key] = reduce(union, [ar, cr])
# return memo[key]		                # Return the union of combinations from both the calls
