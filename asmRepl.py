#!/usr/bin/python

import sys

stack = [] #init stack
functions = {}
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
    isBuff = False
    if fname != '':
        isBuff = True
        functionBuffer = functions[fname][:] #copy
        functionBuffer.reverse()

    while True:
        cmd = functionBuffer.pop() if isBuff else sys.stdin.readline().strip()
        if cmd in ("exit", "return"): return
        if cmd != "" and cmd[0:2] != "//":
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

# how do you handle control flow?
#     like python REPL
#     probably record a function, then runDef until loop is satisfied
#
# how do you handle functions?
#     record command strings in a list-buffer, then pass that to runDef(), which has a loop just like the one above
# 
# Thought: perhaps the main loop should be a function and runDef happens immediately
