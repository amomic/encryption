from pwn import *
context.terminal = ['tmux', 'splitw', '-h']

#Start the process
#p = process(executable="./demo1", argv=["not_demo1"], env={"SECRET" : "super-secret-password"})
p = gdb.debug("./demo1")
#Read information from the elf file
e = ELF("./demo1")

#Get address of main function from elf
main = e.functions["main"]
print("Main at ", main.address)

#Send it to program as a string i.e. "0x40ab0..."
p.sendline(hex(main.address))

p.recvuntil(" random stack variable is at ")

stack_addr = p.recvuntil("\n")[:-1]

print("Got stack address", stack_addr)
stack_addr = int(stack_addr, 16)
print(stack_addr)

offset = 0x4

xaddr = stack_addr + offset

p.sendline(hex(xaddr))

p.interactive()