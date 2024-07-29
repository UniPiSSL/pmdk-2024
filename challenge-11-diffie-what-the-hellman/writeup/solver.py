from pwn import *
import json
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad 
from Crypto.Util.number import long_to_bytes


HOST = 'challenges.pmdk.gr'
PORT = 57685


r = remote(HOST,PORT)


print(r.recvuntil(b"parameters!\r\n"))

Alice_public_key = int(r.recvline().split(b": ")[1].strip().decode(),16)
generator =  int(r.recvline().split(b": ")[1].strip().decode(),16)
prime = int(r.recvline().split(b": ")[1].strip().decode(),16)

Bob_public_key = int(r.recvline().split(b": ")[1].strip().decode(),16)
Encrypted = bytes.fromhex(r.recvline().split(b": ")[1].strip().decode())
 
r.sendlineafter(b"p: ",str(prime).encode())
r.sendlineafter(b"g: ",str(Alice_public_key).encode())
r.sendlineafter(b"A: ",str(1).encode()) # doesn't matter

shared_key_of_Alice_and_Bob = int(r.recvline().split(b": ")[1].strip().decode(),16)



print(f"Decrypted secret is  {xor(Encrypted,long_to_bytes(shared_key_of_Alice_and_Bob)[:len(Encrypted)]).decode()}")
r.close()