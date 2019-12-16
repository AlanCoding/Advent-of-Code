from collections import namedtuple
import copy
import re
import json
from math import gcd


with open(__file__.replace('.py', '.txt')) as f:
    input = f.read()


data = {'problem': input}

data['1'] = """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""  # 31

data['2'] = """9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL"""  # 165

data['3'] = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""

data['4'] = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF"""  # 180697

data['5'] = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""  # 2210736


def ore_multiplier(prod_name, number, production, cache, inventory):
    """Recursive method for any arbitrary species
    finds the number of ORE needed to make it"""
    ct, reactants = production[prod_name]
    # first find the number of ORE needed to run this reaction, as written, once
    if prod_name in cache:
        ore_ct = cache[prod_name]
    else:
        ore_ct = 0
        for reactant in reactants:
            in_ct, name = reactant
            if name == 'ORE':
                ore_ct += in_ct
            else:
                ore_ct += ore_multiplier(name, in_ct, production, cache, inventory)
        cache[prod_name] = ore_ct
        print(f'Need {ore_ct} ORE to make {ct} {prod_name} from: {" ".join(str(entry) for entry in reactants)}.')

    if ct >= number:
        r = ore_ct
    else:
        r = (number // ct) + 1
    print(f'     need {r} ORE to make {number} {prod_name} from known reaction.')
    if prod_name == 'ORE':
        raise Exception('You can only call this on non-ORE species.')
    return r


def solve_problem(input, steps=1):
    # dictionary keyed off reaction product code
    production = {}
    for line in input.split('\n'):
        all_reactants, product_text = line.split(' => ')
        reactant_text = all_reactants.split(', ')
        reactants = []
        for entry in reactant_text:
            ct, name = entry.split(' ')
            reactants.append((int(ct), name))
        product_ct, product_name = product_text.split(' ')
        if product_name in production:
            raise Exception('Multiple routes to product production not supported.')
        production[product_name] = (int(product_ct), reactants)

    # dictionary of how much ore it takes to make something
    cache = {}
    # *cringe* dictionary of how much is in inventory
    inventory = {}

    return ore_multiplier('FUEL', 1, production, cache, inventory)


for name, input in data.items():
    print('')
    r = solve_problem(input)
    print(f'Answer for {name}: {r}')

