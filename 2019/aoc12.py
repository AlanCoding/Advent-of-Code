from collections import namedtuple
import copy
import re
import json
from math import gcd


with open(__file__.replace('.py', '.txt')) as f:
    input = f.read()


data = {
    'problem': input,
    '1': """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>""",
    '2': """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""
}

# for case 1
# After 10 steps:
# pos=<x= 2, y= 1, z=-3>, vel=<x=-3, y=-2, z= 1>
# pos=<x= 1, y=-8, z= 0>, vel=<x=-1, y= 1, z= 3>
# pos=<x= 3, y=-6, z= 1>, vel=<x= 3, y= 2, z=-3>
# pos=<x= 2, y= 0, z= 4>, vel=<x= 1, y=-1, z=-1>

# for case 2
# After 100 steps:
# pos=<x=  8, y=-12, z= -9>, vel=<x= -7, y=  3, z=  0>
# pos=<x= 13, y= 16, z= -3>, vel=<x=  3, y=-11, z= -5>
# pos=<x=-29, y=-11, z= -1>, vel=<x= -3, y=  7, z=  4>
# pos=<x= 16, y=-13, z= 23>, vel=<x=  7, y=  1, z=  1>
#
# Energy after 100 steps:
# pot:  8 + 12 +  9 = 29;   kin: 7 +  3 + 0 = 10;   total: 29 * 10 = 290
# pot: 13 + 16 +  3 = 32;   kin: 3 + 11 + 5 = 19;   total: 32 * 19 = 608
# pot: 29 + 11 +  1 = 41;   kin: 3 +  7 + 4 = 14;   total: 41 * 14 = 574
# pot: 16 + 13 + 23 = 52;   kin: 7 +  1 + 1 =  9;   total: 52 *  9 = 468
# Sum of total energy: 290 + 608 + 574 + 468 = 1940

use_steps = {
    'problem': 1000,
    '1': 10,
    '2': 100
}


Moon = namedtuple('Point', ['position', 'velocity', 'idx'])


def read_input(input):
    moons = []
    p = re.compile(r'^<x=(?P<x>-?\d+),\sy=(?P<y>-?\d+),\sz=(?P<z>-?\d+)>$')
    for idx, line in enumerate(input.split('\n')):
        m = p.search(line)
        pos = [m.group('x'), m.group('y'), m.group('z')]
        for i, val in enumerate(pos):
            assert val is not None
            pos[i] = int(val)
        moons.append(Moon(pos, [0, 0, 0], idx=idx))
    return moons


def print_data(data):
    print('')
    for moon in data:
        print(f'pos=<x={moon.position[0]}, y={moon.position[1]}, z={moon.position[2]}>,'
              f' vel=<x={moon.velocity[0]}, y={moon.velocity[1]}, z={moon.velocity[2]}>')
    print('')


def sign(x):
    if x <= 0:
        return -1
    else:
        return 1


def energy(moons):
    total = 0
    for moon in moons:
        total += sum(abs(val) for val in moon.position) * sum(abs(val) for val in moon.velocity)
    return total


def solve_problem(input, steps=1):
    moons = read_input(input)

    for step in range(steps):
        old_moons = copy.deepcopy(moons)
        for this in moons:
            for that in old_moons:
                if this.idx == that.idx:
                    continue  # don't gravitate yourself
                # gravity effects
                for k in range(3):
                    if this.position[k] == that.position[k]:
                        continue  # no change
                    this.velocity[k] += sign(that.position[k] - this.position[k])
            # movement
            for k in range(3):
                this.position[k] += this.velocity[k]

    print_data(moons)
    return energy(moons)


for name, input in data.items():
    print('')
    r = solve_problem(input, steps=use_steps[name])
    print(f'Answer for {name}: {r}')


def one_dim_state(moons, k):
    """Returns a vector to represent the state of all x positions
    and all x velocities, or any other index."""
    return (
        tuple(moon.position[k] for moon in moons),
        tuple(moon.velocity[k] for moon in moons)
    )


def part2(input):
    moons = read_input(input)
    start_states = tuple(one_dim_state(moons, k) for k in range(3))
    vector_period = {}

    step = 0
    while len(vector_period) < 3:
        step += 1
        old_moons = copy.deepcopy(moons)
        for this in moons:
            for that in old_moons:
                if this.idx == that.idx:
                    continue  # don't gravitate yourself
                # gravity effects
                for k in range(3):
                    if this.position[k] == that.position[k]:
                        continue  # no change
                    this.velocity[k] += sign(that.position[k] - this.position[k])
            # movement
            for k in range(3):
                this.position[k] += this.velocity[k]
        for k in range(3):
            if one_dim_state(moons, k) == start_states[k]:
                vector_period[k] = step
        if step % 100000 == 0:
            print(f'  step {step}, {vector_period}')
            print('     {}'.format(one_dim_state(moons, k)))
            print('     {}'.format(start_states[k]))

    print('')
    print(json.dumps(vector_period, indent=2))
    # least common multiplier
    d, e, f = (vector_period[0], vector_period[1], vector_period[2])
    de_lcm = (d * e) // gcd(d, e)
    lcm = (de_lcm * f) // gcd(de_lcm, f)
    return lcm


print('')
print('***** PART 2 ******')

for name, input in data.items():
    print('')
    r = part2(input)
    print(f'Answer for {name}: {r}')
