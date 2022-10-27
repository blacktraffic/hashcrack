#
#Released as open source by NCC Group Plc - http://www.nccgroup.com/
#
#Developed by Jamie Riden, jamie.riden@nccgroup.com
#
#http://www.github.com/nccgroup/hashcrack
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

    print("Installing impacket - needs 'pip3' on path. this will only affect Windows IFM formats if it's not installed.")
    btexec("pip3 install impacket==0.9.22")
       
    if not is_non_zero_file('hashcat-6.2.6.7z'):
        print("Got hashcat-6.2.6, expanding...")    
        urllib.request.urlretrieve("https://hashcat.net/files/hashcat-6.2.6.7z","hashcat-6.2.6.7z")
    btexec('7z x hashcat-6.2.6.7z')

    print("Getting JksPrivkPrepare.jar - for Java keystores")
    if not is_non_zero_file('JksPrivkPrepare.jar'):
        urllib.request.urlretrieve("https://github.com/floyd-fuh/JKS-private-key-cracker-hashcat/raw/master/JksPrivkPrepare.jar","JksPrivkPrepare.jar")

    print("Getting impacket-0.9.22 - might need to get a different one to match the pip install of impacket")
    if not is_non_zero_file('impacket_0_9_19.zip'):
        urllib.request.urlretrieve("https://github.com/CoreSecurity/impacket/archive/impacket_0_9_19.zip","impacket_0_9_19.zip")
        
    zip_ref = zipfile.ZipFile('impacket_0_9_19.zip', 'r')
    zip_ref.extractall('.')
    zip_ref.close()

    try:
        os.rename('impacket-impacket_0_9_19','impacket')
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


    if not is_non_zero_file('princeprocessor-0.22.7z'):
        urllib.request.urlretrieve("https://github.com/hashcat/princeprocessor/releases/download/v0.22/princeprocessor-0.22.7z")
        btexec('7z x princeprocessor-0.22.7z')
    try:        
        os.rename('princeprocessor-0.22','princeprocessor')
    except:
        print("Couldn't rename princeprocessor - assuming already exists")

        
    shutil.copy2('rules/leet2.rule','hashcat-6.2.6/rules/')
    shutil.copy2('rules/allcase.rule','hashcat-6.2.6/rules/')
    shutil.copy2('rules/nsav2dive.rule','hashcat-6.2.6/rules/')
    shutil.copy2('rules/l33tpasspro.rule','hashcat-6.2.6/rules/')
    
    print("Done - now change the paths in hashcrack.cfg to point to dict, rules, hashcat")        

if __name__== "__main__":
  main()
