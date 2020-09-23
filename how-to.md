# How to crack hashes 

Hashcrack is meant to have a go at doing the correct thing with your hashes without you having to think too hard about it.

The basic usage is:

    python hashcrack.py -i <input file> 

Though you can use explicit dict/rules:

    python hashcrack.py -i <input file> -r rules/best64.rule -d dict/leetest.dic

Or invoke other modes, such as -a1 :

    python hashcrack.py -i <input file> -d dict/left.dic -e dict/right.dic

Or invoke other modes, such as -a3 :

    python hashcrack.py -i <input file> --mask ?a?a?a?a?a?a [--noinc]

Or -a7 (try all 1 and 2 char suffixes against the given dictionary):

    python hashcrack.py -i <input file> -d dict/left.dic --rmask ?a?a

Or -a6 (try all 1 and 2 char prefixes against the given dictionary):

    python hashcrack.py -i <input file> -d dict/words.dic --lmask ?a?a


# Special Circumstances

There are a few bits and bobs that it will unpack for you, to save you the trouble - generally by invoking John the Ripper scripts, or sometimes using internal logic, and e.g. sqlite libraries. These are detailed below together with how to collect the hashes in an appropriate format.


## Responder 

Responder generates a Responder.db file which seems to have a mixture of NetNTLMv1 and v2 hashes. You can get it automatically unpacked and cracked like this:

    python hashcrack.py -i Responder.db


## NTLM from Active directory dumps: 

You can dump creds using ntdsutil, as explained here - https://www.cyberis.co.uk/2014/02/obtaining-ntdsdit-using-in-built.html

    C:\>ntdsutil
    ntdsutil: activate instance ntds
    ntdsutil: ifm
    ifm: create full c:\pentest
    ifm: quit
    ntdsutil: quit

And zip it up into "ifm.zip".

Then to crack, use this, which will run impacket to get the consituent bits out: 

    python hashcrack.py -i ifm.zip -t ifm

(If you omit "-t ifm", it will try to extract the zip password (for encrypted zips) and crack that. )

## NTLM from SAM, Security, System hives

     reg save HKLM\security security.reg
     reg save HKLM\security security.reg
     reg save HKLM\security system.reg

and again, zip it up into "sam.zip"

Then to crack, use this, which will run impacket to get the consituent bits out: 

     python hashcrack.py -i sam.zip -t reg


## Oracle: 

in sqlplus, as admin do: 

    SQL> set linesize 256
    SQL> set pagesize 1000
    SQL> select name||':'||spare4 from sys.user$ where spare4 is not null ;

    DAVE:S:1C92AD7D7F5EA0B094359B165A8E366176F218D3B9366ECBD81854C8D4A8;T:61B388254C0AE676E7782678BAB880ABA57C1E8F57B5295EDBB7F313429A4283A7917B81DA312832246532A6208E361C1F6B0E9FD9E6036A5861F594B318A210B09FF3C19EF29DD05B6E164500E9B2AE

put that in a file dave.txt and run the following, which should unpack it into dave.txt.tmp.112 (hashcatr type 112) and dave.txt.tmp.12300 for you, and have a pop at both.

    python3 hashcrack.py -i dave.txt -t oracle


