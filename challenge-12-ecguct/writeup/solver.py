from random import randint

with open("output.txt","rb") as f:
    ciphertext = f.read()

def shift(p_char,key):
        c_char = (p_char - key) % 256
        return bytes([c_char])

def Caesar(plaintext,key):
    ciphertext = b""
    for i in plaintext:
        ciphertext +=  shift(i,key)

    return ciphertext


plaintexts = []

def brute(ciphertext,times):
    for i in range(times):
        plaintexts.append(Caesar(ciphertext,i))

brute(ciphertext,256)

for i in plaintexts:
    if b"FLAG" in i:
         print(i)