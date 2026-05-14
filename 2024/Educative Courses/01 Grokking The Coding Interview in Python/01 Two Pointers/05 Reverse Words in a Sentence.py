"""

Given a sentence, reverse the order of its words without affecting the order of letters within the given word.

"""

def swap(vs, i, j):
    vs[i], vs[j] = vs[j], vs[i]

def reverse(vs):
    if not (n := len(vs)): return []
    l, r = 0, n - 1
    while l < r:
        swap(vs, l, r)
        l += 1; r -= 1
    return vs

def reverse_words(sentence):
    return ' '.join(reverse(sentence.split()))

if __name__ == '__main__':
    sentence = 'Why is this not working?'
    print(reverse_words(sentence))
