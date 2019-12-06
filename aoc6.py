import sys
import json


with open(__file__.replace('.py', '.txt')) as f:
    problem = f.read()


data = {
    'problem': problem,
    'example': """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""  # should give 42
}


def solve_problem(input):
    parents = {}
    for i, line in enumerate(input.split('\n')):
        about, object = line.split(')')
        parents[object] = about

    orbit_counts = {'COM': 0}

    for object in tuple(parents.keys()):
        stack = [object]
        while stack[-1] not in orbit_counts:
            stack.append(parents[stack[-1]])
        known = orbit_counts[stack.pop()]
        stack.reverse()
        for thing in stack:
            orbit_counts[thing] = orbit_counts[parents[thing]] + 1
        # current_ct = orbit_counts[about]
        # the_ct = current_ct + 1
        # orbit_counts[object] = the_ct

    return sum(orbit_counts.values())

        # if object in orbit_counts:
        #     raise Exception(f'{object} orbits multiple things, line {i}')
        # elif about not in orbit_counts:
        #     raise Exception(f'Object {object} orbits unknown thing {about}, line {i}')
        #     # orbit_counts[object] = 0
        #     continue


# part 1
if sys.argv[-1] in data.keys():
    scenarios = (sys.argv[-1],)
else:
    scenarios = tuple(data.keys())


for scenario in scenarios:
    input = data[scenario]
    r = solve_problem(input)
    print(f'FINAL ANSWER: {r}')


# 932, too low

