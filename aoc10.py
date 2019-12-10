from fractions import Fraction


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


def visible_directions(p, asteroids):
    directions = set()
    for p2 in asteroids:
        if p == p2:
            continue  # do not count yourself
        delta_p = tuple(p2[j] - p[j] for j in range(2))
        if any(delta_p[j] == 0 for j in range(2)):
            direction = tuple(sign(delta_p[j]) for j in range(2))
        else:
            factor = abs(delta_p[1] // Fraction(delta_p[1], delta_p[0]).numerator)
            direction = tuple(delta_p[j] // factor for j in range(2))
        directions.add(direction)
    return directions


def solve_problem(input):
    asteroids = set()
    for y, line in enumerate(input.split('\n')):
        for x, character in enumerate(line):
            if character == '#':
                asteroids.add((x, y))

    asteroids = frozenset(asteroids)  # lock down modifications
    print('  total asteroid count: {0}'.format(len(asteroids)))

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
