import functools
import hashlib

import itertools

SALT = b"ahsbgdzn"


@functools.lru_cache(None)
def get_hash_string(int_value):
    return hashlib.md5(SALT + str(int_value).encode()).hexdigest()


@functools.lru_cache(None)
def get_hash_string2(int_value):
    h = SALT.decode() + str(int_value)
    for _ in range(2017):
        h = hashlib.md5(h.encode()).hexdigest()
    return h


@functools.lru_cache(None)
def get_first_triplet(hash_string):
    for index, character in enumerate(hash_string):
        if index > len(hash_string) - 3:
            break
        if hash_string[index] == hash_string[index + 1] == hash_string[index + 2]:
            return hash_string[index]
    return None


to_check = set()  # (hash, letter_in_quintuple, last_valid_step)
found_keys = {}

for i in itertools.count():
    h = get_hash_string2(i)
    t = get_first_triplet(h)
    if t:
        to_check.add((h, t, i))

    outdated = set()
    for check_entry in to_check:
        hash_to_check, letter, from_step = check_entry
        if i > (from_step + 1000):
            outdated.add(check_entry)
        elif from_step != i and 5 * letter in h:
            print(hash_to_check, "from step", from_step, "confirmed with", h, "from step", i)
            found_keys[from_step] = hash_to_check
            outdated.add(check_entry)

    to_check -= outdated
    if len(found_keys) >= 64:
        break

print(sorted(found_keys)[63], " is an index for 64th hash")
