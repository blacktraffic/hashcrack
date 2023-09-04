#!/usr/bin/perl

$max=5;

@ringbuf=("");
$m=0;


while ( $line=<STDIN> ) {

    chomp($line);
    if ($line=~m/[a-z]+/) {

        $m++;
        push @ringbuf, $line;

        if ($m>$max) {

            #output our n-grams

            #print @g;
            for $g (1..$max) {

                $slice = join(' ', @ringbuf[ 1..$g ]) ;

                #print "$g $slice @ringbuf\n";
                print "$slice\n";
            }

            $j=shift @ringbuf;
            $m--;

        }

        #print "$line\n";
    }
}
