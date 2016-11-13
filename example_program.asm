;add
push 5
push 5
add

;invoke print "interrupt"
push 45
push 44
push 43
push 42
push 4
int print

;call func
func my_function
    ; HELLO WORLD
    push 33
    push 68
    push 76
    push 82
    push 79
    push 87
    push 32
    push 79
    push 76
    push 76
    push 69
    push 72

    push 11  ; length argument
    int print; print interrupt
    return

call my_function
exit
