import itertools


def supports_tls(s):
    it = iter(s)

    has_abba_outside_of_brackets = False
    while True:
        string_outside_brackets = ''.join(itertools.takewhile(lambda c: c != '[', it))
        if not string_outside_brackets:
            break
        if has_abba(string_outside_brackets):
            has_abba_outside_of_brackets = True
        string_inside_brackets = ''.join(itertools.takewhile(lambda c: c != ']', it))
        if has_abba(string_inside_brackets):
            return False
    return has_abba_outside_of_brackets


def has_abba(s):
    for idx in range(len(s) - 3):
        c1, c2, c3, c4 = s[idx:idx + 4]
        if c1 == c4 and c2 == c3 and c1 != c2:
            return True
    return False


assert supports_tls("abba[mnop]qrst")
assert not supports_tls("abcd[bddb]xyyx")
assert not supports_tls("aaaa[qwer]tyui")
assert supports_tls("ioxxoj[asdfgh]zxcvbn")

with open('../data/day7.txt') as f:
    print("Number of IPs supporting TLS:", sum(supports_tls(line.strip()) for line in f))
