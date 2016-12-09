def decompressed_length(s):
    length = 0
    it = iter(s)
    for c in it:
        # consume iterator all up to compression marker
        if c != '(':
            length += 1
        else:
            # consume repeat clause
            repeat_clause = ''
            for c2 in it:
                if c2 != ')':
                    repeat_clause += c2
                else:
                    # end of repeat clause detected, parse compression params
                    to_repeat_len, how_many_times = repeat_clause.split('x')
                    to_repeat_len = int(to_repeat_len)
                    how_many_times = int(how_many_times)

                    # update total length
                    length += to_repeat_len * how_many_times

                    # consume repeated part to advance iterator
                    for _ in range(to_repeat_len):
                        next(it)

                    break  # go back to consuming standard data all up to compression marker
    return length


assert decompressed_length('ADVENT') == 6
assert decompressed_length('A(1x5)BC') == 7
assert decompressed_length('(3x3)XYZ') == 9
assert decompressed_length('A(2x2)BCD(2x2)EFG') == 11
assert decompressed_length('A(2x2)BCD(2x2)EFG') == 11
assert decompressed_length('(6x1)(1x3)A') == 6
assert decompressed_length('X(8x2)(3x3)ABCY') == 18

with open('../data/day9.txt') as f:
    data = f.read()

print("Decompressed length is: ", decompressed_length(data))
