#This file contains some useful python commands that you might need for P2

#Read information concerning the executable file
e = ELF("./demo1")
#This elf object contains a dictionary of all symbols and their addresses
main_addr = e.symbols["main"]
#Note that if PIE is not enabled, the address of main will not change

#main_addr is a decimal value here (an integer). When using hex(main_addr)
#we generate a string which is the hexadecimal representation of main_addr
print(hex(main_addr))

#If you need to convert a series of bytes (for example 0xabcd) to the corresponding string,
#you can use
value_as_integer.to_bytes(4, "little")
#or
value_as_integer.to_bytes(4, "big")
#this will create a string padded to a size of 4 bytes. The second argument sets the used byte
#ordering, you can choose between little and big endian


#The 'process' command of pwntools is quite powerful! We can set the executable, all the arguments, the environment etc
#If you just want to execute the program, you will only need p = process("./prog")
p = process(executable="./demo1", argv=["not_demo1"], env={"SECRET" : "super-secret-password"})

#To send some string to the process, you can use
p.sendline(my_byte_string)
#Note that sendline adds an additional \n at the end of the
#payload, so make sure that you actually want to do this
#Alternatively, you could use
p.send(another_byte_string)
#to ommit the \n at the end

#Assume that we want to receive all input that the program sends us up to a specific string. For that
#we can use recvuntil() as follows:
p.recvuntil("some string")
#This will 'use up' all the input up to the defined string

#Converting addresses from the program output to actual integer representations can be done using 
addr_as_int = int(addr_as_string, 16) 
#The first argument here is the string that we want to convert to an integer. The second argument is
#the base of the used number system. For hexadecimal, we use 16. For octal we would use 8 and for decimal
#we would use 10

#To receive a line up to the newline character we can use
p.recvline()
#Note that each recv... function returns the received data as a byte string

#If you want to interact with the process that you are attacking, you can use
p.interactive()
#to switch to interactive mode.

#If you want to use GDB with your exploit, we recommend that you use the template command to easily create
#a python template which provided exactly this functionality. By calling
template ./demo2 > demo2_exploit.py
#you will create a template exploit for demo2 and safe it to demo2_exploit.py
#Note that this is not a python command but a command that you need to enter in your terminal

#If you want to use the debugger feature, make sure that you start tmux by executing
tmux
#in the terminal. After that you can call your exploit template with
python demo2_exploit GDB
#This will split the tmux window and will provide you with a gdb instance.


#Some commands in pwntools, especially the oens that create assembly code for you, depend on the current architecture
#you can use
context.arch = "amd64"
#or
context.arch = "i386" 
#to set the architecture correctly
#For most of the hacklets, you will not need to do this explicitly

#If you need to create shellcode, I recommend that you use the 'shellcraft' module. 
#For example
shellcraft.amd64.infloop()
#gives you assembly instructions which perform an infinite loop if executed. Note that the
#stuff returned by shellcraft is NOT machine code but a string of assembly instructions. To 
#actually get executable code, you will need the asm instruction like
payload = asm(shellcraft.amd64.infloop())
#If you manage to get such a payload in the programs memory and the program actually executes your payload you are good to go.

#In general, you should always have a look at 
https://docs.pwntools.com
#if you are stuck or have problems with the commands

#Some gdb commands
#Create a breakpoint at beginning of main method
b main
#Start program
r / run #the single-letter commands are mostly shorhands for the longer commands
#Continue until next breakpoint (only makes sense if the program is already running)
c 
#Set watchpoint on variable. This means that gdb will break everytime a certain variable changes it's value
watch variable_name
#Print contents of a variable
p variable
#Print address of a variable
p &variable
#Calculate offset between two variables
p (size_t)&var1 - (size_t)&var2
#Inspect a memory location, for example an array. In this example we would inspect the first 10 elements of the array arr and interpret them as strings
x/10s arr
#Show current stack frame information (old rip, where is it stored, etc. Useful for buffer overflows)
info f
#If you need a specific functionality of gdb -> GOOGLE IS YOUR FRIEND




#Note that this assignment is not a programming task, your solutions will most likely only need a few lines of code, this is fine!
#We do also not enforce some weird coding standard, just make sure that you UNDERSTAND how your solution works and why it works.
#In general, all the exploitation techniques that you need should have been covered in the lecture
#You might notice that there is a big difference between learning about exploits and performing them yourself. 
#If you do not know where to start or how to tackle the tasks, I would recommend that you google for
"exploit writeups"
#and read how other people solved (much more complicated) exploitation challenges. 

