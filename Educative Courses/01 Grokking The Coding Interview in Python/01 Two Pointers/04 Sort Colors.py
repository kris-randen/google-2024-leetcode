"""

Statement
Given an array, colors, which contains a combination of the following three elements:

0(representing red)

1(representing white)

2(representing blue)

Sort the array in place so that the elements of the same color are adjacent, with the colors in the order of red, white, and blue. To improve your problem-solving skills, do not utilize the built-in sort function.

"""

def swap(cs, i, j):
  cs[i], cs[j] = cs[j], cs[i]

def sort_colors(cs):
    if (n := len(cs)) < 2: return cs
    i, l, r = 0, 0, n - 1
    while i <= r:
      if cs[i] == 0:
        swap(cs, l, i)
        l += 1; i += 1
      elif cs[i] == 1:
        i += 1
      else:
        swap(cs, i, r)
        r -= 1
    return cs