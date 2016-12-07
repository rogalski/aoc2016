import itertools

S, H = 'supernet', 'hypernet'


def supports_ssl(s):
    sequences = list(extract_supernet_and_hypernet_sequences(s))
    supernet_sequences = [seq for seq, mark in sequences if mark == S]
    hypernet_sequences = [seq for seq, mark in sequences if mark == H]

    abas = []
    for s in supernet_sequences:
        abas.extend(find_abas(s))

    return any(aba[1] + aba[0] + aba[1] in s for aba in abas for s in hypernet_sequences)


def extract_supernet_and_hypernet_sequences(s):
    it = iter(s)
    while True:
        string_outside_brackets = ''.join(itertools.takewhile(lambda c: c != '[', it))
        if string_outside_brackets:
            yield string_outside_brackets, S
        else:
            break
        string_inside_brackets = ''.join(itertools.takewhile(lambda c: c != ']', it))
        if string_inside_brackets:
            yield string_inside_brackets, H
        else:
            break


def find_abas(s):
    for idx in range(len(s) - 2):
        c1, c2, c3 = s[idx:idx + 3]
        if c1 == c3 and c2 != c3:
            yield s[idx:idx + 3]


assert supports_ssl("aba[bab]xyz")
assert not supports_ssl("xyx[xyx]xyx")
assert supports_ssl("aaa[kek]eke")
assert supports_ssl("zazbz[bzb]cdb")

with open('../data/day7.txt') as f:
    print("Number of IPs supporting SSL:", sum(supports_ssl(line.strip()) for line in f))
