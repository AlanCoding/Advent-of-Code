import sys
import json


with open(__file__.replace('.py', '.txt')) as f:
    input = f.read()


def solve_problem(input, width=25, height=6):
    pixels = [int(e) for e in input]

    image_size = width * height
    assert len(pixels) % image_size == 0

    image_ct = len(pixels) // image_size
    print(f'There are {image_ct} images in this file')

    low_count = image_size
    product = 0
    for i in range(image_ct):
        offset = i * image_size
        image = pixels[offset:offset + image_size]
        if image.count(0) < low_count:
            low_count = image.count(0)
            product = image.count(2) * image.count(1)

    assert low_count != image_size

    return product


print()
r = solve_problem(input)
print(f'FINAL ANSWER: {r}')

print('')
print('******* PART 2 *******')


def part2(input, width=25, height=6):
    pixels = [int(e) for e in input]

    image_size = width * height
    assert len(pixels) % image_size == 0

    image_ct = len(pixels) // image_size
    print(f'There are {image_ct} images in this file')

    result_image = [2 for i in range(image_size)]
    for i in range(image_ct):
        offset = i * image_size
        image = pixels[offset:offset + image_size]
        for idx, color in enumerate(image):
            if color == 2 or result_image[idx] != 2:
                continue
            result_image[idx] = color

    for i in range(height):
        offset = i * width
        print(''.join([
            str(ichr) if ichr != 0 else ' '
            for ichr in result_image[offset:offset + width]
        ]))


example = '0222112222120000'


part2(example, height=2, width=2)

print('\n'*2)

part2(input)

# 6ZKJY, wrong
# GZKJY
