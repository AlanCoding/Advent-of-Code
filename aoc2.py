import os

with open(__file__.replace('.py', '.txt')) as f:
    seq = f.read()

words = seq.split('\n')

twos = 0
threes = 0

for w in words:
    chars = set(c for c in w)
    is_two = False
    is_three = False
    for c in chars:
        ct = w.count(c)
        if ct == 2:
            is_two = True
        elif ct == 3:
            is_three = True
    if is_two:
        twos +=1
    if is_three:
        threes += 1

print twos
print threes

print 'sum'
print twos*threes

for w in words:
    for wp in words:
        same = 0
        for i, c in enumerate(w):
            if wp[i] == c:
                same += 1
        if same == len(w) - 1:
            print 'words %s and %s work ' % (w, wp)

