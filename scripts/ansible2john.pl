#!/usr/bin/perl

# algorithm taken from JTR ansible2john.py but I needed to parse entire YML files

while ($line=<STDIN>) {

    chomp($line);

    if ($line=~m/\$ANSIBLE_VAULT/) { $on=1;}

    if ($on==1) {
        $line=~s/[ \t]//g;
    }

    if ($line!~m/[a-zA-Z0-9]/) {

        ($hdr,$hash)=split(m/\n/,$file,2);
        ($hdr,$version,$cipher)=split(m/;/,$hdr);

        if ($cipher=~m/AES256/) {

            $hash=~s/[^A-Za-z0-9]//g;

            $bins=pack('H*',$hash);

            ($salt,$check,$ct)=split(m/\n/,$bins,3);

            if ($check ne "") {
                printf('$ansible$%d*%d*%s*%s*%s'."\n",0, $cipher, $salt, $ct, $check );
            }
        }
        $on=0;
        $file="";
    }

    if ($on==1) {
        $file.=$line."\n";
    }
}
