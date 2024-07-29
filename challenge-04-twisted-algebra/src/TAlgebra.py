#!/usr/bin/env python3
import os
import random
import sympy as sp
from Crypto.Util.number import bytes_to_long # pip install pycryptodome

# I've always been curious since I was young: 
# How do computers create random numbers if they're actually 
# just following a set of predetermined instructions?

# Perhaps Makoto Matsumoto's most famous creation was the answer I sought =)

# Load flag
flag = b'FLAG{this-is-an-example-flag}'
if os.path.exists('flag.txt'):
    flag = open('flag.txt', 'r').read().strip().encode()
else:
    print('WARNING! Using example flag.')


def P(poly, x0):
    poly = sp.sympify(poly)
    return poly.subs(sp.symbols('x'), x0).evalf()

def GenPoly(roots):
    x = sp.symbols('x')
    P = 1
    for xi in roots:
        P *= (x - xi)
    expanded_P = sp.expand(P)
    return str(expanded_P)
    
def GetRandRoots(n):
    result = []
    for i in range(n):
        result.append(random.getrandbits(32*(i+1)))
    return result

output = open("output.txt", "w")

polynomials = []
for i in range(78):
    roots = GetRandRoots(8)
    poly = GenPoly(roots)
    polynomials.append(poly)
    output.write(poly + "\n")

# So many nice polynomials, which one should I choose? 
# I can't make up my mind, so I'll let the computer decide for me, hehehe >:)

poly = polynomials[random.getrandbits(32) % len(polynomials)]

# Hooray! Now, time to encrypt the flag!

x0 = random.getrandbits(32)
x1 = random.getrandbits(32)

# Make sure p and q are both positive for RSA

p = abs(int(P(poly, x0))) 
q = abs(int(P(poly, x1)))

# Create our public key (>= 1024 bits, extra sekurrrr :D)

n = p*q
e = 0x10001

assert n.bit_length() > 1024

# Polynomials here, polynomials there, polynomials everywhere!
ct = pow(bytes_to_long(flag), e, n)
output.write(str(ct))
