movc R1 65  ; 65 is ASCII for A
wrtc 69 0   ; writing E to heap location 0
syscall printchar
movc R1 67  ; putting 67 just to 
cmpc R1 66  ; compare against 66
jgtl prog   ; and skip this printchar
syscall printchar
label prog
read R1 0   ; read heap location 0 into R1 register
syscall printchar ; print 3x
syscall printchar
syscall printchar
exit    ; bye
