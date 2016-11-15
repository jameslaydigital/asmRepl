; Create string in heap: "Program is running. Cool. Exit? (y/n) >"
wrtc 80 0
wrtc 114 1
wrtc 111 2
wrtc 103 3
wrtc 114 4
wrtc 97 5
wrtc 109 6
wrtc 32 7
wrtc 105 8
wrtc 115 9
wrtc 32 10
wrtc 114 11
wrtc 117 12
wrtc 110 13
wrtc 110 14
wrtc 105 15
wrtc 110 16
wrtc 103 17
wrtc 46 18
wrtc 32 19
wrtc 67 20
wrtc 111 21
wrtc 111 22
wrtc 108 23
wrtc 46 24
wrtc 32 25
wrtc 69 26
wrtc 120 27
wrtc 105 28
wrtc 116 29
wrtc 63 30
wrtc 32 31
wrtc 40 32
wrtc 121 33
wrtc 47 34
wrtc 110 35
wrtc 41 36
wrtc 32 37
wrtc 62 38

label start
movc R1 0
movc R2 39
syscall print   ; prompt user with message

movc R1 39      ; take user input
syscall read

read R1 39      ; if user did not enter 'y', jump back to start
cmpc R1 121
jnel start

syscall exit    ; exit
