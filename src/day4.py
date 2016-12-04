from collections import Counter

sector_id_sum = 0
with open('../data/day4.txt') as f:
    for line in f:
        # caaaaa-bbb-z-y-x-123[abxyz]
        encrypted_name, sid_and_checksum = line.rsplit('-', 1)
        counts = Counter(encrypted_name)
        del counts['-']

        checksum = sid_and_checksum[sid_and_checksum.index('[') + 1:sid_and_checksum.index(']')]
        sector_id = int(sid_and_checksum[:sid_and_checksum.index('[')])

        computed_checksum = ''.join(sorted(counts.keys(), key=lambda letter: (-counts[letter], letter))[:len(checksum)])

        if checksum == computed_checksum:
            sector_id_sum += sector_id

print("Sum of sector ids = ", sector_id_sum)
