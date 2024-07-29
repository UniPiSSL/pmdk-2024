# Diffie What the Hellmand Write-Up



| Δοκιμασία | Diffie What the Hellmand |
| :------- | :----- |
| Δυσκολία | Μέτρια |
| Κατηγορία | Κρυπτογραφία (Cryptography) / Προγραμματισμός (Programming) |
| Λύσεις | 6 |
| Πόντοι | 569 |

## Περιγραφή Δοκιμασίας

``` 
Ο Bob και η Alice επιμένουν ότι το κρυπτοσύστημα ανταλλαγής κλειδιών που έχουν υλοποιήσει δεν έχει κενά ασφαλείας. Μπορείς να τους αποδείξεις λάθος;
```

```py
from Crypto.Util.number import long_to_bytes
from pwn import xor
from secret import ALICE_PRIV,BOB_PRIV,SECRET

p = 117477667918738952579183719876352811442282667176975299658506388983916794266542270944999203435163206062215810775822922421123910464455461286519153688505926472313006014806485076205663018026742480181999336912300022514436004673587192018846621666145334296696433207116469994110066128730623149834083870252895489152123
g = 104831378861792918406603185872102963672377675787070244288476520132867186367073243128721932355048896327567834691503031058630891431160772435946803430038048387919820523845278192892527138537973452950296897433212693740878617106403233353998322359462259883977147097970627584785653515124418036488904398507208057206926 

def Alice_calc():
    A = pow(g,ALICE_PRIV,p) 

    return A

def Bob_calc(A):
    B = pow(g,BOB_PRIV,p) 
    Shared = pow(A,BOB_PRIV,p) 

    return B 

def Flag_Encrypt(B):
    Shared = pow(B,ALICE_PRIV,p)
    ciphertext= xor(SECRET,long_to_bytes(Shared)[:len(SECRET)])

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
```

## Επίλυση
### Με μια πρώτη ματιά

Με μια πρώτη ματιά μπορούμε να καταλάβουμε ότι πρόκειται για το κρυπτοσύστημα ανταλλαγής κλειδιών Diffie Hellman.

Στην δοκιμασία αυτή παρακολουθούμε την διαδικασία ανταλλαγής κοινού κλειδιού μεταξύ του Bob και της Alice.

Επομένως, έχουμε πρόσβαση στις δημόσιες παραμέτρους 

1. Prime
2. Γεννήτορα της Ομάδας της κυκλικής ομάδας του prime αυτού (https://en.wikipedia.org/wiki/Cyclic_group)
3. Το δημόσιο κλειδί της Alice
4. Το δημόσιο κλειδί του Bob
5. Το κρυπτογραφημένο μυστικό τους το οποίο κρυπτογραφήθηκε με το shared key της Alice και του Bob

Στην συνέχεια μας δίνεται η ευκαιρία να επικοινωνήσουμε εμείς με τον Bob.

Μπορούμε να του στείλουμε:

1. Έναν prime
2. Έναν γεννήτορα
3. Το δημόσιο κλειδί μας

### Ανάλυση - Εύρεση ευπάθειας - Exploitation

Στον Diffie Hellman τα βήματα είναι τα εξής:

### H Alice στέλνει το public key στον bob όπου δημιουργείται ως εξής

- x = Ιδιωτικό Κλειδί της Alice 
- Α = Δημόσιο Κλειδί της Alice
- g = Γεννήτορας Ομάδας
- p,g = prime και γεννήτορας

- Α = g <sup>x</sup> % p

### Ο bob παράγει με τον ακριβώς ίδιος τρόπο το δημόσιο κλειδί του.

- y = Ιδιωτικό Κλειδί τού Bob
- B = Δημόσιο Κλειδί του Bob
- Ο ίδιος γεννήτορας που χρησιμοποίησε η Alice
- p,g = prime και γεννήτορας

- B = g<sup>y</sup> % p

### O Bob στέλνει το δημόσιο κλειδί του στην Alice και παράλληλα υπλογίζει το shared key ως εξής:

shared_key = A<sup>y</sup> % p === (g<sup>x</sup>)<sup>y</sup> % p === g<sup>(x*y)</sup> % p

4. Η Alice ακολουθεί την ίδια διαδικασία αφού λάβει το δημόσιο κλειδί του bob:

shared_key = B<sup>x</sup> % p === (g<sup>y</sup>)<sup>x</sup> % p === g<sup>(x*y)</sup> % p

Ένα πολύ βασικό στοιχείο είναι ότι τα private key της Alice και του Bob είναι πάντα ίδια και οι παράμετροι δεν ελέγχονται κατά την δημιουργία του shared key.

Επομένως, έχοντας την ευκαιρία να επικοινωνήσουμε με τον Bob μπορούμε:

1. Να του στείλουμε τον ίδιο prime που χρησιμοποιήθηκε με την Alice.
2. Δεδομένου ότι δεν ελέγχονται οι παράμετροι μπορούμε να στείλουμε για γεννήτορα το δημόσιο κλειδί της Alice

3. Ο Bob όταν λάβει το δημόσιο κλειδί της Alice και θα υπολογίσει ως δικό του δημόσιο κλειδί το εξής:

B = (A<sup>y</sup>) % p === (g<sup>x</sup>)<sup>y</sup>  % p === g<sup>(x*y)</sup> % p === Shared_key

και θα μας το επιστρέψει.

Επομένως, χωρίς να ξέρουμε τα ιδιωτικά κλειδιά του Bob και της Alice θα έχουμε στην κατοχή μας το shared key της Alice και του Bob και θα μπορούμε να κάνουμε decrypt το κρυπτογραφημένο μυστικό.



### Solver


```py
from pwn import *
import json
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes

HOST = '127.0.0.1'
PORT = 4244


r = remote(HOST,PORT)


print(r.recvuntil(b"parameters!\n"))

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
```

## Σημαία


```
FLAG{n0_p4ram_f1lt3r_==_n0_s3cure_s3cr3t}
```
