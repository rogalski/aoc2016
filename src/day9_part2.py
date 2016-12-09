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

                    # prepare repeated part, this also consumes iterator
                    repeated_part = ''.join([next(it) for _ in range(to_repeat_len)])

                    # decompress recursively
                    length += how_many_times * decompressed_length(repeated_part)

                    break  # go back to consuming standard data all up to compression marker
    return length


assert decompressed_length('(3x3)XYZ') == 9
assert decompressed_length('X(8x2)(3x3)ABCY') == len("XABCABCABCABCABCABCY")
assert decompressed_length('(27x12)(20x12)(13x14)(7x10)(1x12)A') == 241920
assert decompressed_length('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN') == 445

with open('../data/day9.txt') as f:
    data = f.read()

print("Decompressed length is: ", decompressed_length(data))
