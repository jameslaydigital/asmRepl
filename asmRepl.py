#!/usr/bin/python
import sys

# SOME NOTES:
# You can't perform control flow by writing gotos because the interpreter will
# not know not to execute them as you're writing them, so this format we have
# here is that input switches from stdin to a buffer when we're writing
# functions or code blocks.

stack = [] #init stack
functions = {}
labels = {}
instructions = []
reg = {"ip" : 0}

def printError(string):
    sys.stderr.write(str(string))
    sys.stderr.write("\n")

##############
# OPERATIONS #
##############

# operations get their operands from the stack, but some operations will take
# up to two arguments, for instance a constant or a modifier token

def subDef():
    if len(stack) > 1:
        b = stack.pop() or 0
        a = stack.pop() or 0
        stack.append(a-b)
        return stack[-1]
    else:
        return "stack arguments error: not enough args on the stack"

def addDef():
    if len(stack) > 1:
        b = stack.pop() or 0
        a = stack.pop() or 0
        stack.append(a+b)
        return stack[-1]
    else:
        return "stack arguments error: not enough args on the stack"

def negDef():
    if len(stack) > 0:
        a = stack.pop() or 0
        stack.append(a*-1)
        return stack[-1]
    else:
        return "stack arguments error: not enough args on the stack"

def pushDef(arg):
    stack.append(int(arg))
    return arg

def popDef():
    if len(stack) > 0:
        return stack.pop()
    else:
        return "stack arguments error: not enough args on the stack"

def printDef():
    return stack[-1]

def intDef(vector):
    return interrupts[vector]()

def jumpDef(loc):
    reg["ip"] = labels[loc]
    return

def makeFuncBuffDef(fname):
    cmd = ""
    functions[fname] = []
    while cmd.strip() != "return":
        sys.stderr.write("> ")
        cmd = sys.stdin.readline().strip()
        functions[fname].append(cmd)
    functions[fname].append("return")

# This is your main REPL runloop
def runDef(fname=''):
    while True:
        cmd = nextInstruction()
        if cmd != "":
            cmds = cmd.split(' ')
            if cmds[0] in symbols:
                if len(cmds) == 1:
                    printError(symbols[cmds[0]]())
                if len(cmds) == 2:
                    printError(symbols[cmds[0]](cmds[1]))
                if len(cmds) == 3:
                    printError(symbols[cmds[0]](cmds[1], cmds[2]))
            else:
                printError("command not recognized: "+cmd+"\n")


def nextInstruction():
    reg["ip"] = reg["ip"] + 1
    if reg["ip"] >= len(instructions):
        instructions.append(sys.stdin.readline().strip())
    return instructions[reg["ip"]].split(";").strip().split(" ")

##############
# INTERRUPTS #
##############

# interrupts get their arguments from the "stack" variable, in the same way as
# the C calling convention in x86 assembly. Interrupts strictly do not take
# "arguments", as the operations sometimes can.

def printInt():
    length = stack.pop()
    if length <= len(stack):
        print ''.join([chr(stack.pop()) for i in range(length)])
        return length
    else:
        stack.append(length)
        return 0


# interrupts is used only by intDef
interrupts = { "print" : printInt }

# symbols contains all possible operations
symbols = { "add" : addDef,
    "sub" : subDef,
    "neg" : negDef,
    "push" : pushDef,
    "pop" : popDef,
    "print" : printDef,
    "func" : makeFuncBuffDef,
    "call" : runDef,
    "int" : intDef,
}

runDef()

# TODO: control flow
#     Record as anonymous function, then run until loop conditions are
#     satisfied.
