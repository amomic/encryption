from pwn import *

context.terminal = ['tmux', 'splitw', '-h']


p = gdb.debug("./demo2")
p.sendline(b"\x61"*32)
p.interactive()


#print(p.recvall())