We discovered a malicious backdoor in the project's dependencies, affected versions are a22aebcb7596ab0e2eafe6aa42810fd1d1a1b307~294e4c999c0600f5ecebf6f14ed8065b846fb45f. Its malicious backdoor is the request package, the requirements.txt file has a dependency request.

![image](https://user-images.githubusercontent.com/58363074/207070190-06b03b83-4acc-453a-b4a4-e4d58de2de46.png)

Even if the request has been deleted by PyPI, many mirror sites have not completely deleted this package, so it can still be installed. For example: https://mirrors.neusoft.edu.cn/pypi/web/simple/request/

Using such a mirror site to download and install this item will be vulnerable.

![image](https://user-images.githubusercontent.com/58363074/207070255-82664d11-0104-4cda-8e0d-5eb614e3879a.png)

Analysis of malicious function of request package: 1.Remote download of malicious code When the request package is installed, the setup.py file in the package will be actively executed. The setup.py file contains the logic for the attacker to remotely download and execute malicious code. At the same time, the C2 domain name is encoded and obfuscated. The decrypted C2 address is: https://dexy.top/request/check.so. 2.Release the remote control Trojan and persist it The malicious code loaded remotely during the installation of the request package includes two functions: Release the remote control Trojan to the .uds folder of the current user's HOME directory. The Trojan name is _err.log (for example, /root/.uds/_err.log). The content of the _err.log remote control Trojan script is encoded and compressed by base64, which reduces the size and enhances the confrontation. Implant malicious backdoor commands in .bashrc to achieve persistence 3.Issue stealing instructions The attacker issues python secret stealing instructions through the remote control Trojan to steal sensitive information (coinbase account secret) After decrypting the stealing instruction, the function is to request the C2 service: http://dexy.top/x.pyx, and remotely load the stealing Trojan. Some of the functions of the remotely loaded secret stealing Trojan are shown below, which are used to steal browser cookies, coinbase accounts and passwords, etc.

Repair suggestion: replace request in requirements.txt with requests