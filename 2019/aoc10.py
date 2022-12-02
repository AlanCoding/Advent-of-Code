from fractions import Fraction
from math import atan2, pi
import json


with open(__file__.replace('.py', '.txt')) as f:
    input = f.read()


data = {
    'problem': input,
    '1': """.#..#
.....
#####
....#
...##""",
    '2': """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####""",  # 5,8 with 33 other asteroids detected
    '3': """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.""",  # 1,2 with 35 other asteroids detected
    '4': """.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..""",  # 6,3 with 41 other asteroids detected
    '5': """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""  # 11,13 with 210 other asteroids detected:
}


def sign(number):
    if number == 0:
        return 0
    return number // abs(number)


def get_direction_vector(p1, p2):
    delta_p = tuple(p2[j] - p1[j] for j in range(2))
    if any(delta_p[j] == 0 for j in range(2)):
        direction = tuple(sign(delta_p[j]) for j in range(2))
    else:
        factor = abs(delta_p[1] // Fraction(delta_p[1], delta_p[0]).numerator)
        direction = tuple(delta_p[j] // factor for j in range(2))
    return direction


def visible_directions(p, asteroids):
    directions = set()
    for p2 in asteroids:
        if p == p2:
            continue  # do not count yourself
        direction = get_direction_vector(p, p2)
        directions.add(direction)
    return directions


def asteroids_from_input(input):
    asteroids = set()
    for y, line in enumerate(input.split('\n')):
        for x, character in enumerate(line):
            if character == '#':
                asteroids.add((x, y))

    return frozenset(asteroids)  # lock down modifications


def solve_problem(input):
    asteroids = asteroids_from_input(input)

    max_see = 0
    for this_loc in asteroids:
        directions = visible_directions(this_loc, asteroids)
        ct = len(directions)
        if ct > max_see:
            max_see = ct
            loc = this_loc

    return max_see, loc


for name, input in data.items():
    print('')
    see_ct, location = solve_problem(input)
    loc_str = ','.join([str(p) for p in location])
    print(f'Answer for {name}: '
          f'Best is {loc_str} with {see_ct} other asteroids detected')


print('')
print('***** PART 2 ******')


def angle_from_vertial(p):
    # the "up" in this case is (0, -1), we want to count up from there
    # going in the clockwise direction
    # ratio = -1 * p[0] * p[1]
    return (atan2(p[1], p[0]) + pi / 2.) % (2 * pi)


print('')
print('testing angle function')
print('These should all increase in order for sorting to be right')
print('dead up {}'.format(angle_from_vertial((0, -1))))
print('Upper right {}'.format(angle_from_vertial((1, -1))))
print('dead right {}'.format(angle_from_vertial((1, 0))))
print('lower right {}'.format(angle_from_vertial((1, 1))))
print('lower left {}'.format(angle_from_vertial((-1, 1))))
print('Upper left {}'.format(angle_from_vertial((-1, -1))))



def mag(p):
    return (p[0]**2 + p[1]**2)**(0.5)


def part2(loc, input, shots=200):
    asteroids = asteroids_from_input(input)
    asteroids_by_direction = {}
    for pt in asteroids:
        direction = get_direction_vector(loc, pt)
        if direction in asteroids_by_direction:
            asteroids_by_direction[direction].append(pt)
        else:
            asteroids_by_direction[direction] = [pt]

    for dir in list(asteroids_by_direction.keys()):
        asteroids_by_direction[dir] = sorted(asteroids_by_direction[dir], key=mag)

    directions_and_asteroids = [(dir, roids) for dir, roids in asteroids_by_direction.items()]

    directions_and_asteroids = sorted(directions_and_asteroids, key=lambda entry: angle_from_vertial(entry[0]))

    Ndirs = len(directions_and_asteroids)
    pos = 0
    for shot in range(shots):
        targets = []
        local_ct = 0
        while not targets:
            targets = directions_and_asteroids[pos][1]
            pos += 1
            if pos >= Ndirs:
                pos = 0
            local_ct += 1
            if local_ct > Ndirs * 2:
                print('\n'.join([str(t) for t in directions_and_asteroids]))
                print(f'Position {pos}, shot {shot}')
                raise RuntimeError('Iteration problem')
        pt = targets.pop()

    return pt


for name, input in data.items():
    print('')
    see_ct, location = solve_problem(input)
    if name in ('problem', '5'):
        shots = 201
    else:
        shots = input.count('#') // 2
    r = part2(location, input, shots=shots)
    print(f'Answer for {name}: {shots}th asteroid is {r}')
    print('  multiply its X coordinate by 100 and then add its Y coordinate {}'.format(r[0] * 100 + r[1]))

