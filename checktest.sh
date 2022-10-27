#!/bin/bash

# should work with activestate or cygwin perl hopefully 

python3 hashcrack.py -i tests/postgres.txt --show | grep :hashcat
if [ $? == '0' ] ; then
echo "PostgreSQL passed"
else echo "PostgreSQL - FAILED"
fi

# autodetect - answer is "foo"
python3 hashcrack.py --hash 0beec7b5ea3f0fdbc95d0dd47f3c5bc275da8a33 --show | grep :foo
if [ $? == '0' ] ; then
echo "SHA1 passed"
else echo "SHA1 - FAILED"
fi

python3 hashcrack.py --hash 2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae --show | grep :foo
if [ $? == '0' ] ; then
echo "SHA256 passed"
else echo "SHA256 - FAILED"
fi

python3 hashcrack.py --hash f7fbba6e0636f890e56fbbf3283e524c6fa3204ae298382d624741d0dc6638326e282c41be5e4254d8820772c5518a2c5a8c0c7f7eda19594a7eb539453e1ed7 --show | grep :foo
if [ $? == '0' ] ; then
echo "SHA512 passed"
else echo "SHA512 - FAILED"
fi

python3 hashcrack.py -i tests/dollar1.txt --show | grep :foo
if [ $? == '0' ] ; then
echo "md5crypt passed"
else echo "md5crypt - FAILED"
fi

python3 hashcrack.py --hash tests/apachemd5.txt --show | grep :foo
if [ $? == '0' ] ; then
echo "Apache MD5 passed"
else echo "Apache MD5 - FAILED"
fi

# ifm

python3 hashcrack.py -i /home/jamie/dev/hashcrack/tests/ifm.zip.tmp.pwdump --show | grep Password1
if [ $? == '0' ] ; then
echo "IFM passed"
else echo "IFM - FAILED"
fi

# autodetect - answer is "cisco"
python3 hashcrack.py --hash 2KFQnbNIdI.2KYOU --show | grep :cisco
if [ $? == '0' ] ; then
echo "2400 (Cisco) passed"
else echo "2400 (Cisco) - FAILED"
fi

python3 hashcrack.py --hash '{ssha1}06$bJbkFGJAB30L2e23$dCESGOsP7jaIIAJ1QAcmaGeG.kr'

# autodetect - hashcat example hashes where the answer is "hashcat"
python3 hashcrack.py -i tests/sha256crypt.txt --show | grep hashcat
if [ $? == '0' ] ; then
echo "sha256crypt passed"
else echo "sha256crypt - FAILED"
fi

python3 hashcrack.py -i tests/sha512crypt.txt --show | grep hashcat
if [ $? == '0' ] ; then
echo "sha512crypt passed"
else echo "sha512crypt - FAILED"
fi

#autodetect PDF
python3 hashcrack.py -i tests/test-hashcat.pdf --show | grep hashcat
if [ $? == '0' ] ; then
echo "10500 (PDF) passed"
else echo "10500 (PDF) - FAILED"
fi


#autodetect Word
python3 hashcrack.py -i tests/test-abc.docx

# manual type selection - hashcat example hashes where the answer is "hashcat"

# oracle 7
python3 hashcrack.py --hash "7A963A529D2E3229:3682427524" -t 3100

# oracle 11
python3 hashcrack.py --hash "ac5f1e62d21fd0529428b84d42e8955b04966703:38445748184477378130" -t 112

# oracle 12+
python3 hashcrack.py --hash "78281A9C0CF626BD05EFC4F41B515B61D6C4D95A250CD4A605CA0EF97168D670EBCB5673B6F5A2FB9CC4E0C0101E659C0C4E3B9B3BEDA846CD15508E88685A2334141655046766111066420254008225" -t 12300

#mssql 2000
python3 hashcrack.py --hash "0x01002702560500000000000000000000000000000000000000008db43dd9b1972a636ad0c7d4b8c515cb8ce46578" -t 131

#mssql 2005
python3 hashcrack.py --hash "0x010018102152f8f28c8499d8ef263c53f8be369d799f931b2fbe" -t 132

python3 hashcrack.py --hash "u4-netntlm::kNS:338d08f8e26de93300000000000000000000000000000000:9526fb8c23a90751cdd619b6cea564742e1e4bf33006ba41:cb8086049ec4736c" -t 5500

python3 hashcrack.py --hash "admin::N46iSNekpT:08ca45b7d7ea58ee:88dcbe4446168966a153a0064958dac6:5c7830315c7830310000000000000b45c67103d07d7b95acd12ffa11230e0000000052920b85f78d013c31cdb3b92f5d765c783030" -t 5600

python3 hashcrack.py --hash "b7c2d6f13a43dce2e44ad120a9cd8a13d0ca23f0414275c0bbe1070d2d1299b1c04da0f1a0f1e4e2537300263a2200000000000000000000140768617368636174:472bdabe2d5d4bffd6add7b3ba79a291d104a9ef" -t 7300

python3 hashcrack.py -i tests/sha3.txt -t sha3

python3 hashcrack.py -i tests/ripe.txt -t ripemd
