from Crypto.Util.number import long_to_bytes

with open('output.txt') as f:
    e = eval(f.readline().split(' = ')[1])
    c = eval(f.readline().split(' = ')[1])

R.<x> = PolynomialRing(GF(1094526398891))

F = 1344204355*x**2 + 2293708968*x + 2874229898 - 310040297343

p = int(F.roots()[0][0])

n = p^1337
phi = euler_phi(n)
d = power_mod(e, -1, phi)
m = power_mod(c, d, n)
print(long_to_bytes(m))