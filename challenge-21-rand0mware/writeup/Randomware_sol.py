import itertools
from hashlib import md5
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
import itertools

def bxor(a, b): # byte xor
    return bytes(x ^ y for x, y in zip(a, b))

with open("encrypted_1.pdf","r") as f: # encrypted 1
    PDF_ENC = bytes.fromhex(f.read())

with open("encrypted_2.png","r") as f: # encrypted 3
    PNG_ENC = bytes.fromhex(f.read())

with open("Alfie_Solomons.pdf","rb") as f: # known plaintext
    known = f.read()

a = b"Sup3r_S3cur3_Rand0m_" # static value2
b = b"s33d_f0r_4_R4ns0m" # static value1

answer1 = b"Alfie Solomons" # answer1
answer2 = b"Professional Rum Producer" # answer2
answer3 = b"Shelby Company Limited" # answer3

byte_combinations = list(itertools.product(range(256), repeat=2))
i = 1
for c in byte_combinations:
    print(f"Try {i} remaining {256*256 - i}")
    i += 1
    key2 = md5( a + b + bytes(c) ).digest() # Create possible Key2
    key3 = md5( answer1[:6] + answer2[:13] + answer3[:6] ).digest() # Create Key3
    try:
        ECB_1 = AES.new(key2,AES.MODE_ECB) # Create AES ECB Object with key2
        ECB_2 = AES.new(key3,AES.MODE_ECB) # Create AES ECB Object with key3
        
        CTR_ENCRYPTED_PDF = unpad(ECB_1.decrypt(unpad(ECB_2.decrypt(PDF_ENC),16)),16)
        # Decrypt with ECB key3 -> unpad -> Decrypt with ECB key2
        CTR_ENCRYPTED_PNG = unpad(ECB_1.decrypt(unpad(ECB_2.decrypt(PNG_ENC),16)),16)
        # Decrypt with ECB key3 -> unpad -> Decrypt with ECB key2
        key_stream = bxor(CTR_ENCRYPTED_PDF,CTR_ENCRYPTED_PNG)
        # XOR the CTR outputs
        recovered = bxor(key_stream,known)
        # XOR with known plaintext (pdf)
        # Check if its a PNG via the Header
        if recovered.hex().startswith("89504e470d0a1a0a"): 
            with open("recover.png","wb") as r:
                r.write(recovered) # Re-create the file
                print(f"Random Bytes were {  bytes(c) }")
                break
    except:
        continue


