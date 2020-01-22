#!/bin/perl

$i=0;
$m=2**14;

while ($i<$m) {

    $j=0;

    while ($j<14) {
	$b=2**$j;
	
	
	
	if ($i & $b) {
	    printf "T%1X",$j;
	}
	$j++;
    }

    print "\n";
    
    $i++;    
}
