

# A for Rock, B for Paper, and C for Scissors

# The score for a single round is the score for the shape you selected
# (1 for Rock, 2 for Paper, and 3 for Scissors)
# plus the score for the outcome of the round
# (0 if you lost, 3 if the round was a draw, and 6 if you won).


with open(__file__.replace('.py', '.txt')) as f:
    input = f.read()


total_score = 0

WIN = [
    ('A', 'B'),  # my paper beats elf rock
    ('B', 'C'),  # my scissors beats elf paper
    ('C', 'A')   # my rock beats elf scissors
]


for line in input.strip().split('\n'):
    elf_play, my_play_xyz = line.split(' ')
    my_play = {
        'X': 'A',
        'Y': 'B',
        'Z': 'C'
    }[my_play_xyz]
    total_score += {
        'A': 1,
        'B': 2,
        'C': 3
    }[my_play]
    if elf_play == my_play:  # draw
        total_score += 3
        continue
    if (elf_play, my_play) in WIN:
        total_score += 6
    else:
        pass

print(f'total_score {total_score}')

# 9870 too low (forgot to count the score for what I played)
# 15632 correct

# X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win.


total_score = 0

WIN_MAPPING = {}

for elf_play, my_play in WIN:
    WIN_MAPPING[elf_play] = my_play

LOSE_MAPPING = {}

for elf_play, my_play in WIN:
    LOSE_MAPPING[my_play] = elf_play

for line in input.strip().split('\n'):
    elf_play, my_play_xyz = line.split(' ')
    my_play = {
        'X': LOSE_MAPPING[elf_play],  # lose
        'Y': elf_play,  # draw
        'Z': WIN_MAPPING[elf_play]  # win
    }[my_play_xyz]
    total_score += {
        'A': 1,
        'B': 2,
        'C': 3
    }[my_play]
    if elf_play == my_play:  # draw
        total_score += 3
        continue
    if (elf_play, my_play) in WIN:
        total_score += 6
    else:
        pass


print(f'total_score {total_score}')
