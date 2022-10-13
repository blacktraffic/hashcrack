#!/bin/perl

# ugly partition for running full descrypt jobs so we can stop and restart, or parallelize 

# test vector is 48c/R8JAv757A
    
$leadin="./hashcat -O -w4 -a3 -m 1500 tests/descrypt.txt ";

print "#cover the <8 char case\n";
print $leadin." -i ?a?a?a?a?a?a?a\n";


print "#cover all the 8 char chases, bit by bit\n";

$i=48;
while ($i<58) { 
    print $leadin.chr($i)."?a?a?a?a?a?a?a\n";
    $i++;
}
$i=65;
while ($i<=90) { 
    print $leadin.chr($i)."?a?a?a?a?a?a?a\n";
    $i++;
}
$i=97;
while ($i<123) { 
    print $leadin.chr($i)."?a?a?a?a?a?a?a\n";
    $i++;
}
    
    
print $leadin."?s?a?a?a?a?a?a?a\n"; 
