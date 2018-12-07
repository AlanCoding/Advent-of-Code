import os

with open(os.path.join(os.path.dirname(__file__), 'numbers.txt')) as f:
    seq = f.read()

adjs = [int(l) for l in seq.split('\n')]

# print adjs

freq = 0

seen = set([0])

seen_twice = None

while True:
    for adj in adjs:
        freq += int(adj)
        if freq in seen:
            seen_twice = freq
            break
        seen.add(freq)
    if seen_twice is not None:
        break

# print seen
print freq
print sum(adjs)
