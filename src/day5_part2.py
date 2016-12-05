import hashlib
import itertools

door_id = "abbhdwsy"
password = [''] * 8

for i in itertools.count():
    base = door_id + str(i)
    hashed = hashlib.md5(base.encode('ascii'))
    hashed_hex = hashed.hexdigest()

    if hashed_hex.startswith("0"*5):
        position = int(hashed_hex[5], 16)
        if position < len(password) and not password[position]:
            password[position] = hashed_hex[6]
            print("\r", "".join(c or '_' for c in password), end='', flush=True)
            if all(password):
                break
