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


pretty = False


def ore_multiplier(prod_name, number, production, inventory):
    ct, reactants = production[prod_name]
    warehouse_has = inventory.get(prod_name, 0)

    # do we need to run this reaction once or more?
    this_needs = number - warehouse_has

    # Use what we already have in stock
    if this_needs <= 0:
        if pretty:
            print(f'Using available {number} of available {warehouse_has} of {prod_name}')
        inventory[prod_name] -= number
        return 0

    # round up if division has a remainder
    runs = (this_needs // ct) + int(this_needs % ct > 0)

    ore_ct = 0
    new_ore = 0
    for reactant in reactants:
        in_ct, name = reactant
        if name == 'ORE':
            ore_ct += in_ct * runs
            new_ore += in_ct * runs
        else:
            ore_ct += ore_multiplier(name, in_ct * runs, production, inventory)
    if pretty:
        print(f'Need {ore_ct} ORE ({new_ore} local) to make {runs * ct} {prod_name} in {runs} runs from: {" ".join(str(entry) for entry in reactants)}.')

    produced = runs * ct
    warehouse_has_new = inventory.get(prod_name, 0)
    if warehouse_has != warehouse_has_new and pretty:
        print(f'   warehouse stores changed while running sub-reactions {warehouse_has}->{warehouse_has_new} for {prod_name}')
    inventory[prod_name] = warehouse_has_new + produced - number
    if inventory[prod_name] and pretty:
        print(f'   saved {inventory[prod_name]} leftover {prod_name}, prior amount was {warehouse_has_new}')
    if inventory[prod_name] < 0:
        raise Exception(f'Something went wrong, on {prod_name}, inventory {inventory[prod_name]}')

    if prod_name == 'ORE':
        raise Exception('You can only call this on non-ORE species.')
    return ore_ct


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

    # *cringe* dictionary of how much is in inventory
    inventory = {}

    return ore_multiplier('FUEL', 1, production, inventory)


for name, input in data.items():
    print('')
    r = solve_problem(input)
    print(f'Answer for {name}: {r}')

