movc R1 65
wrtc 69 0
syscall printchar
movc R1 67
cmpc R1 66
jgtl prog
syscall printchar
label prog
read R1 0
syscall printchar
syscall printchar
syscall printchar
exit
