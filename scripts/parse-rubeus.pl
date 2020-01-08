#!/bin/perl

$acc=""; $col=0;

while ($line=<STDIN>) {

    chomp($line);

    if ($line=~m/Hash                   : ([^ ]+)/) {
        $acc=$1;
        $col=1;
    }
    else {
        if ($col==1) {
            if ($line=~m/([^ ]+)/) {
                $acc=$acc.$1;
            }
            else {
                print "$acc\n";

                $acc="";
                $col=0;
            }
        }
    }
}
