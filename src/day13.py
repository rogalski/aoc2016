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


def explore_bfs(starting_pos):
    sx, sy = starting_pos
    if is_wall(sx, sy):
        raise ValueError("Starting position is wall")

    stack = collections.deque()
    stack.append((starting_pos, 0))
    visited = {starting_pos}

    while stack:
        position, depth = stack.popleft()
        px, py = position
        if is_destination(px, py):
            print("Final location found", position, "with", depth, "moves")
            return

        new_positions = [(px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)]

        for px, py in new_positions:
            if is_wall(px, py):
                continue
            if (px, py) not in visited:
                stack.append(((px, py), depth + 1))
                visited.add((px, py))  # take only first branch with said state on given depth

    raise RuntimeError("Not found")


explore_bfs((1, 1))
