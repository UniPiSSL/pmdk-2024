# rout Write-Up



| Δοκιμασία | Ecguct |
| :------- | :----- |
| Δυσκολία | Εύκολη |
| Κατηγορία | Κρυπτογραφία (Cryptography) / Προγραμματισμός (Programming) |
| Λύσεις | 29 |
| Πόντοι | 100 |


## Περιγραφή Δοκιμασίας

``` 
Τα μυστικά μου διέρρεαν συνέχεια μέχρι να βρω έναν τρόπο να τα ασφαλίσω. Εν τέλει βρήκα έναν τρόπο να τα μετατοπίσω...
```

### Source Code

```py
from secret import Secret_Message
from random import randint


def shift(p_char,key):
        c_char = (p_char + key) % 256
        return bytes([c_char])

def Caesar(plaintext):
    ciphertext = b""
    key = randint(2,256)
    for i in plaintext:
        ciphertext +=  shift(i,key)

    return ciphertext

with open("output.txt","wb") as f:
    f.write(Caesar(Secret_Message))

```

### Output Data

 `output.txt` με το κρυπτογραφημένο flag.

## Επίλυση
### Με μια πρώτη ματιά

Από τον κώδικα παρατηρούμε ότι πρόκειται για κρυπτογράφηση byte Caesar.

Κανονικά το key space του Caesar είναι [0,25]. Ωστόσο, στην συγκεκριμένη υλοποίηση παρατηρούμε ότι αρχικοποιείται ένα κλειδί με έναν τυχαίο αριθμό στο εύρος [2,256].

Για τον λόγω αυτό πιθανός να πρέπει να αποκρυπτογραφήσουμε το `Flag` με κώδικα μιας και τα online tools δεν υποστηρίζουν (λογικά) μέχρι 256 key space καθώς και το encoding του ciphertext.


### Ανάλυση - Εύρεση ευπάθειας - Exploitation

Ο Caesar αλγόριθμος είναι αδύναμος και ευπαθής καθώς χρησιμοποιεί κλειδιά μικρού εύρους με αποτέλεσμα το plaintext να μπορεί να ανακτηθεί με ένα μικρό bruteforce attack.

Επομένως, σε μια επανάληψη από το 2 μέχρι το 255 προσπαθούμε να αποκρυπτογραφήσουμε το κρυπτοκείμενο ακολουθώντας την αντίστροφη διαδικασία της κρυπτογράφησης. Ελέγχουμε αν μέσα στα αποκρυπτογραφημένα κείμενα υπάρχει κάποιο printable string της μορφής `FLAG{` το οποίο είναι το flag format.

### Solver


```py
from random import randint
plaintexts = []

with open("output.txt","rb") as f:
    ciphertext = f.read()

def shift(p_char,key):
        c_char = (p_char - key) % 256
        return bytes([c_char])

def Caesar(plaintext,key):
    ciphertext = b""
    for i in plaintext:
        ciphertext +=  shift(i,key)

    return ciphertext

def brute(ciphertext,times):
    for i in range(times):
        plaintexts.append(Caesar(ciphertext,i))

brute(ciphertext,256)

for i in plaintexts:
    if b"FLAG" in i:
         print(i)
```

## Σημαία

```
FLAG{Ca3s4r_1s_vuln3r4bl3_n0_m4tt3r_wh4t!!}
```
