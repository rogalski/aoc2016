import collections
import hashlib

W = H = 4
UP, DOWN, LEFT, RIGHT = 'U', 'D', 'L', 'R'


def are_doors_open(passcode):
    h = hashlib.md5(passcode.encode()).hexdigest()
    return tuple(1 if v in "bcdef" else 0 for v in h[:4])


def yield_valid_positions(pos, passcode):
    up_is_open, down_is_open, left_is_open, right_is_open = are_doors_open(passcode)
    x, y = pos
    if y > 0 and up_is_open:
        yield (x, y - 1), UP
    if y < (H - 1) and down_is_open:
        yield (x, y + 1), DOWN
    if x > 0 and left_is_open:
        yield (x - 1, y), LEFT
    if x < (W - 1) and right_is_open:
        yield (x + 1, y), RIGHT


# exploration is quasi-bfs, since effectively graph changes in each step
def get_shortest_path(passcode, starting_pos=(0, 0), target=(W - 1, H - 1)):
    base_passcode_length = len(passcode)
    q = collections.deque()
    q.append((starting_pos, passcode))
    while q:
        pos, passcode = q.popleft()
        if pos == target:
            return passcode[base_passcode_length:]

        for new_pos, path_step in yield_valid_positions(pos, passcode):
            q.append((new_pos, passcode + path_step))


def get_longest_path(passcode, starting_pos=(0, 0), target=(W - 1, H - 1)):
    base_passcode_length = len(passcode)
    q = collections.deque()
    q.append((starting_pos, passcode))
    longest_path = ""
    while q:
        pos, passcode = q.popleft()
        if pos == target:
            longest_path = passcode[base_passcode_length:]
            continue

        for new_pos, path_step in yield_valid_positions(pos, passcode):
            q.append((new_pos, passcode + path_step))
    return longest_path


print("Shortest path is", get_shortest_path("pslxynzg"))
print("Shortest path is", len(get_longest_path("pslxynzg")), "steps long")
exit(1)
