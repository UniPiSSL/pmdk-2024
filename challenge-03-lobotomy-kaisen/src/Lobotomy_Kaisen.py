#!/usr/bin/env python3
import os
import hashlib
import sympy as sp
from Crypto.Util.number import getPrime, long_to_bytes, bytes_to_long
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Load flag
AES_KEY = bytes_to_long(b'this-is-an-example-key')

if os.path.exists('key.txt'):
    AES_KEY = bytes_to_long(open('key.txt', 'r').read().strip().encode())

# I sure as hell hope you've watched Jujutsu Kaisen,
# otherwise, you sure as hell will, after this challenge :D

class DomainExpansion:

    # Description:
    # The challenge's domain: Illegible AES.
    # It produces an indecipherable output from the given input to confuse the solver.

    def IllegibleAES(self, plaintext, key):
        md5_hash = hashlib.md5(key).digest() # Hash the key to ensure 16 bytes
        cipher = AES.new(md5_hash, AES.MODE_ECB)
        return cipher.encrypt(pad(plaintext, 16))

class CursedTechnique:

    # Description:
    # The challenge's most powerful cursed technique: Repeated RSA
    # It repeatedly encrypts the plaintext using different RSA parameters to deal damage.

    def RepeatedRSA(self, plaintext, iterations):
        output = []
        
        for i in range(iterations):
            p,q = getPrime(512), getPrime(512)
            n = p*q
            e = 0x7
            ciphertext = pow(plaintext, e, n)
            output.append([ciphertext, n])
        
        return output
        
    # Description:
    # The challenge's less powerful cursed technique: PolynomialFunction
    # Given a number, it passes it through a 4th degree polynomial...

    def F(self, x):
        return int(487287452132*pow(x, 4) - 2476267878632*pow(x,3) + 8028242452324*pow(x, 2) - 56195810567274 * x + 232842749872983)


# Now then, time to get a taste :)

CT = CursedTechnique()

transformed_key = CT.F(AES_KEY)
RSA_Result = CT.RepeatedRSA(transformed_key, 7)

output = open("output.txt", "w")
output.write(str(RSA_Result) + "\n")

# Arm yourself.

Domain = DomainExpansion()

flag = open("flag.pdf", "rb").read()
flag_encrypted = Domain.IllegibleAES(flag, long_to_bytes(AES_KEY))

with open("flag.pdf.enc", "wb") as r:
    r.write(flag_encrypted)
