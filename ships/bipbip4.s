.name    "BipBip4"
.comment "Pas un geek, mais simplement un homme 2.0"
init:
        MODE QiRex                                      #3
        LL  r0, 384 - 7                                 #10
        LL  r1, startbuffer - sparse                    #17
        LL  r2, 384 - 7 - 5                             #24
        LDB [r1], 0, endbuffer - startbuffer            #31
sparse:
        NOP NOP NOP NOP NOP                             #align next check to a %64 address
        NOP NOP NOP NOP NOP
        NOP NOP NOP NOP NOP
        NOP NOP NOP NOP NOP
        NOP NOP NOP NOP NOP
        NOP NOP NOP NOP NOP
        NOP NOP NOP
startbuffer:
        STB [r0], 0, endbuffer - startbuffer            #38
        CHECK                                           #40
        B     r2                                        #43
endbuffer:

