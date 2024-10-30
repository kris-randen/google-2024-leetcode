def find_sum_of_two(nums, target, i):
    if len(nums) < 2: return False
    l, r = i + 1, len(nums) - 1
    while l < r:
        if (sm := nums[l] + nums[r]) == target:
            return True
        if sm < target:
            l += 1; continue
        if sm > target:
            r -= 1; continue
    return False

def find_sum_of_three(nums, target):
    if len(nums) < 3: return False
    nums.sort()
    for i in range(len(nums) - 2):
        if find_sum_of_two(nums, target - nums[i], i):
            return True
    return False