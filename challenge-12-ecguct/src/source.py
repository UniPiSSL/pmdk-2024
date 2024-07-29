from secret import Secret_Message
from random import randint


def shift(p_char,key):
        c_char = (p_char + key) % 256
        return bytes([c_char])

def Caesar(plaintext):
    ciphertext = b""
    key = randint(2,256)
    for i in plaintext:
        ciphertext +=  shift(i,key)

    return ciphertext

with open("output.txt","wb") as f:
    f.write(Caesar(Secret_Message))






