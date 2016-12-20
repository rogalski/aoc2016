def lowest_non_blocked_ip(blocked_ranges):
    blocked_ranges.sort()
    min_allowed = 0
    for start, stop in blocked_ranges:
        assert stop >= start
        if start <= min_allowed < stop:
            min_allowed = stop + 1

    return min_allowed


def num_allowed_ips(blocked_ranges, namespace_size=10):
    blocked_ranges.sort()
    covered_up_to = -1
    num_valid = namespace_size
    for start, stop in blocked_ranges:
        assert stop >= start

        if start <= covered_up_to:
            start = covered_up_to + 1

        if stop < start:
            continue

        num_valid -= (stop-start+1)

        if stop > covered_up_to:
            covered_up_to = stop

    return num_valid


assert lowest_non_blocked_ip([(5, 8), (0, 2), (4, 7)]) == 3
with open('../data/day20.txt') as f:
    blocked_ranges_user_input = [tuple(map(int, l.split('-'))) for l in f]

print("Part1 solution is ", lowest_non_blocked_ip(blocked_ranges_user_input))

assert num_allowed_ips([(5, 8), (0, 2), (4, 7)], 10) == 2
print("Part2 solution is ", num_allowed_ips(blocked_ranges_user_input, 1 << 32))
