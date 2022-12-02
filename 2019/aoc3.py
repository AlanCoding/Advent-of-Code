import sys
import json


with open(__file__.replace('.py', '.txt')) as f:
    problem = f.read()


data = {
    'problem': problem,
    # distance 159
    # part 2: 610
    '1': 'R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83',
    # distance 135
    # part 2: 410
    '2': 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7'
}


def part1(input, part2=False):
    texts = input.split('\n')
    both_moves = [text.split(',') for text in texts]
    both_positions = []
    both_travels = []
    for moves in both_moves:
        cur = [0, 0]
        travels = {tuple(cur): 0}
        travel = 0
        positions = [tuple(cur)]
        for move in moves:
            dir = move[0]
            val = int(move[1:])
            for i in range(val):
                if dir == 'R':
                    cur[0] += 1
                elif dir == 'L':
                    cur[0] -= 1
                elif dir == 'U':
                    cur[1] += 1
                elif dir == 'D':
                    cur[1] -= 1
                travel += 1
                tp_cr = tuple(cur)
                positions.append(tp_cr)
                if tp_cr not in travels:
                    travels[tp_cr] = travel
        both_positions.append(positions)
        both_travels.append(travels)
    print('Positions of wires')
    if len(both_positions[0]) < 100:
        print(json.dumps(both_positions))
    else:
        print('a lot of positions')
    crossings = []
    position_blob = [set(positions) for positions in both_positions]
    for pos in both_positions[0][1:]:
        # if pos == (0, 0):
        #     continue
        if pos in position_blob[1]:
            crossings.append(pos)
    if not part2:
        print('crossings')
        print(crossings)
        dist = sum(abs(pos) for pos in crossings[0])
        for point in crossings:
            this_dist = sum(abs(pos) for pos in point)
            if this_dist < dist:
                dist = this_dist
        return dist
    else:
        length = 100000
        for point in crossings:
            t1 = both_travels[0][point]
            t2 = both_travels[1][point]
            if t1 + t2 < length:
                length = t1 + t2
        return length


# part 1
for name, input in data.items():
    print('')
    print(f'Running scenario {name}')
    r = part1(input)
    print(f'Output: {r}')

# part 2
print('')
print('******* PART 2 *******')
for name, input in data.items():
    print('')
    print(f'Running scenario {name}')
    r = part1(input, part2=True)
    print(f'Output: {r}')
