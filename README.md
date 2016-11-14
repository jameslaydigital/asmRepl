# asmRepl
An interpreted assembly.

Try running it:

    ./vm.py < new.asm
    ./asmRepl.py < example.asm
    ./asmRepl.py ### interactive session, type exit to leave
    
Currently, the runtimes are built on python, but they could easily be converted to a language like C.
Really, a simple project indeed.

It's worth noting that `vm.py` is a non-interactive, but feature-complete runtime, and does not share the same language syntax as `asmRepl.py`.  `asmRepl.py`, thus, is not feature-complete, but is interactive and is a work in progress that currently implements a stack and functions. It does not have complete control-flow capabilities yet.
