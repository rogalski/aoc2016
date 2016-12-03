checked = 0
valid = 0
with open('../data/day3.txt') as f:
    while True:
        try:
            three_lines = next(f), next(f), next(f)
        except StopIteration:
            break

        a_values, b_values, c_values = ([int(s) for s in line.split()] for line in three_lines)

        for a, b, c in zip(a_values, b_values, c_values):
            checked += 1
            if (a + b) > c and (a + c) > b and (b + c) > a:
                valid += 1


print(valid, "valid triangles")
print(checked, "checked triangles")
