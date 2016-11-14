#!/usr/bin/python

import sys

#general-purpose registers
regs = {
    "R1" : 0,
    "R2" : 0,
    "R3" : 0,
    "R4" : 0,
    "ip" : 0,   #instruction pointer
    "bf" : 0    #boolean flag (for comparisons)
}

stack = []
cmdBuffer = []
labels = {}
heap = [0]*(1024*1024) #fixed heap for now

#syscalls simulate host OS system calls
def printcharSysCall():
    sys.stdout.write(chr(regs["R1"]))

def printSysCall():
    #TODO
    return

def readSysCall():
    #TODO
    return

def exitSysCall():
    exit(0)

def showstackSysCall():
    sys.stdout.write("stack: ")
    print stack

def showregsSysCall():
    sys.stdout.write("general registers: ")
    print regs

def showlabelsSysCall():
    sys.stdout.write("labels: ")
    print labels

def showsregsSysCall():
    sys.stdout.write("special registers: ")
    print regs


syscalls = {
    "print"     : printSysCall,
    "printchar" : printcharSysCall,
    "showstack" : showstackSysCall,
    "showregs"  : showregsSysCall,
    "showlabels": showlabelsSysCall,
    "showsregs" : showsregsSysCall,
    "read"      : readSysCall,
    "exit"      : exitSysCall
}



def pushcOp(value):
    stack.append(int(value))

def pushrOp(reg):
    stack.append(int(regs[reg]))

def poprOp(reg):
    regs[reg] = stack.pop()

def movcOp(reg, value):
    regs[reg] = int(value)

def movrOp(regA, regB):
    regs[regA] = regs[regB]

def wrtrOp(reg, mem):
    heap[int(mem)] = regs[regA]

def wrtcOp(value, mem):
    heap[int(mem)] = int(value)

def readOp(reg, mem):
    regs[reg] = heap[int(mem)]

## JUMPS ##
def jmplOp(lbl):
    #unconditional jump
    regs['ip'] = labels[lbl]-1
    #-1 because the ip will be incr after this very op is ran

def jeqlOp(lbl):
    if regs["bf"] == 0:
        jmplOp(lbl)

def jnelOp(lbl):
    if regs["bf"] != 0:
        jmplOp(lbl)

def jgtlOp(lbl):
    if regs["bf"] == 1:
        jmplOp(lbl)

def jltlOp(lbl):
    if regs["bf"] == -1:
        jmplOp(lbl)

def cmprOp(regA, regB):
    cmpcOp(regA, regs[regB])

def cmpcOp(reg, value):
    value = int(value)
    if regs[reg] >  value: 
        regs["bf"] = 1
    if regs[reg] == value:
        regs["bf"] = 0
    if regs[reg] <  value:
        regs["bf"] = -1


def addrOp(regA, regB):
    regs[regA] = regs[regA]+regs[regB]

def addcOp(regA, value):
    regs[regA] = regs[regA]+int(value)

def multOp(regA, regB):
    regs[regA] = regs[regA] * regs[regB]

def exitOp():
    exit(0)

def lablOp(lname):
    labels[lname] = regs['ip']+1

def syscallOp(vector):
    syscalls[vector]()

def dumpOp():
    showstackSysCall()
    showregsSysCall()
    showsregsSysCall()
    showlabelsSysCall()

def noopOp(a=None, b=None):
    return

operations = {
    "addr"  : addrOp,   #add registers and store result in first register
    "addc"  : addcOp,   #add reg to const and store result in register
    "mult"  : multOp,   #multiply regA * regB, store in regA
    "movc"  : movcOp,   #copy constant to register
    "movr"  : movrOp,   #copy register to register

    "wrtr"  : wrtrOp,   #write reg to memory
    "wrtc"  : wrtcOp,   #write const to memory
    "read"  : readOp,   #read memory to register

    "pshr"  : pushrOp,  #push constant or register
    "popr"  : poprOp,   #pop to register

    "cmpr"  : cmprOp,  #compare two registers
    "cmpc"  : cmpcOp,  #compare reg against const 

    "jmpl"  : jmplOp,  #jmp unconditionally
    "jeql"  : jeqlOp,  #jmp if equal
    "jnel"  : jnelOp,  #jmp if not equal
    "jgtl"  : jgtlOp,  #jmp if greater than
    "jltl"  : jltlOp,  #jmp if less than
    "dump"  : dumpOp,
    "label" : noopOp, #it's a keyword
    "noop"  : noopOp, 

    "exit"  : exitOp,   #exits program. Should be a syscall but...
    "syscall" : syscallOp   #call constant vector, like an interrupt
}

class Operation:
    def __init__(self, cmd):
        opsArgs = cmd.split(";")[0].strip().split(" ")
        if cmd != "":
            length = len(opsArgs)
            self.name = opsArgs[0]
            self.op1 = opsArgs[1] if length > 1 else None
            self.op2 = opsArgs[2] if length > 2 else None
            self.ignore = False
        else:
            self.ignore = True


def runCmd(cmd):
    op = Operation(cmd)
    if op.ignore == False:
        if op.name not in operations:
            printError("FATAL: operation '"+op.name+"' not recognized.")
            dumpOp()
            exit(1)
        if op.op1 and op.op2:
            operations[op.name](op.op1, op.op2)
        elif op.op1:
            operations[op.name](op.op1)
        else:
            operations[op.name]()
    regs['ip'] += 1

def printError(msg):
    sys.stderr.write(msg+"\n");

#run loop
def run():
    while True:
        if regs['ip'] < len(cmdBuffer):
            runCmd(cmdBuffer[regs['ip']])
        else:
            printError("END OF PROGRAM")
            exit(1)

def identifyLables():
    loc = 0
    for cmd in cmdBuffer:
        op = Operation(cmd)
        if op.ignore == False:
            if op.name == "label":
                labels[op.op1] = int(loc)
        loc += 1
    # showlabelsSysCall()

def fillCmdBuff():
    cmd = ""
    while cmd != "exit":
        cmd = sys.stdin.readline().strip()
        cmdBuffer.append(cmd)
    identifyLables()
    run()

fillCmdBuff()
