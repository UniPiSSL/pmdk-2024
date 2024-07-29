# Lobotomy Kaisen

| Δοκιμασία | Lobotomy Kaisen |
| :------- | :----- |
| Δυσκολία | Δύσκολη |
| Κατηγορία | Κρυπτογραφία (Cryptography) |
| Λύσεις | 8 |
| Πόντοι | 539 |

## Επισκόπηση Δοκιμασίας

Η περιγραφή της δοκιμασίας αναφέρει:
```
Προσπαθώ εδώ και ώρες να ανακτήσω το μυστικό σύνθημα που κρύβεται μέσα στον κώδικα, αλλά μια κρυπτογραφική κατάρα το προστατεύει! Έχεις τη δύναμη να την κερδίσεις;
```
Επιπλέον μας δίνετε ένα zip αρχείο με 4 αρχεία.

### Ο κώδικας κρυπτογράφησης (Python3)

```py
import os
import hashlib
import sympy as sp
from Crypto.Util.number import getPrime, long_to_bytes, bytes_to_long
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Load flag
AES_KEY = bytes_to_long(b'this-is-an-example-key')

if os.path.exists('key.txt'):
    AES_KEY = bytes_to_long(open('key.txt', 'r').read().strip().encode())

# I sure as hell hope you've watched Jujutsu Kaisen,
# otherwise, you sure as hell will, after this challenge :D

class DomainExpansion:

    # Description:
    # The challenge's domain: Illegible AES.
    # It produces an indecipherable output from the given input to confuse the solver.

    def IllegibleAES(self, plaintext, key):
        md5_hash = hashlib.md5(key).digest() # Hash the key to ensure 16 bytes
        cipher = AES.new(md5_hash, AES.MODE_ECB)
        return cipher.encrypt(pad(plaintext, 16))

class CursedTechnique:

    # Description:
    # The challenge's most powerful cursed technique: Repeated RSA
    # It repeatedly encrypts the plaintext using different RSA parameters to deal damage.

    def RepeatedRSA(self, plaintext, iterations):
        output = []
        
        for i in range(iterations):
            p,q = getPrime(512), getPrime(512)
            n = p*q
            e = 0x7
            ciphertext = pow(plaintext, e, n)
            output.append([ciphertext, n])
        
        return output
        
    # Description:
    # The challenge's less powerful cursed technique: PolynomialFunction
    # Given a number, it passes it through a 4th degree polynomial...

    def F(self, x):
        return int(487287452132*pow(x, 4) - 2476267878632*pow(x,3) + 8028242452324*pow(x, 2) - 56195810567274 * x + 232842749872983)


# Now then, time to get a taste :)

CT = CursedTechnique()

transformed_key = CT.F(AES_KEY)
RSA_Result = CT.RepeatedRSA(transformed_key, 7)

output = open("output.txt", "w")
output.write(str(RSA_Result) + "\n")

# Arm yourself.

Domain = DomainExpansion()

flag = open("flag.pdf", "rb").read()
flag_encrypted = Domain.IllegibleAES(flag, long_to_bytes(AES_KEY))

with open("flag.pdf.enc", "wb") as r:
    r.write(flag_encrypted)
```

## Επίλυση

Αρχικά, βλέπουμε πως στο zip του challenge περιλαμβάνονται 4 αρχεία.

1. `Lobotomy_Kaisen.py` : Είναι το κύριο script του challenge που περιλαμβάνει τον κώδικα.
2. `requirements.txt` : Περιέχει της απαραίτητες βιβλιοθήκες (libraries) που χρειάζεται το κύριο script για να τρέξει.
3. `output.txt` : Περιέχει το κρυπτογραφημένο output το οποίο κρυπτογραφήθηκε με το κύριο script.
4. `flag.pdf.enc` : Το κρυπτογραφημένο αρχείο "flag.pdf" που περιέχει τη σημαία

### Με μια πρώτη ματιά

Ας αναλύσουμε πρώτα το κύριο αρχείο `Lobotomy_Kaisen.py`. Με μια πρώτη ματιά βλέπουμε ότι περιέχει 2 κλάσεις και 3 συναρτήσεις συνολικά:

1. Κλάση `DomainExpansion`, συνάρτηση `IllegibleAES(plaintext, key)` : Παίρνει 2 παραμέτρους, εκ των οποίων η μία είναι ένα plaintext (απλό κείμενο σε bytes) και η άλλη είναι ένα key (πάλι σε bytes). Παίρνει το MD5 hash του key (ώστε να είναι πάντα 16 bytes) και χρησιμοποιεί τον κρυπταλγόριθμο `AES` με κλειδί `MD5_HASH(key)` σε mode `ECB` για να κρυπτογραφήσει το `plaintext`. Επιστρέφει το κρυπτογραφημένο plaintext.

2. Κλάση `CursedTechnique`, συνάρτηση `RepeatedRSA(plaintext, iterations)` : Παίρνει 2 παραμέτρους, εκ των οποίων η μία είναι ένα plaintext (σε μορφή int) και η άλλη είναι o αριθμός των επαναλήψεων (int). Στη συνέχεια, σε κάθε επανάληψη εφαρμόζει standard [RSA Encryption](https://el.wikipedia.org/wiki/RSA) πάνω στο αρχικό plaintext (το plaintext δεν αλλάζει) με `τυχαία p και q, διαφορετικά σε κάθε επανάληψη`. Το `e=7` μένει σταθερό. Αφού κρυπτογραφήσει το plaintext, το προσθέτει σε μια λίστα `output` μαζι με το αντίστοιχο `Public Modulus (n)`. Αυτό επαναλαμβάνεται `iterations` φορές, και έπειτα επιστρέφει τη λίστα `output`.

3. Κλάση `CursedTechnique`, συνάρτηση `F(x)` : Παίρνει ως παράμετρο έναν ακέραιο x και υπολογίζει το F(x) με τη δεδομένη συνάρτηση (4ου βαθμού πολυώνυμο, βλέπε τον κώδικα)

### Αναλύοντας το κύριο πρόγραμμα

Το κύριο πρόγραμμα ξεκινάει υπολογίζοντας το `transformed_key = F(AES_KEY)` μέσω της συνάρτησης `F` που περιγράψαμε επάνω. Να σημειωθεί πως εμείς δεν γνωρίζουμε τη τιμή του `AES_KEY`. 

Στη συνέχεια, χρησιμοποιώντας το νέο `tranformed_key`, καλεί την συνάρτηση `RepeatedRSA` με `plaintext = transformed_key` και `iterations = 7`. Το αποτέλεσμα (μια λίστα με 7 δυάδες `[ciphertext, n]`) το γράφει στο `output.txt`, δηλαδή μας είναι γνωστό. 

Έπειτα, διαβάζει τα περιεχόμενα (bytes) του `flag.pdf` (`flag = open("flag.pdf", "rb").read()`) και καλεί την συνάρτηση `IllegibleAES` με παραμέτρους:

1. Τα bytes του `flag.pdf` ως `plaintext`
2. Το byte representation του AES_KEY ως `key` (`long_to_bytes(AES_KEY)`)

Το κρυπτοκείμενο (δηλαδή τα ciphertext bytes) το γράφει στο αρχείο `flag.pdf.enc`.

### Η κύρια ευπάθεια (vulnerability)

Ένα overview υψηλού επιπέδου του προγράμματος είναι πως:

1. Υπάρχει ένας ακέραιος AES_KEY με τον οποίο κρυπτογραφήθηκε το `flag.pdf`. Αν μπορέσουμε να τον ανακτήσουμε, μπορούμε να αποκρυπτογραφήσουμε το `flag.pdf.enc` Και να πάρουμε πίσω το `flag.pdf`.
2. Ξέρουμε ότι το F(AES_KEY) κρυπτογραφήθηκε με RSA 7 φορές, και για αυτές τις 7 φορές γνωρίζουμε τα pairs `[ciphrtext, Public Modulus (n)]`
3. Γνωρίζουμε την συνάρτηση F. Αν μπορέσουμε και ανακτήσουμε το F(AES_KEY), μπορούμε να λύσουμε την εξίσωση F(x) = F(AES_KEY) και να βρούμε (το πολύ) 4 πραγματικές ρίζες (πιθανά x, δηλαδή πιθανά values του AES_KEY).

Το ενδιαφέρον στο συγκεκριμένο challenge είναι το ότι το public exponent (e = 7) είναι ίσο με της επαναλήψεις της συνάρτησης `RepeatedRSA`, δηλαδή για e = 7 έχουμε 7 pairs `[ciphertext (remainder), n (modulus)]`. Αν ψάξουμε στο Google για πιθανά attacks πάνω σε RSA με αυτό το setup, πολύ πιθανό να βρούμε τον όρο `Hastad's Broadcast Attack`, η να διαβάσουμε [αυτό](https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf) το paper. 

Ουσιαστικά αυτό που μας λέει το attack είναι ότι στην αριθμητική ανάλυση, υπάρχει ένα θεώρημα που ονομάζεται [Κινέζικο Θεώρημα Υπολοίπων](https://en.wikipedia.org/wiki/Chinese_remainder_theorem). Με απλά λόγια, αν έχεις κάποιες [ισοτιμίες (congruences)](https://el.wikipedia.org/wiki/%CE%91%CF%81%CE%B9%CE%B8%CE%BC%CE%B7%CF%84%CE%B9%CE%BA%CE%AE_%CF%85%CF%80%CE%BF%CE%BB%CE%BF%CE%AF%CF%80%CF%89%CE%BD#%CE%A3%CF%87%CE%AD%CF%83%CE%B7_%CE%B9%CF%83%CE%BF%CF%84%CE%B9%CE%BC%CE%AF%CE%B1%CF%82) του **ίδιου** αριθμού (x) modulo διαφορετικών αριθμών n (n1, n2, n3, ...) και ξέρεις τα αποτελέσματα αυτών των πράξεων (remainders), μπορείς να υπολογίσεις το `x mod (n1 * n2 * n3 * ...)`. Δηλαδή, αν γνωρίζω για παράδειγμα:

`x mod 11 = 3`
`x mod 17 = 1`
`x mod 24 = 6`

Μπορώ να υπολογίσω το `x mod 11*17*24`, δηλαδή το `x mod 4488`. Και επιπλέον, αν τυχαίνει να ισχύει `x < 4488`, τότε μπορώ να βρω το ίδιο το x! (Στο παραπάνω παράδειγμα, `x = 630`)

Επεκτείνοντας αυτή τη λογική για μεγαλύτερους αριθμούς, ο `Hastad` μας λέει πως αν κάνω RSA πάνω στο ίδιο plaintext (δηλαδή υπολογίζω `c = p^e mod n`) πολλές φορές (`>= e` για την ακρίβεια) και ξέρω τα αποτελέσματα (ciphertext/remainders) και τα modulo (n), τότε μπορώ να ανακτήσω μέσω του Κινέζικου Θεωρήματος Υπολοίπων το `p^e`.

Γιατί? Επειδή:

1. Το `p (plaintext)` είναι σταθερό
2. Το `e = 7` είναι σταθερό
3. Άρα και το `p^e` είναι σταθερό. Είναι σαν το `x` στο παράδειγμα πάνω! Δεν το γνωρίζουμε, αλλά ξέρουμε ότι είναι σταθερό!

**Note:**

Ο Hastad αυτό που μας λέει στη πραγματικότητα είναι ότι:

Όταν υπολογίσουμε: `p^e mod (n1*n2*n3*....)`, τότε αν τα pairs `[ciphertext, n]` που γνωρίζουμε είναι περισσότερα η ίσα του `e` (στο δικό μας case, >= 7), θα ισχύει `p^e < n1*n2*n3*...` άρα `p^e mod (n1*n2*n3*....) = p^e`, δηλαδή το αποτέλεσμα του Κινέζικου Θεωρήματος Υπολοίπων θα είναι `p^e`.

Επομένως, μπορούμε να χρησιμοποιήσουμε τη συνάρτηση `CRT` (Chinese Remainder Theorem) της βιβλιοθήκης sympy: `from sympy.ntheory.modular import crt`

Στη πραγματικότητα όμως, αυτό το value που θα βρούμε θα είναι το `F(AES_KEY)^e` (ξαναδές την ανάλυση του κώδικα). Μπορούμε να πάρουμε την e-οστή ρίζα του αποτελέσματος (7η ρίζα στη προκειμένη περίπτωση) και να απομονώσουμε το `F(AES_KEY)`. 

Αφού γνωρίζουμε τη συνάρτηση F, μπορούμε να τη περάσουμε στο `sympy` και να εξισώσουμε `F(x) = F(AES_KEY)`. Ένα από τα αποτελέσματα (x) θα είναι ακέραιος (γιατί το `F(AES_KEY)` είναι θετικός ακέραιος). Θα χρησιμοποιήσουμε αυτό (για την ακρίβεια, το MD5 hash αυτουνού - πρέπει πρώτα να το μετατρέψουμε σε bytes) για να αποκρυπτογραφήσουμε το `flag.pdf.enc` με standard `AES ECB`.

### Κώδικας επίλυσης

```py
#!/usr/bin/env python3
import hashlib
import sympy as sp
from sympy.ntheory.modular import crt
from gmpy2 import iroot
from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
    
def DecryptAES(ct, key): # Undoes the flag encryption given the key
    md5_hash = hashlib.md5(key).digest()
    cipher = AES.new(md5_hash, AES.MODE_ECB)
    return unpad(cipher.decrypt(ct), 16)

# Open the output file
parser = open("output.txt", "r").readlines()

# Parse the congruences (tuples of [ciphertexts, moduli])
congruences = eval(parser[0])

# Define x as a symbol and parse f(x) in sympy
x = sp.symbols('x')
f = 487287452132*x**4 - 2476267878632*x**3 + 8028242452324*x**2 - 56195810567274 * x + 232842749872983

# Parse remainders and moduli into 2 lists to prepare for CRT
mods = [] # τα διάφορα n
rems = [] # τα διάφορα ciphertexts
for congruence in congruences:
    rems.append(congruence[0])
    mods.append(congruence[1])
 
# Solve for (f(AES_KEY))^7 using CRT 
solution = crt(mods, rems)[0]
print(f"[+] Recovered (f(AES_KEY))^7 = {solution}\n")

# Take the 7th root of the solution to get f(AES_KEY)
obfuscated_key = int(iroot(solution, 7)[0]) #iroot -> integer root
print(f"[+] Recovered f(AES_KEY) = {obfuscated_key}\n")

# Solve the equation f(x) = f(AES_KEY) <=> f(x) - f(AES_KEY) = 0
# for x in order to recover AES_KEY
AES_KEY = sp.solve(f - obfuscated_key, x)[0] # Παίρνουμε το 1ο root
print(f"[+] Recovered AES_KEY = {AES_KEY}\n")

# Read the ciphertext (the encrypted flag file)
encrypted_flag = open("flag.pdf.enc", "rb").read()

# Get its decrypted bytes
decrypted_flag = DecryptAES(encrypted_flag, long_to_bytes(AES_KEY))

# Write the decrypted bytes to a file and we are done
with open("solved.pdf", "wb") as s:
    s.write(decrypted_flag)
    
print(f"[+] Wrote flag to 'solved.pdf'")
```

## Σημαία

```
FLAG{n4h_I’d_w1n_~_s4t0ru_G0Jo}
```