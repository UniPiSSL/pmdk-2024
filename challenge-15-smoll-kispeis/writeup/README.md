# smoll_kispeis Write-Up

| Δοκιμασία | smoll_kispeis |
| :------- | :----- |
| Δυσκολία | Μέτρια |
| Κατηγορία |  Κρυπτογραφία / Προγραμματισμός (Programming) |
| Λύσεις | 13 |
| Πόντοι | 420 |


## Περιγραφή Δοκιμασίας

``` 
Είμαι control freek και θέλω τα πάντα σε τάξη... H κρυπτογραφία δεν αποτελεί εξαίρεση!
```

```py
import os
from math import prod
from secret import FLAG
from Crypto.Util.number import isPrime, bytes_to_long
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES

class PRNG:
    def __init__(self, seed):
        self.state = seed
        self.A = 2574075728169663774421561315431415276173294095797791071804714248410303618125
        self.B = 87736994699280841534870667657477253616147884454736852116822371260058821182713
        self.M = 2**256
    
    def getPrime(self):
        while True:
            self.state = (self.A * self.state + self.B) % self.M
            if isPrime(self.state):
                return self.state


key = bytes(sorted(os.urandom(16)))
n = prod([PRNG(k).getPrime() for k in key])
cipher = AES.new(key, AES.MODE_ECB)
enc_flag = cipher.encrypt(pad(FLAG, 16))

with open('output.txt', 'w') as f:
    f.write(f'n = 0x{n:x}\n')
    f.write(f'enc_flag = {enc_flag.hex()}\n')
```

### Output Data

 `output.txt` με το n και το κρυπτογραφημένο flag.

## Επίλυση
### Με μια πρώτη ματιά

Από τον κώδικα παρατηρούμε ότι πρόκειται για κρυπτογράφηση με `AES ECB` για την κρυπτογράφηση του flag με ένα κλειδί.

Συγκεκριμένα μια μεταβλητή key αρχικοποιείται με `16 τυχαία Bytes` με την χρήση της συνάρτησης `os.urandom`. Αυτά τα bytes ταξινομούνται με αύξουσα σειρά.

Στην συνέχεια δημιουργείται μια μεταβλητή `n`. Αυτή η μεταβλητή είναι το γινόμενο του κάθε αποτελέσματος μιας κλάσης `PRNG`.

Ειδικότερα, κάθε byte της μεταβλητης key περνάει σαν όρισμα στην κλάση `PRNG` όπου στην συνέχεια καλεί την συνάρτηση `getPrime`.

Η κλάση `PRNG` φαίνεται να είναι μια κανονική υλοποίηση μιας `lcg linear congruential generator` της οποίας τις παραμέτρους γνωρίζουμε.

Επομένως, για κάθε Byte του κλειδιού αρχικοποιείται μια lcg με `seed` το εκάστοτε byte του κλειδιού. 

Στην συνέχεια καλείται η `getPrime` όπου χρησιμοποιεί την lcg που μόλις φτιάχτηκε για να παράγει αριθμούς έως ότου βρεί έναν αριθμό που να είναι `πρώτος`. 

Όταν ένα αποτέλεσμα της lcg είναι `πρώτος αριθμός` σταματάει και επιστρέφει τον αριθμό αυτόν.

Η διαδικασία επαναλαμβάνεται για κάθε τιμή του κλειδιού και στο τέλος υπολογίζεται το γινόμενο όλων αυτών των πρώτων αριθμών για να παράγει την μεταβλητή `n`.


### Ανάλυση - Εύρεση ευπάθειας - Exploitation

Έστω ότι το τυχαίο κλειδί είναι το εξής 

`key = [51,85,123,245,2,73,75,115,21,35,73,80,24,69,200,17]`

Μετά την ταξινόμηση το κλειδί θα έχει ως εξής:

`key = [2, 17, 21, 24, 35, 51, 69, 73, 73, 75, 80, 85, 115, 123, 200, 245]`

Στην συνέχεια κάθε τιμή του θα μπει στην κλάση lcg για να παραχθεί ένας `prime`.

Για παράδειγμα το 2 θα μπει και θα υπολογιστεί το εξής:

`(A * 2 + B) % M `

Όπου 
```py
A = 2574075728169663774421561315431415276173294095797791071804714248410303618125
B = 87736994699280841534870667657477253616147884454736852116822371260058821182713
M = 2**256
```

Μέχρις ότου το αποτέλεσμα είναι ένας prime p1

Οπότε το `n = p1 * p2 * p3 * ... * p15 * p16`

Γνωρίζουμε ότι υπάρχουν `256` πιθανά bytes.

Επομένως, μπορούμε σε μια λούπα από το 0 μέχρι το 255 να αρχικοποιούμε την ίδια `lcg` αφού γνωρίζουμε της παραμέτρους της και να ελέγχουμε αν ο `prime` που θα παραχθεί διαιρεί ακριβώς το `n`.

Αν διαιρεί ακριβώς το n τότε σημαίνει ότι η τιμή που χρησιμοποιήθηκε στην lcg είναι τιμή του κλειδιού που χρησιμοποιήθηκε στον AES.

Έχοντας ανακτήσει το κλειδί της κρυπτογράφησης και αφού ο AES είναι `συμμετρική κρυπτογράφηση` 

Που σημαίνει ότι το ίδιο κλειδί χρησιμοποιείται και για την κρυπτογράφηση και για την αποκρυπτογράφηση, μπορούμε να αποκρυπτογραφήσουμε το `flag`.


### Solver


```py
from Crypto.Util.number import isPrime
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES

class PRNG:
    def __init__(self, seed):
        self.state = seed
        self.A = 2574075728169663774421561315431415276173294095797791071804714248410303618125
        self.B = 87736994699280841534870667657477253616147884454736852116822371260058821182713
        self.M = 2**256
    
    def getPrime(self):
        while True:
            self.state = (self.A * self.state + self.B) % self.M
            if isPrime(self.state):
                return self.state

with open('output.txt') as f:
    n = eval(f.readline().split(' = ')[1])
    enc_flag = bytes.fromhex(f.readline().split(' = ')[1])

key = []
for k in range(256):
    p = PRNG(k).getPrime()
    if n % p == 0:
        key.append(k)


key = bytes(sorted(key))

cipher = AES.new(key, AES.MODE_ECB)

print(unpad(cipher.decrypt(enc_flag), 16))
```

## Σημαία

```
FLAG{l4rg3_m0dul0_w1th_sm4ll_k3ysp4c3}
```