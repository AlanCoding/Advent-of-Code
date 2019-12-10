from itertools import chain


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


def can_see(p1, p2, asteroids):
    delta_p = tuple(p2[j] - p1[j] for j in range(2))
    for (j, k) in ((1, 0), (0, 1)):
        if delta_p[j] == 0:
            if delta_p[k] == 0:
                return False  # do not count self
            continue
        sign = delta_p[j] // abs(delta_p[j])
        # loop over all candidate fractions
        for delta_j in range(sign, delta_p[j], sign):
            if abs(delta_p[k] * delta_j) % abs(delta_p[j]) != 0:
                continue  # fraction did not divide other dimension, not in center
            delta_k = (delta_p[k] * delta_j) // delta_p[j]  # no remainder
            this_point = [None for i in range(2)]
            this_point[j] = p1[j] + delta_j
            this_point[k] = p1[k] + delta_k
            if tuple(this_point) in asteroids:
                return False

    # if delta_p[0] == 0:
    #     if delta_p[1] == 0:
    #         return False  # do not count self
    #     y_sign = abs(delta_p[1]) // delta_p[1]
    #     for y in range(p1[1] + y_sign, p2[1], y_sign):
    #         if (p1[0], y) in asteroids:
    #             return False
    # else:
    #     # loop through all (x, y) points on straight line
    #     x_sign = abs(delta_p[0]) // delta_p[0]
    #     for x in range(p1[0] + x_sign, p2[0], x_sign):
    #         if abs(delta_p[1] * (x - p1[0])) % abs(delta_p[0]) != 0:
    #             continue  # did not pass through center of box
    #         delta_y = ((delta_p[1]) * (x - p1[0])) // (delta_p[0])
    #         y = p1[1] + delta_y
    #         if (x, y) in asteroids:
    #             return False
    return True


def visible_count(p, asteroids):
    ct = 0
    for p2 in asteroids:
        if can_see(p, p2, asteroids):
            ct += 1
    return ct


def solve_problem(input):
    asteroids = set()
    for y, line in enumerate(input.split('\n')):
        for x, character in enumerate(line):
            if character == '#':
                asteroids.add((x, y))

    asteroids = frozenset(asteroids)  # lock down modifications
    print('  total asteroid count: {0}'.format(len(asteroids)))

    # print(asteroids)
    max_see = 0
    for this_loc in asteroids:
        ct = visible_count(this_loc, asteroids)
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
