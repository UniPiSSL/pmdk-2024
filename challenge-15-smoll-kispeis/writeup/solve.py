from Crypto.Util.number import isPrime
from Crypto.Util.Padding import unpad
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

with open('output.txt') as f:
    n = eval(f.readline().split(' = ')[1])
    enc_flag = bytes.fromhex(f.readline().split(' = ')[1])

key = []
for k in range(256):
    p = PRNG(k).getPrime()
    if n % p == 0:
        key.append(k)


key = bytes(sorted(key))

cipher = AES.new(key, AES.MODE_ECB)

print(unpad(cipher.decrypt(enc_flag), 16))