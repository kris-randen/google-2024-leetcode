"""

04. 3 Sum



Statement
Given an array of integers, nums, and an integer value, target, determine if there are any three integers in nums whose sum is equal to the target, that is, nums[i] + nums[j] + nums[k] == target. Return TRUE if three such integers exist in the array. Otherwise, return FALSE.

Note: A valid triplet consists of elements with distinct indexes. This means, for the triplet nums[i], nums[j], and nums[k], i 

"""

def two_sum(vs, t):
    l, r = 0, len(vs) - 1
    while l < r:
        if (s := vs[l] + vs[r]) == t: return True
        if s < t: l += 1
        if s > t: r -= 1
    return False

def three_sum(vs, t):
    if t < sum(vs[:3]) or \
       t > sum(vs[-3:]): return False

    for i in range(len(vs)):
        if two_sum(vs[:i] + vs[i + 1:], t - vs[i]): return True

    return False

def find_sum_of_three(vs, t):
    return three_sum(sorted(vs), t)






