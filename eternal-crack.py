#!/usr/bin/python

import sys
import os
import re
import argparse

def subsq(state, remains, n, wf):

    #don't do more than this many tweaks
    if n>5:
        if len(state+remains)>6:
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


def stem_file(filename,pattern="[^A-Za-z0-9]"):

    wf = open(filename+".stem","w")
    
    with open(filename,'r', encoding="utf-8") as inpfile:
        l = inpfile.readline()

        while l:
            l = re.sub(pattern,'',l)

            if isinstance(l, str):
                wf.write(l+"\n")
                
            l = inpfile.readline()
            l = re.sub(pattern,'',l)
            
    wf.close()

def bt_exec(command):
    print("EXEC: "+command)
    os.system(command)

def recompute(hashfile, hashtype):
    #spit out the known hashes so far
    print("python hashcrack.py -t "+hashtype+" -i "+hashfile+" -r rules\InsidePro-PasswordsPro.rule  --show  | perl get-passwords-from-pot.pl > "+hashfile+".tmp.pass")
    bt_exec("python hashcrack.py -t "+hashtype+" -i "+hashfile+" -r rules\InsidePro-PasswordsPro.rule  --show  | perl get-passwords-from-pot.pl > "+hashfile+".tmp.pass")

    #take those and generate some subsequences and stems
    print("Stemming passwords...")
    stem_file(hashfile+".tmp.pass")
    print("Subsequencing passwords...")
    subsq_file(hashfile+".tmp.pass")


# todo mix-in

hashtype="1000"

parser = argparse.ArgumentParser(description='Helps to crack passwords')
parser.add_argument('-i','--input', help='Input file' )
parser.add_argument('-m','--mix', help='Mix-in file' )
parser.add_argument('-n','--number', help='Number of iterations' )
parser.add_argument('-t','--type', help='Hash type (defaults to ntlm/1000)')
args = parser.parse_args()

if not args.input:
    die("Please specify [--input|-i] <input file> ")
    
hashfile=args.input

#replay those at the remaining passwords with tweaks:

iterations=1 
if args.number and args.number>1:
    iterations=args.number

if args.mix:
    mix=os.path.abspath(args.mix)
    print("Cracking stage - mixin crib...")
    bt_exec("python hashcrack.py --noinc -c "+mix+" -t ntlm -i "+hashfile+" -3")

    print("Cracking stage - mixin purple rain (leetspeak)...")
    bt_exec("python hashcrack.py --noinc -d "+mix+" -t ntlm -i "+hashfile+" -3")

    print("Cracking stage - mixin purple rain (random rules plus prince)...")
    bt_exec("python hashcrack.py --noinc -d "+mix+" -t ntlm -i "+hashfile+" -R")
    recompute(hashfile, hashtype)

for x in range(iterations):

    recompute(hashfile, hashtype)

    print("Cracking stage - insertions.rule / subs")
    bt_exec("python hashcrack.py --noinc -d "+hashfile+".tmp.pass.subs -t ntlm -i "+hashfile+" -r rules/insertions.rule")
    recompute(hashfile, hashtype)

    #todo add rules
    print("Cracking stage - leetspeak / stem...")
    bt_exec("python hashcrack.py --noinc -d "+hashfile+".tmp.pass.stem -t ntlm -i "+hashfile+" -3 -r rules/nsav2dive.rule")
    recompute(hashfile, hashtype)

    print("Cracking stage - right mask / subs ...")
    bt_exec("python hashcrack.py --noinc -d "+hashfile+".tmp.pass.subs -t ntlm -i "+hashfile+" --rmask ?a?a?a")
    recompute(hashfile, hashtype)

    print("Cracking stage - left mask / subs ...")
    bt_exec("python hashcrack.py --noinc -d "+hashfile+".tmp.pass.subs -t ntlm -i "+hashfile+" --lmask ?a?a")
    recompute(hashfile, hashtype)

    print("Cracking stage - purple rain (random rules plus prince) / subs ...")
    bt_exec("python hashcrack.py --noinc -d "+hashfile+".tmp.pass.subs -t ntlm -i "+hashfile+" -R")
    recompute(hashfile, hashtype)


