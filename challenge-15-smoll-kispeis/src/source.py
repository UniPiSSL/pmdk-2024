import os
from math import prod
from secret import FLAG
from Crypto.Util.number import isPrime, bytes_to_long
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES

class PRNG:
    def __init__(self, seed):
        self.state = seed
        self.A = 2574075728169663774421561315431415276173294095797791071804714248410303618125
        self.B = 87736994699280841534870667657477253616147884454736852116822371260058821182713
        self.M = 2**256
    
    def getPrime(self):
        while True:
            self.state = (self.A * self.state + self.B) % self.M
            if isPrime(self.state):
                return self.state


key = bytes(sorted(os.urandom(16)))
n = prod([PRNG(k).getPrime() for k in key])
cipher = AES.new(key, AES.MODE_ECB)
enc_flag = cipher.encrypt(pad(FLAG, 16))

with open('output.txt', 'w') as f:
    f.write(f'n = 0x{n:x}\n')
    f.write(f'enc_flag = {enc_flag.hex()}\n')