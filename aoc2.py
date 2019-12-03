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

def solve_problem(input):

    # An Intcode program is a list of integers separated by commas (like 1,0,0,3,99).
    numbers = [int(element) for element in input.split(',')]

    # pretty-print
    if len(numbers) < 10:
        print(json.dumps(numbers, indent=2))
    else:
        print('a-lot-of-numbers')
        # before running the program
        # replace position 1 with the value 12 and
        numbers[1] = 12
        # replace position 2 with the value 2.
        numbers[2] = 2

    i = 0

    while True:
        val = numbers[i]
        # print('start ' + str((i, val)))
        if val == 99:
            break
        if val not in (1, 2):
            raise Exception(f'Could not process code {val}')
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
    print(f'FINAL ANSWER: {numbers[0]}')


if sys.argv[-1] in data.keys():
    input = data[sys.argv[-1]]
    solve_problem(input)

else:
    for name, input in data.items():
        print('')
        print(f'Solving case {name}')
        solve_problem(input)

