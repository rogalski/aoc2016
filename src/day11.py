"""
Yay, learned something today!

This is a somewhat similar to cannibals and missionaries
problem solved via state-space search by creating tree
of all possible states and filtering out invalid ones

State vector is: (dM1, dG1, dM2, dG2, ...,  dE), where:

dMn = total distance of microchip of type n from 4th floor
dGn = total distance of generator of type n from 4th floor
dE = distance of elevator from 4th floor
"""
import collections
import functools
import itertools
import math
import re


def memorize_generator(f):
    _cache = {}

    @functools.wraps(f)
    def wrapper(*args):
        try:
            return _cache[args]
        except KeyError:
            _cache[args] = list(f(*args))
            return _cache[args]

    return wrapper


def memorize(f):
    _cache = {}

    @functools.wraps(f)
    def wrapper(*args):
        try:
            return _cache[args]
        except KeyError:
            _cache[args] = f(*args)
            return _cache[args]

    return wrapper


@memorize_generator
def yield_valid_states(state):
    for move in yield_valid_moves(state):
        new_state = tuple(old_el + diff_el for old_el, diff_el in zip(state, move))
        if is_valid_state(new_state):
            yield new_state


@memorize_generator
def yield_valid_moves(state):
    objects_count = len(state) - 1
    for single_element_moved_position in range(objects_count):
        if state[single_element_moved_position] == state[-1]:
            move = [0] * objects_count + [1]
            move[single_element_moved_position] = 1
            if state[-1] < 3:
                yield move
            if state[-1] > 0:
                yield [-1 * m for m in move]

    for p0, p1 in itertools.combinations(range(objects_count), 2):
        if state[p0] == state[p1] == state[-1]:
            move = [0] * objects_count + [1]
            move[p0] = 1
            move[p1] = 1
            if state[-1] < 3:
                yield move
            if state[-1] > 0:
                yield [-1 * m for m in move]


@memorize
def is_valid_state(state):
    # is out of bounds?
    if any(s < 0 or s > 3 for s in state):
        return False

    # are microchips fried? check for generator on same floor with unpaired chip
    for base_idx in range(len(state) // 2):
        chip_floor, gen_floor = state[2 * base_idx:2 * base_idx + 2]
        if chip_floor != gen_floor and any(state[p] == chip_floor for p in range(len(state) - 1) if p % 2):
            return False

    return True


def explore_dfs(starting_state):
    # BFS exploration of state space
    # performance is really bad for huge trees
    if not is_valid_state(starting_state):
        raise ValueError(starting_state)

    q = collections.deque()
    q.append([starting_state])
    visited = set()
    old_len_states = 0

    while q:
        states = q.popleft()
        if len(states) != old_len_states:
            old_len_states = len(states)
            print('Start checking depth', old_len_states - 1)
            print('Visited in previous steps:', len(visited), '/', 4 ** len(states[0]))

        state = states[-1]
        visited.add(state)
        if all(s == 0 for s in state):
            print("Final state found", state, "with moves", len(states) - 1)
            print(elements)
            print(states)
            break
        for s in yield_valid_states(state):
            if s not in visited:
                q.append(states + [s])


def explore_astar(starting_state):
    """
    A* search for shortest path
    Based on pseudocode located on Wikipedia:
    https://en.wikipedia.org/wiki/A*_search_algorithm"
    """

    def heuristic_cost_estimate(state_vector):
        """
        Cost is proportional to:
        - distance between corresponding microchip and generator
        - longest distance between one of these two items nad 4th floor
        - 2 factor accounts for having to go forth and back

        Just a rough estimate that happens to work for input 1, but not for input 2.
        """
        it = iter(state_vector)
        return 2 * sum(max(i0, i1) * (abs(i1 - i0) + 1) for i0, i1 in zip(it, it))

    if not is_valid_state(starting_state):
        raise ValueError(starting_state)

    closed_set = set()
    open_set = {starting_state}
    came_from = {}

    g_score = collections.defaultdict(lambda: math.inf)
    g_score[starting_state] = 0

    f_score = collections.defaultdict(lambda: math.inf)
    f_score[starting_state] = heuristic_cost_estimate(starting_state)

    while open_set:
        current = min(open_set, key=lambda k: f_score[k])
        if all(v == 0 for v in current):
            # end state
            return reconstruct_path(came_from, current)

        open_set.remove(current)
        closed_set.add(current)

        for state in yield_valid_states(current):
            if state in closed_set:
                continue
            tentative_g_score = g_score[current] + 1
            if state not in open_set:
                open_set.add(state)
            elif tentative_g_score >= g_score[state]:
                continue  # This is not a better path.

            # This path is the best until now. Record it!
            came_from[state] = current
            g_score[state] = tentative_g_score
            f_score[state] = g_score[state] + heuristic_cost_estimate(state)


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path


# parse input
FLOOR_DISTANCE = {
    'first': 3, 'second': 2, 'third': 1, 'fourth': 0
}

FLOOR_RGX = re.compile('The (\w+) floor contains')
ITEM_RGX = re.compile('(\w+)(?: (generator)|-compatible (microchip))')

elements = set()
item_distances_from_floor = {}  # element: (microchip_distance, generator_distance)

with open('../data/day11.txt') as f:
    for line in f:
        m = FLOOR_RGX.match(line)
        floor_distance = FLOOR_DISTANCE.get(m.group(1))
        for m in ITEM_RGX.finditer(line):
            element, is_generator, is_microchip = m.groups()
            elements.add(element)

            idx = 0 if is_microchip else 1 if is_generator else None
            if element not in item_distances_from_floor:
                item_distances_from_floor[element] = [None, None]
            item_distances_from_floor[element][idx] = floor_distance

elements = sorted(elements)  # convert set to list for deterministic ordering
start_vector = tuple(
    itertools.chain(*[item_distances_from_floor[element] for element in elements], [FLOOR_DISTANCE['first']]))

path = explore_astar(start_vector)
print(*path, sep='\n')
print(len(path) - 1, "steps")
