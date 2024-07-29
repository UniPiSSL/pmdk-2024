# Twisted Algebra

| Δοκιμασία | Twisted Algebra |
| :------- | :----- |
| Δυσκολία | Υπερβολικά Δύσκολη |
| Κατηγορία | Κρυπτογραφία (Cryptography) |
| Λύσεις | 8 |
| Πόντοι | 539 |

## Επισκόπηση Δοκιμασίας

Η περιγραφή της δοκιμασίας αναφέρει:
```
Ένας πελάτης της τράπεζας στην οποία δουλεύω έχασε τον κωδικό πρόσβασής του. Σου επισυνάπτω τον κώδικα που χρησιμοποιήσαμε για να τον κρυπτογραφήσουμε. Η δουλειά σου ως εκπρόσωπος του IT είναι να τον ανακτήσεις.
```
Επιπλέον μας δίνετε ένα zip αρχείο με 3 αρχεία.

### Ο κώδικας κρυπτογράφησης (Python3)

```py
#!/usr/bin/env python3
import os
import random
import sympy as sp
from Crypto.Util.number import bytes_to_long

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
```

## Επίλυση

Αρχικά, βλέπουμε πως στο zip του challenge περιλαμβάνονται 3 αρχεία.

1. `TAlgebra.py` : Είναι το κύριο script του challenge που περιλαμβάνει τον κώδικα.
2. `requirements.txt` : Περιέχει της απαραίτητες βιβλιοθήκες (libraries) που χρειάζεται το κύριο script για να τρέξει.
3. `output.txt` : Περιέχει το κρυπτογραφημένο output το οποίο κρυπτογραφήθηκε με το κύριο script.

### Με μια πρώτη ματιά

Ας αναλύσουμε πρώτα το κύριο αρχείο `TAlgebra.py`. Με μια πρώτη ματιά βλέπουμε ότι περιέχει 3 συναρτήσεις:

1. `P(poly, x0)` : Παίρνει 2 παραμέτρους, εκ των οποίων η μία είναι ένα πολυώνυμο (poly) και η άλλη είναι ένα x0 (int). Στη συνέχεια αντικαθιστά όπου x το x0 και υπολογίζει το F(x0).
2. `GenPoly(roots)` : Παίρνει ως παράμετρο μία λίστα ακεραίων (roots) και δημιουργεί ένα πολυώνυμο με ρίζες αυτούς τους ακεραίους - `P(x) = (x-x0)*(x-x1)*(x-x2)*...*(x-xν), με x1,x2,...,xν ∈ roots`. Στη συνέχεια κάνει τις επιμεριστικές και επιστρέφει την "ανοιχτή" μορφή του πολυωνύμου.
3. `GetRandRoots(n)` : Δημιουργεί μια λίστα n τυχαίων ακεραίων (που θα χρησιμοποιηθούν στην GenPoly ως ρίζες - δηλαδή δημιουργεί τη λίστα roots). Ο κάθε τυχαίος ακέραιος έχει bitsize 32x, δηλαδή ο πρώτος είναι `32*1 = 32bit` ακέραιος, ο 2ος `32*2 = 64bit`, ο 3ος `32*3 = 96bit` κτλ.

### Αναλύοντας το κύριο πρόγραμμα

Το κύριο πρόγραμμα ξεκινάει ανοίγοντας το αρχείο output.txt (`output = open("output.txt", "w")`) και δημιουργώντας μια λίστα για τα πολυώνυμα (`polynomials = []`).

Στη συνέχεια, επαναλαμβάνουμε τα εξής βήματα για `78 φορές`:

1. Καλούμε τη `GetRandRoots` με `n = 8` και δημιουργούμε μια λίστα 8 τυχαίων ακεραίων (`roots = GetRandRoots(8)`)
2. Δημιουργούμε ένα πολυώνυμο με ρίζες τους προαναφερόμενους ακεραίους μέσω της `GenPoly` (`poly = GenPoly(roots)`)
3. Προσαρτούμε στη λίστα των πολυωνύμων που φτιάξαμε προηγουμένως το `poly` (`polynomials.append(poly)`)
4. Γράφουμε στο `output.txt` το `poly` μαζί με ένα line break (`output.write(poly + "\n")`)

Με απλά λόγια, δημιουργούμε 78 πολυώνυμα με 8 τυχαίες ρίζες το καθένα, τα γράφουμε όλα στο `output.txt` και ταυτόχρονα τα αποθηκεύουμε σε μια λίστα `polynomials`.

Στη συνέχεια, διαλέγουμε ένα τυχαίο πολυώνυμο από αυτά τα 78 (`poly = polynomials[random.getrandbits(32) % len(polynomials)]`). Αυτό το κάνουμε παίρνοντας έναν τυχαίο 32bit ακέραιο και κάνοντας τον mod το length της λίστας μας, ώστε να βρίσκεται μέσα στα όριά της.

Έχοντας αυτό το πολυώνυμο, διαλέγουμε 2 τυχαία σημεία x0 και x1 ως εξής:
```py
x0 = random.getrandbits(32)
x1 = random.getrandbits(32)
```

### To RSA κομμάτι του προγράμματος

Αφού έχουμε διαλέξει ένα τυχαίο πολυώνυμο (`poly`) και 2 τυχαία σημεία x0, x1, υπολογίζουμε τα `P(x0)` και `P(x1)` μέσω της συνάρτησης `P`. Τα αποτελέσματα θα τα χρησιμοποιήσουμε ως ιδιωτικές παραμέτρους για [RSA Encryption](https://el.wikipedia.org/wiki/RSA), επομένως θέλουμε να είναι θετικά:
```py
# Make sure p and q are both positive for RSA
p = abs(int(P(poly, x0))) 
q = abs(int(P(poly, x1)))
```
Σημείωση: Κανονικά, οι p και q πρέπει να είναι πρώτοι αριθμοί για σωστό RSA implementation, όμως δεν είναι απαραίτητο. Στη προκειμένη περίπτωση, έχουμε composite p και q, το οποίο είναι insecure επειδή μπορεί κανείς να κάνει πιο εύκολα factor το public key (n) και να υπολογίσει το Φ(n) και στη συνέχεια να ανακτήσει το private exponent. 

Τέλος, υπολογίζουμε `n=p*q` και θέτουμε το Public Exponent μας (e) να είναι `0x10001`. Στη συνέχεια κρυπτογραφούμε το flag με standard RSA:
```py
# Create our public key (>= 1024 bits, extra sekurrrr :D)

n = p*q
e = 0x10001

assert n.bit_length() > 1024

# Polynomials here, polynomials there, polynomials everywhere!
ct = pow(bytes_to_long(flag), e, n)
output.write(str(ct))
```

### Η κύρια ευπάθεια (vulnerability)

Έχοντας αναλύσει εκτενώς το κύριο πρόγραμμα, βλέπουμε πως τα μόνα μας δεδομένα είναι τα `78 polynomials` με 8 τυχαίες ρίζες το καθένα και το RSA encrypted flag. Δεν ξέρουμε ούτε πια 2 σημεία x0 και x1 επιλέχθηκαν, ούτε πιο πολυώνυμο χρησιμοποιήθηκε για να υπολογιστούν τα `p = |P(x0)|, q = |P(x1)|`, ούτε το public modulus (n) που χρησιμοποιήθηκε για RSA. Το main theme στη δοκιμασία είναι το ότι όλα υπολογίστηκαν "τυχαία", ξεκινώντας από τις ρίζες του κάθε πολυωνύμου, μέχρι και το πολυώνυμο P που χρησιμοποιήθηκε για τον υπολογισμό των p και q. 

Αν διαβάσουμε το hint που μας δίνεται, μπορούμε να καταλάβουμε πως το "random" module της Python δεν είναι και τόσο "random". Στη πραγματικότητα, είναι pseudorandom number generator, δηλαδή οι αριθμοί που παράγει ακολουθούν ένα συγκεκριμένο set εντολών. To hint μας αναφέρει τον `"Makoto Matsumoto"`, ο οποίος έγινε γνωστός για την δημιουργία του [Mersenne Twister](https://en.wikipedia.org/wiki/Mersenne_Twister), ενός αλγορίθμου που παράγει ψευδοτυχαίους αριθμούς. Με ένα απλό Google search, μπορούμε να επιβεβαιώσουμε πως το "random" module της Pyhton χρησιμοποιεί στη πραγματικότητα τον Mersenne Twister.

Άμα παρατηρήσουμε το [Disadvantages](https://en.wikipedia.org/wiki/Mersenne_Twister#Disadvantages) section του wikipedia article, βλέπουμε το εξής:
```
Is not cryptographically secure, unless the CryptMT variant (discussed below) is used. The reason is that observing a sufficient number of iterations (624 in the case of MT19937, since this is the size of the state vector from which future iterations are produced) allows one to predict all future iterations.
```
Επομένως, αν με κάποιο τρόπο ένας attacker γνωρίζει `624 consecutive iterations (outputs)` του Mersenne Twister, μπορεί να ξέρει και όλα τα επόμενα. 

Στο δικό μας case, γνωρίζουμε 78 πολυώνυμα των οποίων οι ρίζες είναι όλες outputs του random module της Python, δηλαδή του Mersenne Twister. Κάθε πολυώνυμο έχει 8 ρίζες, και όλα τα πολυώνυμα προσαρτώνται στο output με τη σειρά που υπολογίστηκαν. Επιπλέον, γνωρίζουμε πως για κάθε πολυώνυμο, οι ρίζες έχουν παραχθεί με αύξουσα σειρά, δηλαδή η πιο μικρή ρίζα παράχθηκε πρώτη, και η μεγαλύτερη τελευταία (επομένως, ξέρουμε το ολικό order των outputs του Mersenne Twister). Τέλος, έχουμε 78 πολυώνυμα, με 8 ρίζες το καθένα. Αυτό σημαίνει πως αν βρούμε τις ρίζες του καθενός με τη σωστή σειρά, θα ξέρουμε `78*8 = 624 iterations (outputs)` του Mersenne Twister, ακριβώς όσα χρειαζόμαστε για να το σπάσουμε!

Η [συγκεκριμένη](https://github.com/kmyk/mersenne-twister-predictor) βιβλιοθήκη θα μας βοηθήσει σε αυτό ακριβώς.

### To RSA κομμάτι τις επίλυσης

Αφού κάνουμε train το Mersenne Twister Predictor με τα σωστά values, μπορούμε να ξέρουμε και όλα τα επόμενα outputs, ακριβώς έτσι όπως έγιναν στο αρχικό script. Επομένως, αφού τα `x0, x1` και `poly` επιλέχθηκαν τυχαία χρησιμοποιώντας πάλι τον Mersenne Twister, μπορούμε να ξέρουμε ακριβώς πια values είχαν, αρκεί να επαναλάβουμε 1-1 τον αρχικό κώδικα στον solver μας. Γνωρίζοντας τα `x0,x1` και `poly`, στη συνέχεια μπορούμε να υπολογίσουμε ακριβώς τα ίδια `p,q` με το αρχικό πρόγραμμα, και συνεπώς και το `public modulus (n)`. Έτσι, μπορούμε στη συνέχεια να υπολογίσουμε το `Φ(n)` μέσω του `sympy` (αφού p και q είναι composite, και επομένως το n είναι εύκολα παραγοντοποιήσιμο) και μέσω του `Public Exponent (e)` να βγάλουμε το `Private Exponent (d)` ως `d = pow(e, -1, Φ(n))`.

Μπορούμε μετά να αποκρυπτογραφήσουμε το flag με standard RSA.

### Κώδικας επίλυσης

```py
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
```

## Σημαία

```
FLAG{https://www.youtube.com/watch?v=-Djq3QihTyA}
```
