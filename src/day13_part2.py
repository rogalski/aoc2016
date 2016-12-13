import collections
import functools


@functools.lru_cache(None)
def is_wall(x, y):
    if x < 0 or y < 0:
        return True
    v = x * x + 3 * x + 2 * x * y + y + y * y + 1362
    return sum(int(b) for b in bin(v)[2:]) % 2


def is_destination(x, y):
    return x == 31 and y == 39


def explore_paths(sx, sy):
    start_pos = (sx, sy)
    if is_wall(sx, sy):
        raise ValueError("Starting position is wall")

    stack = collections.deque()
    stack.append([start_pos])
    visited = set()

    while stack:
        path = stack.popleft()
        visited.add(path[-1])
        if len(path) == 51:
            continue
        location = path[-1]
        px, py = location
        new_positions = [(px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)]

        for px, py in new_positions:
            if is_wall(px, py):
                continue
            if (px, py) not in path:
                stack.appendleft(path + [(px, py)])

    print(len(visited))


explore_paths(1, 1)
