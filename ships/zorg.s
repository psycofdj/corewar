.name    " Zork "
.comment " This is the first ship ever. "
test:
        ll r0, 0x2ecf           # Load simple code
        ll r1, 0x13e0           # into two registers
test2:
        ll r2 , to - from1      # Load offsets for
        ll r3 , to - from2 + 4  # the two str
        str [r2] , r0           # Write code just
from1:  str [r3] , r1           # before PC
from2:
to: # When the PC reaches here , a check
    # instruction has been written
