# Hashcat: Hacking together a modifed SHA GPU function in OpenCL - simple worked example 

Let's assume someone is silly enough to run SHA on 3 copies of the
password and use that as a hash function. (I have seen N times, I 
cannot say who did it.) We can do it in CPU using the fantastic 
mdxfind tool ( https://www.techsolvency.com/pub/bin/mdxfind/ ), but GPU
would be nice if we can.

There is also the chance to kludge it using rules - for the 3x we
could use one ruleset call dupedupe.rule containing 'dd\n' and add
this to our normal crack.

Initially we find the base function, SHA1, which happens to be module
100 if you look at the hashcat modes.

This comes with a c program for set up and then some opencl kernels
and some test code. We want to clone all this to module_00109.c in
which we'll do our implementation.

NB: if we looked at something like mode 21 (osCommerce, xt:Commerce),
it uses a type 20 kernel, as it's based on mode 20 kernel (
md5($salt.$pass) ). In our case, we create a new kernel as there's
nothing that matches closely enough. 

  ```
module_00021.c:static const u64   KERN_TYPE      = 20;
  ```

The module we want to copy and hack is 00100 :

C code is here: src/modules/module_00100.c and has test vectors as follows, where ST_HASH is sha1_hex("hashcat") 

```
static const char *ST_PASS        = "hashcat";
static const char *ST_HASH        = "b89eaac7e61417341b710b727768294d0e6a277b";
```

we need to change this to: 

```
static const char *ST_HASH        = "2747823a9a0e26ae6d4ea5df9a971a952798e4b6";
```

and to work out that out, we did:

```
jamie@determinist:~/hashcat$ perl test.pl
0311b4c0b1245c0f329149e443bf33b41a265156 == sha1('hashcathashcathashcat')
jamie@determinist:~/hashcat$ cat test.pl
#!/bin/perl

use Digest::SHA qw (sha1_hex);
use Digest::SHA qw (sha1);

print sha1_hex ( "hashcathaschathashcat" );
```

The opencl kernels are here: 

```
$ find . | grep m00100
./OpenCL/m00100_a1-pure.cl
./OpenCL/m00100_a0-pure.cl
./OpenCL/m00100_a3-optimized.cl
./OpenCL/m00100_a3-pure.cl
./OpenCL/m00100_a1-optimized.cl
./OpenCL/m00100_a0-optimized.cl
```

which correspond to the pure and optimized kernels for -a0 (dict+rules) -a1 (dict1 x dict2) and -a3 (mask)

The test suite is here:
./tools/test_modules/m00100.pm


Easiest one to do is test suite - we just need to iterate sha1_hex(),
so
  my $digest = sha1_hex ($word);
becomes
  my $digest = sha1_hex ( $word.$word.$word );

in the kernels, we need to find sha1_update_swap() and do a similar
loop - in between sha1_init() and sha1_final()

The optimized kernels get kind of scary, imagine someone unrolled some
assembler loops.

Let's clone as 109, that's not taken and is within the SHA1 grouping


remember to change 00100 -> 00109 throughout !

we also need to do 3 SHA1 updates with the candidate password:

```
jamie@determinist:~/hashcat$ diff OpenCL/m00109_a0-pure.cl OpenCL/m00100_a0-pure.cl
19c19
< KERNEL_FQ void m00109_mxx (KERN_ATTR_RULES ())
---
> KERNEL_FQ void m00100_mxx (KERN_ATTR_RULES ())
50,52d49
<     // 3 x
<     sha1_update_swap (&ctx, tmp.i, tmp.pw_len);
<     sha1_update_swap (&ctx, tmp.i, tmp.pw_len);
66c63
< KERNEL_FQ void m00109_sxx (KERN_ATTR_RULES ())
---
> KERNEL_FQ void m00100_sxx (KERN_ATTR_RULES ())
109,111d105
<     // 3 x
<     sha1_update_swap (&ctx, tmp.i, tmp.pw_len);
<     sha1_update_swap (&ctx, tmp.i, tmp.pw_len);
```

if you've messed up the kernel code, you might need to clear the
cache, if you want it to rebuild, like:

```
$ rm -f kernels/m00109_a0-pure.835be7e0.kernel
```

Again, remember to change 100 -> 109 throughout !
Change the name, change the mode number, change the test vector !

```
jamie@determinist:~/hashcat$ diff src/modules/module_00109.c  src/modules/module_00100.c
20,21c20,21
< static const char *HASH_NAME      = "SHA1x3";
< static const u64   KERN_TYPE      = 109;
---
> static const char *HASH_NAME      = "SHA1";
> static const u64   KERN_TYPE      = 100;
24a25
>                                   | OPTI_TYPE_NOT_ITERATED
33c34
< static const char *ST_HASH        = "2747823a9a0e26ae6d4ea5df9a971a952798e4b6";
---
> static const char *ST_HASH        = "b89eaac7e61417341b710b727768294d0e6a277b";
```

change the test code : 

```
jamie@determinist:~/hashcat$ diff tools/test_modules/m00109.pm tools/test_modules/m00100.pm
19c19
<   my $digest = sha1_hex ($word . $word . $word);
---
>   my $digest = sha1_hex ($word);
```

now compile

```
$ make
```

and invoke

```
jamie@determinist:~/hashcat$ ./hashcat -m 109 testsha1-cubed.txt crib.txt -a0
hashcat (v6.2.6-846-g4d412c8e0+) starting

...

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Optimizers applied:
* Zero-Byte
* Early-Skip
* Not-Salted
* Not-Iterated
* Single-Hash
* Single-Salt
* Raw-Hash

Watchdog: Temperature abort trigger set to 90c

Host memory required for this attack: 491 MB

Dictionary cache hit:
* Filename..: crib.txt
* Passwords.: 3
* Bytes.....: 22
* Keyspace..: 3

The wordlist or mask that you are using is too small.
This means that hashcat cannot use the full parallel power of your device(s).
Unless you supply more work, your cracking speed will drop.
For tips on supplying more work, see: https://hashcat.net/faq/morework

Approaching final keyspace - workload adjusted.

2747823a9a0e26ae6d4ea5df9a971a952798e4b6:hashcat
```

For opencl specifics, this is quite good: https://www.nersc.gov/assets/pubs_presos/MattsonTutorialSC14.pdf
