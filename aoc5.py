import os
from copy import copy

with open(__file__.replace('.py', '.txt')) as f:
    seq = f.read()

debug = False

# seq = 'wWuUJjXxqQrqQmKBzZbZzLlkWNqQ'
# debug = True

print len(seq)

orig = copy(seq)

def is_match(c1, c2):
    if c1.isupper() == c2.isupper():
        if debug:
            print ' not hit: ' + c1 + c2
        return False
    return bool(c1.lower() == c2.lower())

for c in 'abcdefghijklmnopqrstuvwxyz':
    seq = orig.replace(c, '').replace(c.upper(), '')

    while True:
        new = ''
        changed = False
        live = False
        for i in range(len(seq)):
            if live:
                live = False
                continue  # is second of matching sequence
            j = i + 1
            c1 = seq[i]
            if j >= len(seq):
                if debug:
                    print 'reached end'
                new += c1
                break
            c2 = seq[j]
            if not is_match(c1, c2):
                new += c1
                continue
            if debug:
                print 'matched: ' + c1 + c2
            live = True
            changed = True
            new += seq[j+1:]
            break
                
        seq = new
        # print len(seq)
        if debug:
            print ' new sequence:'
            print seq
        if not changed:
            break

    print c + ': ' + str(len(seq))

    # print seq

# method1: 9172
# method2: 9172

# c: 8758
