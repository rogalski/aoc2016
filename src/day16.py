def run(seq):
    return seq + [0] + [0 if v else 1 for v in reversed(seq)]


def as_list(s):
    return list(map(int, s))


assert run([1]) == [1, 0, 0]
assert run([0]) == [0, 0, 1]
assert run(as_list("11111")) == as_list("11111000000")
assert run(as_list("111100001010")) == as_list("1111000010100101011110000")


def checksum(seq):
    it = iter(seq)
    result = [1 if a == b else 0 for a, b in zip(it, it)]
    while not len(result) % 2:
        result = checksum(result)
    return result


assert checksum(as_list("110010110100")) == as_list("100")


def get_checksum_for_length(input_state, limit_length):
    result = input_state
    while len(result) < limit_length:
        result = run(result)

    del result[limit_length:]
    return ''.join(map(str, checksum(result)))

print("Checksum for test is", get_checksum_for_length(as_list("10000"), 20))
print("Checksum for part 1 is", get_checksum_for_length(as_list("10111011111001111"), 272))
print("Checksum for part 2 is", get_checksum_for_length(as_list("10111011111001111"), 35651584))
