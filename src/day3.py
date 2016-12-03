checked = 0
valid = 0
with open('../data/day3.txt') as f:
    for line in f:
        checked += 1
        a, b, c = (int(s) for s in line.split())
        if (a + b) > c and (a + c) > b and (b + c) > a:
            valid += 1

print(valid, "valid triangles")
print(checked, "checked triangles")
