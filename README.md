# soapbox

Cracking passwords is pretty power-intensive; please consider moving to a low CO2 electricity provider, such as Ecotricity in the UK. Their customer service is also much better than most; check the OFGEM complaints data if you don't believe me. It only takes a couple of minutes, no affiliate link - https://www.ecotricity.co.uk/for-your-home 

# hashcrack

Do you want https://github.com/netmux/HASH-CRACK instead? I'm sorry about the name collision; I wasn't aware of it until after this project was released. 

This 'hashcrack' is a script which unpacks some hash types, picks sensible options and invokes hashcat.

email: jamie@blacktraffic.co.uk if you need support

I'm not sure if anyone at NCC will be looking after this, but I'll be doing active dev in this branch in future: https://github.com/blacktraffic/hashcrack

# python version

To install:

    pip3 install -r requirements.txt
    python3 setup.py

If you don't have Python in your path:

    <path to python>/python.exe -m pip install -r requirements.txt
    <path to python>/python.exe setup.py

for 7z files, you may need perl and Compress::Raw::LZMA, so maybe one of these two depending on your perl distribution: 

ActiveState Perl:
    ppm install Compress::Raw::LZMA

Strawberry Perl:
    cpan install Compress::Raw::LZMA

To run - various cases:

"Bog standard" crack:

    python3 hashcrack.py -i <input file>

or:

    python3 hashcrack.py --hash <literal hash>


Try harder - use words and phrases and previously found passwords 

    python3 hashcrack.py --input <input file> --words --phrases --found

Nuclear option - use bigger rules + dict + suffixes 

    python3 hashcrack.py --input <input file> --nuke

Try a bunch of dumb passwords:

    python3 hashcrack.py -i <input file> --crib dict/dumb.txt

Try a bunch of dumb passwords part 2:

    python3 hashcrack.py -i <input file> --mask default.hcmask

Try your own mask:

    python3 hashcrack.py -i <input file> --mask ?l?l?l?l?l?l

Run an IFM dump you've saved as a zip - requires impacket for decode

    python3 hashcrack.py -i <input file.zip> [-t ifm] 



See also test.bat / test.sh 

Input file may be a docx, pdf, JKS file, etc.


See also crackstation dictionaries - https://crackstation.net/


If you don't have Perl/Python/Java in your path, can set the correct paths in `hashcrack.cfg` - these are the paths to the executable files, rather than the directory the executable is in.




===

Thanks to https://github.com/berzerk0 for some wordlists - these are CC licensed. See:  https://github.com/berzerk0/Probable-Wordlists/tree/master/Real-Passwords

Other wordlists used are openwall_all.txt from Solar Designer, a crack of 275mil of Troy Hunt's hashes (mine), and breachcompilation.txt - origin unknown. (Have merged the last two.)

Includes https://www.7-zip.org/ code - which is LGPL. Thanks all! 

nsav2dive.rule is from here - thanks! https://github.com/NSAKEY/nsa-rules

License for nsav2dive.rule:

The Fair License

Copyright (c) 2015 _NSAKEY

Usage of the works is permitted provided that this instrument is retained with the works, so that any entity that uses the works is notified of this instrument.

DISCLAIMER: THE WORKS ARE WITHOUT WARRANTY.

Special thanks to CMIYK competition and hashes.org for test data.
