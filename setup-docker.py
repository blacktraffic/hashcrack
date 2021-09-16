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
    #check for file existence and download
    print("Installing configparser and other dependencies - needs 'pip3' on path")
    btexec("pip3 install -r requirements.txt")

    btexec('cp -rf rules/* hashcat-6.2.2/rules/')
    btexec('cp -rf hashcat-6.2.2/rules/* rules/')

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

    btexec("cd impacket ; python3 setup.py install") 

    print("Install done ...")

if __name__== "__main__":
  main()
  print("Ready!")
  btexec('/bin/bash')
  
