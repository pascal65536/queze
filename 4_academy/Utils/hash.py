import hashlib

def get_hash(item):
    hash = hashlib.md5(item.encode()).hexdigest()
    print(hash)
    return hash

get_hash("123456789")