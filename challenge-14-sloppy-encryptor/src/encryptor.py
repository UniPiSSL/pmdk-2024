from random import randint as rint
from secret_stuff import FLAG

def encrypt(FLAG):
    return "".join([str(ord(c))+str(rint(126, 254)) for c in FLAG])

def toBytes(enc):
    return b"".join([chr(int(enc[i]) + 100).encode() for i in range(len(enc))])

with open("./flag.enc","wb") as f:
    enc = encrypt(FLAG)
    enc_ = toBytes(enc)
    f.write(enc_)
