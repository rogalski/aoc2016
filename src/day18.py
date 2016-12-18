SAFE, TRAP = '.', '^'


def is_trap(column_number, previous_row):
    left = previous_row[column_number - 1] if column_number > 0 else SAFE
    center = previous_row[column_number]
    try:
        right = previous_row[column_number + 1]
    except IndexError:
        right = SAFE
    return ((left == TRAP and center == right == SAFE)
            or (left == center == SAFE and right == TRAP)
            or (left == center == TRAP and right == SAFE)
            or (center == right == TRAP and left == SAFE))


def generate_map(first_row, total_rows):
    col_count = len(first_row)
    trap_map = [first_row]
    while len(trap_map) < total_rows:
        new_row = ''.join(TRAP if is_trap(c, trap_map[-1]) else SAFE for c in range(col_count))
        trap_map.append(new_row)
    return trap_map


def get_count(trap_map, item_type):
    return sum(tile == item_type for row in trap_map for tile in row)


print(*generate_map("..^^.", 3), sep='\n')
print("test1 has", get_count(generate_map("..^^.", 3), SAFE), "safe tiles")
print("test2 has", get_count(generate_map(".^^.^.^^^^", 10), SAFE), "safe tiles")
print("part1 has", get_count(generate_map("^.^^^.^..^....^^....^^^^.^^.^...^^.^.^^.^^.^^..^.^...^.^..^.^^.^..^.....^^^.^.^^^..^^...^^^...^...^.", 40), SAFE), "safe tiles")
print("part2 has", get_count(generate_map("^.^^^.^..^....^^....^^^^.^^.^...^^.^.^^.^^.^^..^.^...^.^..^.^^.^..^.....^^^.^.^^^..^^...^^^...^...^.", 400000), SAFE), "safe tiles")
