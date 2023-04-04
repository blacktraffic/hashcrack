import sys
import re

with open(sys.argv[1]) as inf:
    for line in inf:
        pw = line.split(':')[-1]
        pw = pw.rstrip()

        #convert any HEX strings
        m = re.search('\$HEX\[(.+)\]',pw)
        
        if m is not None:
            pw=bytes.fromhex( m.group(1)).decode("iso-8859-1") 

        print(pw)
        
                
