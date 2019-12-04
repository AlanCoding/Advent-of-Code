


def meets_criteria(number):
    digits = [int(e) for e in str(number)]
    if len(digits) != 6:
        return False
    last = digits[0]
    has_repeating = False
    for digit in digits[1:]:
        if digit < last:
            return False
        if digit == last:
            has_repeating = True
        last = digit
    return has_repeating


input = '152085-670283'

low, high = [int(e) for e in input.split('-')]


print('Examples')

EXAMPLES = (
    111111,  # meets these criteria (double 11, never decreases).
    223450,  # does not meet these criteria (decreasing pair of digits 50).
    123789,  # does not meet these criteria (no double).    
)

for ex in EXAMPLES:
    out = meets_criteria(ex)
    print(f'Example {ex}, outcome: {out}')


ct = 0
for i in range(low, high + 1):  # should it be inclusive????
    if meets_criteria(i):
        ct += 1
    if i % 100000 == 0:
        print(f'Iterating on {i}, at count {ct}')


print(f'Answer: {ct}')

# guesses
# 16775
# 43596
# 1764 - correct
