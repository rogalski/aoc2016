import hashlib
import itertools

door_id = "abbhdwsy"
password = []

for i in itertools.count():
    base = door_id + str(i)
    hashed = hashlib.md5(base.encode('ascii'))
    hashed_hex = hashed.hexdigest()

    if hashed_hex.startswith("0"*5):
        password.append(hashed_hex[5])
        if len(password) == 8:
            break

print("".join(password))
