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

