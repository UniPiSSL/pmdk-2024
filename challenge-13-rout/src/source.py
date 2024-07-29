from secret import p, FLAG
from Crypto.Util.number import bytes_to_long

assert (1344204355 * p ** 2 + 2293708968 * p + 2874229898) % 1094526398891 == 310040297343

n = p**1337
e = 0x10001
m = bytes_to_long(FLAG)
c = pow(m, e, n)

with open('output.txt', 'w') as f:
    f.write(f'e = 0x{e:x}\n')
    f.write(f'c = 0x{c:x}\n')