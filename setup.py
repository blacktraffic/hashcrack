#
#Released as open source by NCC Group Plc - http://www.nccgroup.com/
#
#Originally developed by Jamie Riden at NCC
# 
#Now maintained as separate branch, jamie@blacktraffic.co.uk 
#
#http://www.github.com/blacktraffic/hashcrack
#
#This software is licensed under AGPL v3 - see LICENSE.txt
#

import os
import urllib.request
import zipfile
import shutil

def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

def btexec( sexec ):
    print('RUN: '+sexec) 
    os.system(sexec)
    
def main():
    btexec('mkdir dict')
    #check for file existence and download
    print("Installing configparser and other dependencies - needs 'pip3' on path")
    btexec("pip3 install -r requirements.txt")

    if not is_non_zero_file('hashcat-6.1.1.7z'):
        print("Got hashcat-6.1.1, expanding...")    
        urllib.request.urlretrieve("https://hashcat.net/files/hashcat-6.1.1.7z","hashcat-6.1.1.7z")
        btexec('7z x hashcat-6.1.1.7z')

    print("Getting JksPrivkPrepare.jar - for Java keystores")
    if not is_non_zero_file('JksPrivkPrepare.jar'):
        urllib.request.urlretrieve("https://github.com/floyd-fuh/JKS-private-key-cracker-hashcat/raw/master/JksPrivkPrepare.jar","JksPrivkPrepare.jar")

    print("Getting impacket-0.9.22 - might need to get a different one to match the pip install of impacket")
    if not is_non_zero_file('impacket_0_9_22.zip'):
        urllib.request.urlretrieve("https://github.com/CoreSecurity/impacket/archive/impacket_0_9_22.zip","impacket_0_9_22.zip")
        
    zip_ref = zipfile.ZipFile('impacket_0_9_22.zip', 'r')
    zip_ref.extractall('.')
    zip_ref.close()

    try:
        os.rename('impacket-impacket_0_9_22','impacket')
    except:
        print("Couldn't rename impacket - assuming already exists")

    if not is_non_zero_file('bleeding-jumbo.zip'):
        urllib.request.urlretrieve("https://github.com/magnumripper/JohnTheRipper/archive/bleeding-jumbo.zip","bleeding-jumbo.zip")
        
    zip_ref = zipfile.ZipFile('bleeding-jumbo.zip', 'r')
    zip_ref.extractall('.')
    zip_ref.close()

    try:        
        os.rename('JohnTheRipper-bleeding-jumbo','john')
    except:
        print("Couldn't rename john - assuming already exists")
        
    shutil.copy2('rules/leet2.rule','hashcat-6.1.1/rules/')
    shutil.copy2('rules/allcase.rule','hashcat-6.1.1/rules/')
    shutil.copy2('rules/nsav2dive.rule','hashcat-6.1.1/rules/')
    shutil.copy2('rules/l33tpasspro.rule','hashcat-6.1.1/rules/')
    
    print("Done - now change the paths in hashcrack.cfg to point to dict, rules, hashcat")        

if __name__== "__main__":
  main()
