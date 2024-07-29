#!/usr/bin/env python3
import hashlib
import sympy as sp
from sympy.ntheory.modular import crt
from gmpy2 import iroot
from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
    
def DecryptAES(ct, key): # Undoes the flag encryption given the key
    md5_hash = hashlib.md5(key).digest()
    cipher = AES.new(md5_hash, AES.MODE_ECB)
    return unpad(cipher.decrypt(ct), 16)

# Open the output file
parser = open("output.txt", "r").readlines()

# Parse the congruences (tuples of [ciphertexts, moduli])
congruences = eval(parser[0])

# Define x as a symbol and parse f(x) in sympy
x = sp.symbols('x')
f = 487287452132*x**4 - 2476267878632*x**3 + 8028242452324*x**2 - 56195810567274 * x + 232842749872983

# Parse remainders and moduli into 2 lists to prepare for CRT
mods = [] # τα διάφορα n
rems = [] # τα διάφορα ciphertexts
for congruence in congruences:
    rems.append(congruence[0])
    mods.append(congruence[1])
 
# Solve for (f(AES_KEY))^7 using CRT 
solution = crt(mods, rems)[0]
print(f"[+] Recovered (f(AES_KEY))^7 = {solution}\n")

# Take the 7th root of the solution to get f(AES_KEY)
obfuscated_key = int(iroot(solution, 7)[0]) #iroot -> integer root
print(f"[+] Recovered f(AES_KEY) = {obfuscated_key}\n")

# Solve the equation f(x) = f(AES_KEY) <=> f(x) - f(AES_KEY) = 0
# for x in order to recover AES_KEY
AES_KEY = sp.solve(f - obfuscated_key, x)[0] # Παίρνουμε το 1ο root
print(f"[+] Recovered AES_KEY = {AES_KEY}\n")

# Read the ciphertext (the encrypted flag file)
encrypted_flag = open("flag.pdf.enc", "rb").read()

# Get its decrypted bytes
decrypted_flag = DecryptAES(encrypted_flag, long_to_bytes(AES_KEY))

# Write the decrypted bytes to a file and we are done
with open("solved.pdf", "wb") as s:
    s.write(decrypted_flag)
    
print(f"[+] Wrote flag to 'solved.pdf'")
