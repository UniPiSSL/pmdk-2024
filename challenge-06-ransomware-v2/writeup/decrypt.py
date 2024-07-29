#!/bin/env python3

from ctypes import CDLL
import struct
import os

OUT_DIR = "files_decrypted"
ENC_EXT = ".sus"
ENC_DIR = "files"

PNG_HEADER = bytes([137, 80, 78, 71, 13, 10, 26, 10])

libc = CDLL("/lib/x86_64-linux-gnu/libc.so.6")
seed = struct.unpack('Q', PNG_HEADER)[0]
print(f"Seed = {seed}")
libc.srand(seed)

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


if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

enc_files = os.listdir(ENC_DIR)
data = []

for file in enc_files:
	if file.endswith(ENC_EXT):
		data.append(parse_file(file))

sorted_data = sorted(data, key=lambda x: x[0])

for file in sorted_data:
	decrypt_file(file)
