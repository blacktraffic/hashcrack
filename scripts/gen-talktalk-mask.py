#!/usr/bin/python3

def talktalkmask(mask,caps,digits):

    if (caps>=1):
        talktalkmask(mask+'?1',caps-1,digits)
        
    if (digits>=1):
        talktalkmask(mask+'?2',caps,digits-1)
        
    if caps==0 and digits==0:
        print("ABCDEFGHIJKLMNOPQRSTUVWXYZ,0123456789,"+mask)
        

talktalkmask('',5,3)
            
