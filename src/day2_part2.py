keypad = [
    [None, None, 1, None, None],
    [None, 2, 3, 4, None],
    [5, 6, 7, 8, 9],
    [None, 'A', 'B', 'C', None],
    [None, None, 'D', None, None],
]

indices_to_key = {
    (row_idx, col_idx): value
    for row_idx, row in enumerate(keypad)
    for col_idx, value in enumerate(row)
    if value is not None
    }

moves = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

last_key_idx = (2, 0)
assert indices_to_key[last_key_idx] == 5

with open('../data/day2.txt') as f:
    for line in f:
        for char in line:
            if char not in moves:
                continue
            move = moves[char]
            new_key = (last_key_idx[0] + move[0], last_key_idx[1] + move[1])
            if new_key in indices_to_key:
                last_key_idx = new_key
        print(indices_to_key[last_key_idx], end='')
