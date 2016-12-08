ON, OFF = '*', ' '
W = 50
H = 6
DISPLAY = [[OFF] * W for _ in range(H)]


def rect(display, w, h):
    for row_num, row in enumerate(display):
        if row_num < h:
            row[:w] = [ON] * w


def rotate_column(display, col_num, shift):
    column = [row[col_num] for row in display]
    shift = len(column) - (shift % len(column))
    shifted = column[shift:] + column[:shift]
    for row, new_column_value in zip(display, shifted):
        row[col_num] = new_column_value


def rotate_row(display, row_num, shift):
    row = display[row_num]
    shift = len(row) - (shift % len(row))
    display[row_num] = row[shift:] + row[:shift]


rotate_map = {'row': rotate_row, 'column': rotate_column}

with open('../data/day8.txt') as f:
    for l in f:
        if l.startswith('rect'):
            cmd, args = l.split()
            w, h = args.split('x')
            rect(DISPLAY, int(w), int(h))
        elif l.startswith('rotate'):
            _, cmd, arg1, _, arg2 = l.split()
            idx = int(arg1.split('=')[1])
            shift = int(arg2)
            rotate_map[cmd](DISPLAY, idx, shift)
        else:
            pass  # skip invalid

print(sum(sum(v == ON for v in row) for row in DISPLAY), 'lights on')


# part 2
def print_display(display, letter_width=5):
    for row in display:
        for col_num, value in enumerate(row):
            if (col_num % letter_width) == 0:
                print("   ", end='')
            print(value, end='')
        print()


print_display(DISPLAY)
