from mt19937predictor import MT19937Predictor
from Crypto.Util.number import long_to_bytes
import sympy as sp

def P(poly, x0):
    poly = sp.sympify(poly)
    return poly.subs(sp.symbols('x'), x0).evalf()

file = open("output.txt", "r").readlines()

polynomials = file[:-1] # parse polynomials
ct = int(file[-1:][0]) # parse RSA ciphertext

# Predictor training: 78 Polynomials * 8 random roots = 624, just what we need :)
predictor = MT19937Predictor()
for i in range(len(polynomials)):
    poly = polynomials[i]
    # Find the roots using sympy.solve
    roots = sp.solve(poly)
    
    # The roots are already sorted from smallest to greatest, so we proceed
    for i in range(len(roots)):
        predictor.setrandbits(roots[i], 32*(i+1))

# Predictor has been trained, simply calculate the rest as the original script
poly = polynomials[predictor.getrandbits(32) % len(polynomials)]
x0 = predictor.getrandbits(32)
x1 = predictor.getrandbits(32)
p = abs(int(P(poly, x0))) 
q = abs(int(P(poly, x1)))
n = p*q
e = 0x10001

# Calculate d
d = pow(e, -1, int(sp.totient(n)))

# Decrypt
pt = pow(ct,d,n)
print(long_to_bytes(pt).decode())