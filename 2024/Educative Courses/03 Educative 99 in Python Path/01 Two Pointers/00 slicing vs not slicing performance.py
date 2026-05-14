import time
import random

def two_sum_slice(vs, t):
    """Uses slicing to remove one element before calling two_sum."""
    n = len(vs)
    for i in range(n):
        arr = vs[:i] + vs[i+1:]  # slicing (and concatenating)
        if two_sum(arr, t - vs[i]):
            return True
    return False

def two_sum_skip(vs, t):
    """Avoids slicing by skipping an index in the two_sum logic."""
    n = len(vs)
    for i in range(n):
        if two_sum_no_slice(vs, t - vs[i], i):
            return True
    return False

def two_sum(arr, t):
    """Standard two-pointer two_sum on a sorted list."""
    l, r = 0, len(arr) - 1
    while l < r:
        s = arr[l] + arr[r]
        if s == t:
            return True
        elif s < t:
            l += 1
        else:
            r -= 1
    return False

def two_sum_no_slice(vs, t, skip_index):
    """Two-pointer, but skip `skip_index` manually."""
    l, r = 0, len(vs) - 1
    while l < r:
        if l == skip_index:
            l += 1
            continue
        if r == skip_index:
            r -= 1
            continue
        s = vs[l] + vs[r]
        if s == t:
            return True
        elif s < t:
            l += 1
        else:
            r -= 1
    return False

def three_sum_slice(vs, t):
    """Three-sum using the slice-based approach."""
    vs.sort()
    # Quick checks
    if t < vs[0] + vs[1] + vs[2] or t > vs[-1] + vs[-2] + vs[-3]:
        return False
    return two_sum_slice(vs, t)

def three_sum_skip(vs, t):
    """Three-sum using the no-slice approach."""
    vs.sort()
    if t < vs[0] + vs[1] + vs[2] or t > vs[-1] + vs[-2] + vs[-3]:
        return False
    return two_sum_skip(vs, t)

# ---------------
# BENCHMARK CODE
# ---------------
def benchmark(num_tests=1000, list_size=200):
    slice_total_time = 0
    skip_total_time = 0

    for _ in range(num_tests):
        # Generate random data
        vs = [random.randint(0, 500) for __ in range(list_size)]
        t = random.randint(0, 1500)

        start = time.time()
        _ = three_sum_slice(vs[:], t)
        slice_total_time += (time.time() - start)

        start = time.time()
        _ = three_sum_skip(vs[:], t)
        skip_total_time += (time.time() - start)

    print(f"Slice-based total time: {slice_total_time:.6f} seconds")
    print(f"Skip-based total time:  {skip_total_time:.6f} seconds")

if __name__ == "__main__":
    benchmark(num_tests=345, list_size=20000)