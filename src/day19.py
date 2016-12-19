import itertools


def white_elephant_game_part1(n):
    indices = list(range(n))
    has_presents = [True] * n
    count_presents = n

    steal_from_next = False
    for idx in itertools.cycle(indices):
        if not has_presents[idx]:
            continue

        if steal_from_next:
            has_presents[idx] = False
            steal_from_next = False
            count_presents -= 1
            if count_presents <= 1:
                break

        elif has_presents[idx]:
            steal_from_next = True

    return next(idx + 1 for idx, v in enumerate(has_presents) if v)


assert white_elephant_game_part1(5) == 3
print("Part1 solution is", white_elephant_game_part1(3004953))
