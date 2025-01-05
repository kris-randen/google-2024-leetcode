"""

03 Sort Colors

Given an array, colors, which contains a combination of the following three elements:

0 (representing red)

1 (representing white)

2 (representing blue)

Sort the array in place so that the elements of the same color are adjacent, with the colors in the order of red, white, and blue. To improve your problem-solving skills, do not utilize the built-in sort function.


"""


"""

2 Pointers Approach

The key is to understand the invariant. l, f, r are the three pointers. Everything before l is 0, everything beyond r is 2. Now this is not enough. We also need to note that everything starting from l to f - 1 (inclusive) is actually 1. Hence when we find a 0 we swap that with l and increment both l and f because we know what the 0 will get swapped when swapping on the l side is 1. But when we swap a 2 with r we don't know what that element will be there's no guarantee for this from the invariant and hence we only decrement the r pointer and don't increment the f pointer.

"""


def swap(cs, i, j):
    cs[i], cs[j] = cs[j], cs[i]

def sort_colors(cs):
    if (n := len(cs)) < 2: return cs
    l, f, r = 0, 0, n - 1
    while f <= r:
        if cs[f] == 0:
            swap(cs, f, l)
            l += 1; f += 1
        elif cs[f] == 1:
            f += 1
        else:
            swap(cs, f, r)
            r -= 1
    return cs




















