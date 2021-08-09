#!/usr/bin/python

import sys
import os
import re

def subsq(state, remains, n, wf):

    #don't do more than this many tweaks
    if n>4:
        if len(state+remains)>4:
            wf.write(state+remains+"\n")
            return
        
    if len(remains)>0:
        c=remains[0]        

        subsq(state+c,remains[1:],n,wf)
        subsq(state,remains[1:],n+1,wf)
       
    else:
        #only output fragments longer than this 
        if len(state)>6:
            wf.write(state+"\n")
        

def subsq_file(filename):

    
    wf = open(filename+".subs","w")
    
    with open(filename,'r', encoding="utf-8") as inpfile:
        l = inpfile.readline()
       
        while l:
            subsq('',l.rstrip(),0,wf)
            l = inpfile.readline()

    wf.close()


def stem_file(filename,pattern):

    wf = open(filename+".stem","w")
    
    with open(filename,'r', encoding="utf-8") as inpfile:
        l = inpfile.readline()

        while l:
            l = re.sub('[^A-Za-z0-9]','',l)

            if isinstance(l, str):
                wf.write(l+"\n")
                
            l = inpfile.readline()
            l = re.sub('[^A-Za-z0-9]','',l)
            
    wf.close()




def recompute(hashfile, hashtype):
    #spit out the known hashes so far
    print("python hashcrack.py -d dict\Top32Million-probable.txt -t "+hashtype+" -i "+hashfile+" -r rules\InsidePro-PasswordsPro.rule  --show  | perl get-passwords-from-pot.pl > "+hashfile+".tmp.pass")
    os.system("python hashcrack.py -d dict\Top32Million-probable.txt -t "+hashtype+" -i "+hashfile+" -r rules\InsidePro-PasswordsPro.rule  --show  | perl get-passwords-from-pot.pl > "+hashfile+".tmp.pass")

    #take those and generate some subsequences and stems
    print("Stemming passwords...")
    stem_file(hashfile+".tmp.pass")
    print("Subsequencing passwords...")
    subsq_file(hashfile+".tmp.pass")


# todo mix-in

hashfile="hashes.txt"
hashtype="1000"

#replay those at the remaining passwords with tweaks:
print("Cracking stage 1 - nsav2dive.rule")
print("python hashcrack.py --noinc -d "+hashfile+".tmp.pass.subs -t ntlm -i "+hashfile+" -r rules/nsav2dive.rule")
os.system("python hashcrack.py --noinc -d "+hashfile+".tmp.pass.subs -t ntlm -i "+hashfile+" -r rules/nsav2dive.rule")
recompute(hashfile, hashtype)

print("Cracking stage 2 - insertions.rule")
print("python hashcrack.py --noinc -d "+hashfile+".tmp.pass.subs -t ntlm -i "+hashfile+" -r rules/insertions.rule")
os.system("python hashcrack.py --noinc -d "+hashfile+".tmp.pass.subs -t ntlm -i "+hashfile+" -r rules/insertions.rule")
recompute(hashfile, hashtype)

print("Cracking stage 3 - leetspeak...")
print("python hashcrack.py --noinc -d "+hashfile+".tmp.pass.stem -t ntlm -i "+hashfile+" -3")
os.system("python hashcrack.py --noinc -d "+hashfile+".tmp.pass.stem -t ntlm -i "+hashfile+" -3")
recompute(hashfile, hashtype)

print("Cracking stage 4 - right mask...")
print("python hashcrack.py --noinc -d "+hashfile+".tmp.pass.stem -t ntlm -i "+hashfile+" --rmask ?a?a?a")
os.system("python hashcrack.py --noinc -d "+hashfile+".tmp.pass.stem -t ntlm -i "+hashfile+" --rmask ?a?a?a")
recompute(hashfile, hashtype)

print("Cracking stage 5 - purple rain...")
print("python hashcrack.py --noinc -d "+hashfile+".tmp.pass.subs -t ntlm -i "+hashfile+" -R")
os.system("python hashcrack.py --noinc -d "+hashfile+".tmp.pass.subs -t ntlm -i "+hashfile+" -R")
recompute(hashfile, hashtype)


