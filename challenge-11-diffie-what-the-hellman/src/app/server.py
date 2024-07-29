#!/usr/bin/env python3
from Crypto.Util.number import long_to_bytes
from secret import ALICE_PRIV, BOB_PRIV, SECRET, p, g

def xor(byte_str1, byte_str2):
    if len(byte_str1) != len(byte_str2):
        raise ValueError("Byte strings must have the same length")
    result = bytes([a ^ b for a, b in zip(byte_str1, byte_str2)])
    return result

def Alice_calc():
    A = pow(g, ALICE_PRIV, p) 

    return A

def Bob_calc(A):
    B = pow(g, BOB_PRIV, p) 
    Shared = pow(A, BOB_PRIV, p) 

    return B 

def Flag_Encrypt(B):
    Shared = pow(B, ALICE_PRIV, p)
    ciphertext= xor(SECRET, long_to_bytes(Shared)[:len(SECRET)])

    return ciphertext.hex() 


if __name__ == "__main__":
    A = Alice_calc() 
    print("Hello Bob, Just heard about this crypto system where you can exchange symmetric keys, Wanna try it?")
    print("Oh yea, i've read about it...Let's do it.")
    print("I am sending you my parameters!")
    print(f"Intercepted A : {hex(A)}")
    print(f"Intercepted g : {hex(g)}")
    print(f"Intercepted p : {hex(p)}")
    # Bob receives the parameters and send Alice his PK
    B = Bob_calc(A)
    print(f"Intercepted B : {hex(B)}")
    # Alice use the shared key to encrypt a secret and sends it to Bob
    ciphertext = Flag_Encrypt(B)
    print(f"Intercepted Ciphertext : {ciphertext}")
    try:
        print("Send parameters to Bob")
        p = int(input("p: "))
        g = int(input("g: "))
        if g == 1:
            print("Halt!? What are you doing?")
            exit()
        A = int(input("A: "))
        B = Bob_calc(A)
        print(f"Here is my public key stranger : {hex(B)}")
    except ValueError as e:
        print(e)
