#!/bin/python

# fugly, but we've all got SSDs and RAM cache, right?

import sys
import re

for line in sys.stdin:

    line=line.rstrip()
    
    with open("./regmap.cfg") as f:
        for cfgline in f:
            if cfgline[0]!='#':

                try:
                    (regexp, type, hr) = cfgline.split('!')

                    if re.search(regexp,line):
                        #output to file stdin.type
                        with open("separated-"+type+".txt", "a") as myfile:
                            myfile.write(line+"\n")
                            
                            print('type ' + type + ' - hash ' + line )
                except:
                    junk=0
                
