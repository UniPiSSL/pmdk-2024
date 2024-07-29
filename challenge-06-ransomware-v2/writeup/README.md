# ransomware-v2

| Δοκιμασία | ransomware-v2 |
| :------- | :----- |
| Δυσκολία | Δύσκολη |
| Κατηγορία | Αντίστροφη Μηχανική |
| Λύσεις | 7 |
| Πόντοι | 555 |

## Επισκόπηση Δοκιμασίας

Ανάλυση ενός λυτρισμικού με σκοπό την εύρεση ευπάθειας στον αλγόριθμο που χρησιμοποιείται για την κρυπτογράφηση των αρχείων.

## Επίλυση

Ξεκινώντας, με την αποσυμπίεση της δοκιμασίας παρατηρούμε:

 1. Το αρχείο free_0days.
 2. Έναν κατάλογο files ο οποίος περιέχει αρχεία με κατάληξη .sus

Χρησιμοποιώντας την εντολή file (σε ένα περιβάλλον Linux) μπορούμε να δούμε τον τύπο του αρχείου `free_0days`

```
$ file free_0days

free_0days: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=139ca132c1f8d8506da00584bc6bc54362c95ca9, for GNU/Linux 3.2.0, with debug_info, not stripped
```

οπότε το `free_0days` είναι ένα `ELF 64bit` εκτελέσιμο με σύμβολα αποσφαλμάτωσης.

Τώρα που γνωρίζουμε με τι τύπο αρχείου έχουμε να κάνουμε μπορούμε να χρησιμοποιήσουμε έναν απομεταγλωττιστή (decompiler) ώστε να κατανοήσουμε τις ενέργειες που πραγματοποιεί το εκτελέσιμο.

Για τους σκοπούς αυτής της αναφοράς θα χρησιμοποιηθεί ο απομεταγλωτιστής `IDA - Hexrays`.


Η πρώτη συνάρτηση που καλείται πάντα σε ένα ELF εκτελέσιμο είναι η main (για τους σκοπούς αυτής της αναφοράς - στην πραγματικότητα είναι η `_start`).

Οπότε θα ξεκινήσουμε την ανάλυση μας από την συνάρτηση main.
Στην `IDA Hexrays` επιλέγουμε την `main` από το function list και πατάμε F5 ώστε να δημιουργηθεί ο ψευδοκώδικας.

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  unsigned int seed; // eax
  size_t i; // [rsp+18h] [rbp-8h]

  fetch_filenames(*argv);
  seed = generate_rng_seed();
  srand(seed);
  for ( i = 0LL; i < filenames_sz; ++i )
    enc_file(filenames[i], i);
  clean_up();
  return 0;
}
```

Στην αρχή η main καλεί την συνάρτηση fetch_filename η οποία παίρνει σαν όρισμα το `*argv` η ισοδύναμα το `argv[0]`.

Τι είναι όμως το `argv`?

Το `char* argv[]` είναι ένας πίνακας από αλφαριθμητικά στον οποίο αποθηκεύονται τα ορίσματα που περνάμε στο εκτελέσιμο από την γραμμή εντολών.

π.χ Aν έχουμε ένα εκτελέσιμο `a.bin` και το τρέξουμε έτσι:
```
./a.bin argument1 argument2
```
τότε: 
```
argv[0] = "./a.bin"
argv[1]  = "argument1"
argv[2] = "argument2"
...
```

'Eτσι λοιπόν το όρισμα που περνάει στην fetch_filename είναι η διαδρομή του εκτελέσιμου άρα στην περίπτωση μας `./free_0days`.

Προχωράμε στην ανάλυση της `fetch_filenames`

```c
void __cdecl fetch_filenames(const char *prog_name)
{
  size_t v1; // rax
  size_t sz; // [rsp+10h] [rbp-30h]
  DIR *dir; // [rsp+18h] [rbp-28h]
  size_t filename_sz; // [rsp+20h] [rbp-20h]
  dirent *entry; // [rsp+30h] [rbp-10h]
  char *filename; // [rsp+38h] [rbp-8h]

  dir = opendir("."); // 1
  if ( !dir )
  {
    perror("Error opening directory");
    exit(-1);
  }
  sz = 0LL;
  while ( 1 )
  {
    entry = readdir(dir); // 2
    if ( !entry || sz > 0xFE )
      break;
    if ( strcmp(entry->d_name, ".") // 3
      && strcmp(entry->d_name, "..")
      && strcmp(entry->d_name, prog_name + 2)
      && !strncmp(entry->d_name, "ch4ll3ng_", 9uLL) )
    {
      filename_sz = strlen(entry->d_name) + 1;
      filename = (char *)malloc(filename_sz); // 4

       // 5
      strncpy(filename, entry->d_name, filename_sz);
      v1 = sz++;
      filenames[v1] = filename;
    }
  }

  // 6
  filenames_sz = sz;
  closedir(dir);
}
```

1. Ανοίγει τον τρέχων κατάλογο χρησιμοποιώντας την συνάρτηση `opendir` η οποία επιστρέφει έναν δείκτη σε μια δομή `DIR` η οποία περιγράφει έναν κατάλογο.

Στην συνέχεια εκτελεί τις παρακάτω ενέργειες μέχρι να έχουν ελεγχθεί όλα τα στοιχεία του τρέχοντος καταλόγου:

2. Διαβάζει το επόμενο στοιχείο του τρέχοντος καταλόγου.
3. Ελέγχει αν:
    - Το όνομα του στοιχείου δεν (`d_name`) είναι `.` ή `..`
    - Το όνομα του στοιχείου δεν είναι το όνομα του εκτελέσιμου.
    - Το όνομα του στοιχείου αρχίζει με `chall3ng_`.

Αν ισχύουν αυτές οι συνθήκες τότε αποθηκεύει το όνομα του στοιχείου στον καθολικό (global) πίνακα filenames.

Στο τέλος αποθηκεύει τον αριθμό τον στοιχείων που εκχωρήθηκαν στον πίνακα filenames στην καθολική μεταβλητή `filenames_sz`.

Συνεχίζουμε την ανάλυση της `generate_rng_seed()`:

```__int64 __cdecl generate_rng_seed()
{
  int fd; // [rsp+Ch] [rbp-14h]
  __int64 seed; // [rsp+10h] [rbp-10h] BYREF
  unsigned __int64 v3; // [rsp+18h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  fd = open(filenames[0], 0);
  if ( fd == -1 )
  {
    perror("Error opening file");
    exit(-1);
  }
  read(fd, &seed, 8uLL);
  return seed;
}
```

H οποία πραγματοποιεί μια πολύ απλή λειτουργία:

Ανοίγει το πρώτο αρχείο από τον πίνακα filenames και διαβάζει τα πρώτα 8 bytes αποθηκεύοντας τα στην μεταβλητή seed τύπου `int64` της οποίας την τιμή στην συνέχεια επιστρέφει.

Στην συνέχεια αυτή η τιμή χρησιμοποιείτε  ως τιμή-σπόρος για την αρχικοποίηση μιας Γεννήτριας Ψευδοτυχαίων Αριθμών (PRNG) με την κλήση της συνάρτησης `srand()`.

Σε αυτό το σημείο, ο πίνακας `filenames` περιέχει τα ονόματα των αρχείων του τρέχοντος καταλόγου που ξεκινούν με `chall3ng_`, η μεταβλητή `filenames_sz` περιέχει το πλήθος των αρχείων, και τα πρώτα 8 bytes του πρώτου αρχείου έχουν χρησιμοποιηθεί για την αρχικοποίηση της γεννήτριας ψευδοτυχαίων αριθμών.

Αφού έχει γίνει λοιπόν αυτή η προεργασία η συνάρτηση `main` καλεί την συνάρτηση `enc_file` για κάθε αρχείο μέσα στον πίνακα `filenames`.

```
  for ( i = 0LL; i < filenames_sz; ++i )
    enc_file(filenames[i], i);
```

```
void __cdecl enc_file(const char *filename, unsigned int id)
{
  size_t file_sz; // [rsp+18h] [rbp-18h]
  char *buf; // [rsp+20h] [rbp-10h]
  char *enc_filename; // [rsp+28h] [rbp-8h]

  // 1
  file_sz = get_file_sz(filename);
  buf = (char *)malloc(file_sz);
  read_file(filename, buf, file_sz);
  
  // 2
  enc_filename = append_ext(filename);
  
  // 3
  enc_data(buf, file_sz);
  create_enc_file(enc_filename, buf, file_sz, id);

  free(enc_filename);
  free(buf);
}
```

Η συνάρτηση `enc_file` πραγματοποιεί της παρακάτω λειτουργίες:

1. Διαβάζει τα περιεχόμενα του κάθε αρχείου.
2. Δημιουργεί το όνομα του νέου "κρυπτογραφημένου" αρχείου, προσθέτοντας στο όνομα του αρχείου την κατάληξη `.sus`.
3. Κρυπτογραφεί τα περιεχόμενα του αρχείου και αποθηκεύει το κρυπτοκείμενο σε ένα νέο αρχείο.

```
void __cdecl enc_data(char *data, size_t sz)
{
  size_t i; // [rsp+18h] [rbp-8h]

  for ( i = 0LL; i < sz; ++i )
    data[i] ^= rand() % 256;
}
```

H συνάρτηση `enc_data` κρυπτογραφεί με έναν πολύ απλό τρόπο τα δεδομένα του αρχείο:

Κάθε byte του αρχείου γίνεται xor με έναν αριθμό που παράγεται από την γεννήτρια ψευδοτυχαίων αριθμών.


Στην συνέχεια η συνάρτηση `create_enc_file` θα δημιουργήσει το νέο κρυπτογραφημένο αρχείου όπου:



```
void __cdecl create_enc_file(const char *filename, char *data, size_t sz, unsigned int id)
{
  unsigned int ida; // [rsp+4h] [rbp-2Ch] BYREF
  size_t sza; // [rsp+8h] [rbp-28h]
  char *dataa; // [rsp+10h] [rbp-20h]
  const char *filenamea; // [rsp+18h] [rbp-18h]
  int fd; // [rsp+2Ch] [rbp-4h]

  filenamea = filename;
  dataa = data;
  sza = sz;
  ida = id;
  fd = open(filename, 577, 384LL);
  if ( fd == -1 )
  {
    perror("open");
    exit(-1);
  }
  write(fd, &ida, 4uLL); // 1
  write(fd, dataa, sza); // 2
  close(fd);
}
```

1. Τα 4 πρώτα bytes περιέχουν τον Α/Α του αρχείο (id) κωδικοποιημένο σε little endian.

2. Τα επόμενα **n** bytes περιέχουν το κρυπτογραφημένο περιεχόμενο του αρχείου.

# Αποκρυπτογράφηση
Όπως είδαμε παραπάνω γνωρίζουμε:

1. Η τιμή-σπόρος της γεννήτριας ψευδ. αριθμών είναι τα πρώτα 8 bytes του πρώτου αρχείου.

2. Την σειρά που κρυπτογραφήθηκαν τα αρχεία - αφού τα πρώτα 4 bytes των κρυπτογραφημένων αρχείων περιέχουν τον Α/Α τους κωδικοποιημένο σε little endian.

3. Η κρυπτογράφηση των περιεχομένων των αρχείων γίνεται κάνοντας xor καθε byte του αρχείου με έναν αριθμό από την γεννήτρια ψευδ. αριθμών.

Αν παρατηρήσουμε τα ονόματα των κρυπτογραφημένων αρχείων που μας δίνονται μπορούμε να συμπεράνουμε ότι πρόκειται για κρυπτογραφημένα αρχεία png.

Διαβάζοντας το πρότυπο για τον τύπο αρχείου PNG (http://www.libpng.org/pub/png/spec/1.2/)

παρατηρούμε το παρακάτω:

(http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html#PNG-file-signature)

```
The first eight bytes of a PNG file always contain the following (decimal) values:

   137 80 78 71 13 10 26 10
```

Το οποίο σημαίνει ότι όλα τα png αρχεία ξεκινάνε με τα παραπάνω bytes και άρα η τιμή σπόρος που χρησιμοποιείται για την αρχικοποίηση της γεννήτριας είναι πάντα η ίδια.

Έτσι λοιπόν μπορούμε να αναπαράγουμε τους αριθμούς που χρησιμοποιήθηκαν για την κρυπτογράφηση του κάθε αρχείου αφού γνωρίζουμε την σειρά που κρυπτογραφήθηκαν (μέσα από τον Α/Α στα πρώτα 4 bytes).

Αφού έχουμε αποκρυπτογραφήσει όλα τα αρχεία, θα βρούμε το flag στην εικόνα `ch4ll3ng_flag.png`.

## Δέσμη ενεργειών επίλυσης.
```
#!/bin/env python3

from ctypes import CDLL
import struct
import os

OUT_DIR = "dec"
ENC_EXT = ".sus"
ENC_DIR = "files"

PNG_HEADER = bytes([137, 80, 78, 71, 13, 10, 26, 10])

libc = CDLL("/lib/x86_64-linux-gnu/libc.so.6")
seed = struct.unpack('Q', PNG_HEADER)[0]
print(f"Seed = {seed}")

def parse_file(filename):
	with open(f"{ENC_DIR}/{filename}", "rb") as f:
		data = f.read()

	file_id = struct.unpack("<I", data[:4])[0]
	return file_id, filename[:-len(ENC_EXT)], data[4:]


def decrypt_file(file: tuple):
	_, filename, data = file
	out = b""

	for i in range(len(data)):
		out += bytes([data[i] ^ (libc.rand() % 256)])

	with open(f"{OUT_DIR}/{filename}", "wb") as f:
		f.write(out)

libc.srand(seed)

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

enc_files = os.listdir(ENC_DIR)
data = []

for file in enc_files:
	data.append(parse_file(file))

sorted_data = sorted(data, key=lambda x: x[0])

for file in sorted_data:
	decrypt_file(file)
```

## Σημαία

```
FLAG{m4g1c_byt3s_54v3_f1l35}
```
