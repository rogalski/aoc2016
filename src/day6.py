from collections import Counter

with open('../data/day6.txt') as f:
    N = len(next(f).strip())
    f.seek(0)
    counters = [Counter() for _ in range(N)]
    for line in f:
        for counter, char in zip(counters, line):
            counter[char] += 1

message = "".join(counter.most_common(1)[0][0] for counter in counters)
print("Message:", message)
