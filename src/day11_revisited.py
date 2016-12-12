"""
Day 11: part 2

There is a proofed relationship between jealous husbands and
cannibals and missionaries. This fact will be exploited.
I don't know proof, but let's do not care for now.

State vector is: ((M1, G1), (M2, G2), (M3, G3), (M4, G4)  E), where:

Mn - number of microchips on nth floor
Gn - number of generators on nth floor
E  - elevator floor (0 based, 0-3)
end state: ((0, 0), (0, 0), (0, 0), (M4, G4), 3)
"""
import collections
import re


def explore_dfs(starting_state):
    if not is_valid_state(starting_state):
        raise ValueError(starting_state)

    stack = collections.deque()
    stack.append((starting_state, 0))
    visited = {starting_state}

    moves = [(2, 0), (1, 0), (1, 1), (0, 1), (0, 2)]
    directions = [-1, 1]

    while stack:
        state, depth = stack.popleft()
        if is_final_state(state):
            print("Final state found", state, "with", depth, "moves")
            return

        src_floor = state[-1]
        src_m, src_g = state[src_floor]
        for d in directions:
            dst_floor = src_floor + d
            if not 0 <= dst_floor <= 3:
                continue
            dst_m, dst_g = state[dst_floor]

            for delta_m, delta_g in moves:
                if src_m < delta_m or src_g < delta_g:
                    continue
                next_state = list(state)
                next_state[src_floor] = src_m - delta_m, src_g - delta_g
                next_state[dst_floor] = dst_m + delta_m, dst_g + delta_g
                next_state[-1] = dst_floor
                next_state = tuple(next_state)
                if is_valid_state(next_state) and next_state not in visited:
                    stack.append((next_state, depth + 1))
                    visited.add(next_state)  # take only first branch with said state on given depth

    raise RuntimeError("Not found")


def is_valid_state(state):
    return not any(0 < g < m for m, g in state[:-1])


def is_final_state(state):
    return state[:3] == ((0, 0),) * 3


FLOOR_MAP = {
    'first': 0, 'second': 1, 'third': 2, 'fourth': 3
}

FLOOR_RGX = re.compile('The (\w+) floor contains')
ITEM_RGX = re.compile('(\w+)(?: (generator)|-compatible (microchip))')

starting_state = tuple([0, 0] for _ in range(4)) + (0,)
with open('../data/day11_part2.txt') as f:
    for line in f:
        m = FLOOR_RGX.match(line)
        floor_number = FLOOR_MAP.get(m.group(1))
        for m in ITEM_RGX.finditer(line):
            _, is_generator, is_microchip = m.groups()
            if is_microchip:
                starting_state[floor_number][0] += 1
            elif is_generator:
                starting_state[floor_number][1] += 1
            else:
                raise RuntimeError(line)

starting_state = tuple(tuple(o) if type(o) is list else o for o in starting_state)
explore_dfs(starting_state)
exit()
