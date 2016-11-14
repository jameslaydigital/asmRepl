#!/usr/bin/python

import sys

sregs = {
    "ip" : 0 #instruction pointer
}

#general-purpose registers
gregs = {
    "R1" : 0,
    "R2" : 0,
    "R3" : 0,
    "R4" : 0
}

stack = []
cmdBuffer = []
labels = {}

#syscalls simulate host OS system calls
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
    print gregs

def showlabelsSysCall():
    sys.stdout.write("labels: ")
    print labels

def showsregsSysCall():
    sys.stdout.write("special registers: ")
    print sregs


syscalls = {
    "print"     : printSysCall,
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
    stack.append(int(gregs[reg]))

def poprOp(reg):
    gregs[reg] = stack.pop()

def movcOp(reg, value):
    gregs[reg] = int(value)

def movrOp(regA, regB):
    gregs[regA] = gregs[regB]

def jmplOp(reg):
    sregs['ip'] = gregs[reg]-1

## JUMPS ##
def jmplOp(lbl):
    #unconditional jump
    sregs['ip'] = labels[lbl]-1
    #-1 because the ip will be incr after this very op is ran

def jeqlOp(lbl):
    if sregs["bf"] == 0:
        jmplOp(lbl)

def jnelOp(lbl):
    if sregs["bf"] != 0:
        jmplOp(lbl)

def jgtlOp(lbl):
    if sregs["bf"] == 1:
        jmplOp(lbl)

def jltlOp(lbl):
    if sregs["bf"] == -1:
        jmplOp(lbl)

def cmprOp(regA, regB):
    if gregs[regA] >  gregs[regB]: sregs["bf"] = 1
    if gregs[regA] == gregs[regB]: sregs["bf"] = 0
    if gregs[regA] <  gregs[regB]: sregs["bf"] = -1


def addrOp(regA, regB):
    gregs[regA] = gregs[regA]+gregs[regB]

def exitOp():
    exit(0)

def lablOp(lname):
    labels[lname] = sregs['ip']+1

def syscallOp(vector):
    syscalls[vector]()

def dumpOp():
    showstackSysCall()
    showregsSysCall()
    showsregsSysCall()
    showlabelsSysCall()

operations = {
    "addr"  : addrOp,   #add registers and store result in first register
    "movc"  : movcOp,   #copy constant to register
    "movr"  : movrOp,   #copy register to register
    "pshr"  : pushrOp,  #push constant or register
    "popr"  : poprOp,   #pop to register

    "labl"  : lablOp,    #save label to labels as name lname

    "cmpr"  : cmprOp,  #compare two registers
    "jmpl"  : jmplOp,  #jmp unconditionally
    "jeql"  : jeqlOp,  #jmp if equal
    "jnel"  : jnelOp,  #jmp if not equal
    "jgtl"  : jgtlOp,  #jmp if greater than
    "jltl"  : jltlOp,  #jmp if less than
    "dump"  : dumpOp,

    "exit"  : exitOp,   #exits program. Should be a syscall but...
    "syscall" : syscallOp   #call constant vector, like an interrupt
}

class Operation:
    def __init__(self, cmd):
        noCmts = cmd.strip().split(";")[0]
        opsArgs = cmd.split(" ")
        length = len(opsArgs)

        self.name = opsArgs[0]
        self.op1 = opsArgs[1] if length > 1 else None
        self.op2 = opsArgs[2] if length > 2 else None


def runCmd(cmd):
    op = Operation(cmd)
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
    sregs['ip'] += 1

def printError(msg):
    sys.stderr.write(msg+"\n");

#run loop
def run():
    while True:
        if sregs['ip'] < len(cmdBuffer):
            runCmd(cmdBuffer[sregs['ip']])
        else:
            printError("END OF PROGRAM")
            exit(1)

def fillCmdBuff():
    cmd = ""
    while cmd != "exit":
        cmd = sys.stdin.readline().strip()
        cmdBuffer.append(cmd)
    run()

fillCmdBuff()
