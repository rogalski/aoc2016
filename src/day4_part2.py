import string

with open('../data/day4.txt') as f:
    table = str.maketrans(string.ascii_lowercase, string.ascii_lowercase[1:] + 'a')
    for line in f:
        # caaaaa-bbb-z-y-x-123[abxyz]
        encrypted_name, sid_and_checksum = line.rsplit('-', 1)
        sector_id = int(sid_and_checksum[:sid_and_checksum.index('[')])
        to_rotate = sector_id % 26
        table = str.maketrans(string.ascii_lowercase,
                              string.ascii_lowercase[to_rotate:] + string.ascii_lowercase[:to_rotate])

        decrypted_name = encrypted_name.translate(table)
        if 'north' in decrypted_name:
            print(decrypted_name, sector_id)
