import json
import sys


with open(__file__.replace('.py', '.txt')) as f:
    problem = f.read()


data = {
    'problem': problem,
    '1': '1,0,0,0,99',
    '2': '2,3,0,3,99',
    '3': '2,4,4,5,99,0',
    '4': '1,1,1,4,99,5,6,0,99'
}

# for part 1
replacers = {
    'problem': (12, 2)
}

pretty = True


class UnrecognizedProcessCode(Exception):
    pass


def solve_problem(input, rep1=None, rep2=None):

    # An Intcode program is a list of integers separated by commas (like 1,0,0,3,99).
    numbers = [int(element) for element in input.split(',')]

    if pretty:
        # pretty-print
        if len(numbers) < 10:
            print(json.dumps(numbers, indent=2))
        else:
            print('a-lot-of-numbers')

    # before running the program
    if rep1 is not None:
        # replace position 1 with the value 12 and
        numbers[1] = rep1
    if rep2 is not None:
        # replace position 2 with the value 2.
        numbers[2] = rep2

    i = 0

    while True:
        val = numbers[i]
        # print('start ' + str((i, val)))
        if val == 99:
            break
        if val not in (1, 2):
            raise UnrecognizedProcessCode(f'Could not process code {val}')
        p1, p2, outp = numbers[i+1:i+4]
        # print((p1, p2, outp))
        in1 = numbers[p1]
        in2 = numbers[p2]
        # print(outp)
        if val == 1:
            numbers[outp] = in1 + in2
        elif val == 2:
            numbers[outp] = in1 * in2
        i += 4

    # What value is left at position 0 after the program halts?
    return numbers[0]


# part 1
if sys.argv[-1] in data.keys():
    input = data[sys.argv[-1]]
    rep1, rep2 = replacers.get(name, (None, None))
    r = solve_problem(input, rep1=rep1, rep2=rep2)
    print(f'FINAL ANSWER: {r}')

else:
    for name, input in data.items():
        print('')
        print(f'Solving case {name}')
        rep1, rep2 = replacers.get(name, (None, None))
        r = solve_problem(input, rep1=rep1, rep2=rep2)
        print(f'FINAL ANSWER: {r}')


pretty = False

# part 2
expect = 19690720

# for N in range(100000000):
#     for other in range(N):
#         # In this program, the value placed in address 1 is called the noun,
#         # and the value placed in address 2 is called the verb.
#         try:
#             r = solve_problem(input, rep1=N, rep2=other)
#             if r == expect:
#                 # What is 100 * noun + verb?
#                 ans = 100 * N * other
#                 raise Exception(f'PART 2 {ans}')
#         except (UnrecognizedProcessCode, IndexError):
#             pass
# 
#         try:
#             r = solve_problem(input, rep1=other, rep2=N)
#             if r == expect:
#                 # What is 100 * noun + verb?
#                 ans = 100 * N * other
#                 raise Exception(f'PART 2 {ans}')
#         except (UnrecognizedProcessCode, IndexError):
#             pass
#     print(f'Iterating to next, {N}')

input = data['problem']

N = len(input.split(','))


# In this program, the value placed in address 1 is called the noun,
# and the value placed in address 2 is called the verb.
for noun in range(N):
    for verb in range(N):
        try:
            r = solve_problem(input, rep1=noun, rep2=verb)
            if r == expect:
                # What is 100 * noun + verb?
                ans = 100 * noun + verb
                raise Exception(f'PART 2 {ans}')
        except (UnrecognizedProcessCode, IndexError):
            pass

    print(f'Iterating to next noun, {noun}')

