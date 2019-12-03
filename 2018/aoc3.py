import os

with open(__file__.replace('.py', '.txt')) as f:
    seq = f.read()

words = seq.split('\n')


class Square:
    def __init__(self, word):
        word, dim_word = word.rsplit(' ', 1)
        self.width, self.height = [int(num_str) for num_str in dim_word.split('x')]
        self.id, cord_word = word.strip(' :#').split(' @ ')
        self.x, self.y = [int(num_str) for num_str in cord_word.split(',')]
        self.x2 = self.x + self.width
        self.y2 = self.y + self.height
        self.conflicting = False


max_x = 0
max_y = 0


for word in words:
    s = Square(word)
    if s.x2 > max_x:
        max_x = s.x2
    if s.y2 > max_y:
        max_y = s.y2

print ' max cords'
print (max_x, max_y)


canvas = [[0 for i in range(max_y)] for j in range(max_x)]
dup = 0
squares = [Square(word) for word in words]


for s in squares:
    for i in range(s.x, s.x2):
        for j in range(s.y, s.y2):
            if canvas[i][j] == 1:
                dup += 1
            canvas[i][j] += 1


print 'Duplicated cells'
print dup

print 'Total cells'
print max_x*max_y

# --- part 2 ---

for s in squares:
    for i in range(s.x, s.x2):
        for j in range(s.y, s.y2):
            if canvas[i][j] > 1:
                s.conflicting = True
                break
        if s.conflicting:
            break


for s in squares:
    if not s.conflicting:
        print 'Non-conflicting square:'
        print s.id

