"""
Solves day15 problem via Chinese Remainder Theorem.
CRT is based on Rosetta code entry.
See: http://rosettacode.org/wiki/Chinese_remainder_theorem
get_earliest_t_via_crt simply creates proper (in terms of crt)
formulation of problem.
"""

import functools
import itertools
import math
import re


def all_are_coprimes(numbers):
    return all(math.gcd(a, b) for a, b in itertools.combinations(numbers, 2))


def chinese_remainder(n, a):
    assert all_are_coprimes(n)
    prod = functools.reduce(lambda x, y: x * y, n, 1)
    result = 0
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        result += a_i * mul_inv(p, n_i) * p
    return result % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def get_earliest_t_via_crt(data_input):
    remainders = [m for m, _ in data_input]
    base_positions = [m - (p + dt) % m for dt, (m, p) in enumerate(data_input, start=1)]
    return chinese_remainder(remainders, base_positions)


def get_input_from_file(file_path):
    rgx = re.compile("Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).")
    with open(file_path) as f:
        return [tuple(map(int, rgx.match(line).groups()[1:3])) for line in f]


test_input = [(5, 4), (2, 1)]
assert 5 == get_earliest_t_via_crt(test_input)
part1_input = get_input_from_file('../data/day15.txt')
print(part1_input)
print("[part1] You need to wait for", get_earliest_t_via_crt(part1_input), "time units")
part2_input = part1_input + [(11, 0)]
print("[part2] You need to wait for", get_earliest_t_via_crt(part2_input), "time units")
