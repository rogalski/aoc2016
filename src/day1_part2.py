#!/usr/bin/env python3
with open('../data/day1.txt') as f:
    steps = f.read().split(", ")

N, E, S, W = 'N', 'E', 'S', 'W'
L, R = 'L', 'R'

new_direction_left = {N: W, W: S, S: E, E: N}
new_direction_right = {N: E, E: S, S: W, W: N}
new_direction = {L: new_direction_left, R: new_direction_right}

direction = N
position = (0, 0)
seen = {position}
seen_twice = False

for step in steps:
    turn, distance = step[0], int(step[1:])
    direction = new_direction[turn][direction]

    if direction == N:
        dx = 1
    elif direction == S:
        dx = -1
    else:
        dx = 0

    if direction == E:
        dy = 1
    elif direction == W:
        dy = -1
    else:
        dy = 0

    for d in range(distance):
        position = (position[0] + dx, position[1] + dy)
        if position in seen:
            seen_twice = True
            break
        seen.add(position)

    if seen_twice:
        break

total_distance = abs(position[0]) + abs(position[1])
print("Position:", position, "Total distance", total_distance)
