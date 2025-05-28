JF'S SIGABA SIMULATOR MANUAL
============================

DESCRIPTION
-----------
I created a simulator of the Siagaba cipher machine. It works in text mode (TUI interface). It is written in Python and only uses the standard library. Consequently, it works on any platform on which the Python 3.x interpreter is installed (Windows, Linux, Mac-OS-X, etc.).

Installation
------------
My simulator is in the form of a TARBALL: a compressed TAR file. Just download it from my website and then untar it.

Example :
C:\> wget http://www.jfbouch.fr/crypto/sigaba/sigabajf.tar
C:\> tar xf sigabajf.tar

After decompression, we obtain a file tree which starts at the sigabajf directory.

Show syntax
-----------
Just use the -h option to display the syntax.
We start by moving to the root directory of the software.

C:\> cd sigabajf
C:\sigabajf> dir  
[.]               [..]              [LOGS]            [MSGS]     RotorBiFace.py
RotorIndx.py      [ROTORS]          sigaba.py         sigaba_tui.py     syslog.py

C:\sigabajf> python sigaba_tui.py -h
Usage:
Syntax: sigaba_tui.py [option...]
Example:
 echo AAAAAAAAAAAAAAAA | python sigaba_tui.py \
   -m CSP-889  \
   -s ECM \
   -I 00R:01:02:03:04R=05:06:07R:08:09=10:20:30:40:50 \
   -E ABCDE:FGHIJ:01234 \
   -c
 [Expected: JTSCA LXDRW OQKRX]
 -h             Help
 -D prefix      DEBUG, if prefix equal LOG, use STDOUT
 -m model       CSP-889 by default (it exists also the CSP-2900
                model)
 -s set         The set of rotors (ECM by default)
 -I internal    Internal Key, by default:
                00:01:02:03:04=05:06:07:08:09=10:20:30:40:50
                If the rotor is in Reverse position, it is
                followed by 'R'
                Example:  00:01R:02:03R:....
 -E external    External Key, OOOOO:OOOOO:00000 by default
 -N external    External Key but using Navy Indicator method, 
                ex: -N MERDE
 -c/-d          The mode: Cipher/Decipher, by default: Power off

Note: If you activate the program without option, it reads standard input. We must interrupt it with Ctrl-C or terminate standard input (via Ctrl-D on Unix or Ctrl-Z on Windows).

A simple example
----------------
To encrypt text, use the “-c” option. Plain text is read from standard input. For example, we want to encrypt the text HELLOWORLD.

C:\sigabajf> echo HELLOWORLD | python sigaba_tui.py -c
FLQGF ONNOE O

C:\sigabajf> echo HELLOWORLD > MSGS\plain.txt
C:\sigabajf> more MSGS\plain.txt
HELLOWORLD

C:\sigabajf> python sigaba_tui.py -c   < MSGS\plain.txt
FLQGF ONNOE O

Note: The Microsoft Windows system adds a space, which here is coded by the letter O. There is no additional character under Unix.

To decrypt a text, we use the “-d” option.

C:\sigabajf> echo FLQGF ONNOE O |python sigaba_tui.py -d
HELLOWORLD

Here are the default values used in the previous examples:

Model: CSP-889
Rotors set: ECM
Mode: ENCRYPT
Reset Mode: OPERATE
Rotor 00,0,YCHLQSUGBDIXNZKERPVJTAWFOM
Rotor 01,0,INPXBWETGUYSAOCHVLDMQKZJFR
Rotor 02,0,WNDRIOZPTAXHFJYQBMSVEKUCGL
Rotor 03,0,TZGHOBKRVUXLQDMPNFWCJYEIAS
Rotor 04,0,YWTAHRQJVLCEXUNGBIPZMSDFOK
Rotor 05,0,QSLRBTEKOGAICFWYVMHJNXZUDP
Rotor 06,0,CHJDQIGNBSAKVTUOXFWLEPRMZY
Rotor 07,0,CDFAJXTIMNBEQHSUGRYLWZKVPO
Rotor 08,0,XHFESZDNRBCGKQIJLTVMUOYAPW
Rotor 09,0,EZJQXMOGYTCSFRIUPVNADLHWBK
Rotor 10,0,7591482630
Rotor 20,0,3810592764
Rotor 30,0,4086153297
Rotor 40,0,3980526174
Rotor 50,0,6497135280
Key: OOOOO OOOOO 00000

The example given when displaying the syntax
--------------------------------------------

C:\sigabajf>  echo AAAAAAAAAAAAAAA | python sigaba_tui.py -m CSP-889 -s ECM -I 00R:01:02:03:04R=05:06:07R:08:09=10:20:30:40:50 -E ABCDE:FGHIJ:01234 -c
JTSCA LXDRW OQKRX

Here is the corresponding configuration:
- Model: CSP-889
- Set: ECM

Note: In fact, the set of rotors corresponds concretely to a directory (ROTORS\ECM) which contains files with the extension *.rot for encryption and control rotors or the *.ri extension for Index rotors.
Example :
C:\sigabajf> more ROTORS\ECM\00.rot
YCHLQSUGBDIXNZKERPVJTAWFOM

Alpha wheel 0
C:\sigabajf> more ROTORS\ECM\10.ri
7591482630

Rotor Index 10

- Rotors:
 - The encryption rotors (left to right). The letter R following the name of a rotor indicates it is in reverse mode: 
00R 01 02 03 04R
 - Control rotors (left to right): 05 06 07R 08 09
 - Index rotors: 10 20 30 40 50

- Key:
Initial positions:
 - For encryption rotors (from left to right): A B C D E
 - For control rotors (left to right): F G H I J
 - For index rotors: 0 1 2 3 4
Note: With a graphical simulator, this corresponds to 10 21 32 43 54 initial positions.

- Mode: encryption


Debugging
---------
It is possible to obtain debugging information using the “-D” option followed by a word. If this word is "LOG", the Debugging information will be visible on the screen. If this is not the case, a log file is created in the LOGS directory and whose prefix corresponds to the word following option D.

WARNING! The log is very detailed. It can only be used if very few letters (1,2 or 3) are encrypted (or deciphered), otherwise the log becomes enormous.

here is an example
- Model: CSP-2900
- Set: ECM
- Rotors:
    Cipher: 08R 02 05R 09 01
    Control: 07 00R 04 03 06R
    Index: 30R 10 50R 40 20
-Key:
    Cipher Rotors: M E R D E
    Control rotors: S H I T S
    Index rotors: 0 1 7 8 9
- Mode: Encryption

C:\sigabajf> echo THE ZEBRE | python sigaba_tui.py -m CSP-2900 -s ECM -I 08R:02:05R:09:01=07:00R:04:03:06R=30R:10:50R:40:20 -E MERDE:SHITS:01789 -c -D MRD
ZTABW AULD

C:\sigabajf> echo ZTABW AULD | python sigaba_tui.py -m CSP-2900 -s ECM -I 08R:02:05R:09:01=07:00R:04:03:06R=30R:10:50R:40:20 -E MERDE:SHITS:01789 -d -D MRD2
THE XEBRE

Here is the start of the log file:

DEBUG 7 4351  ---Starting Logging----
INFO 6 4484  kargs:{'debug': True, 'ident': 'MRD', 'rep': 'ECM', 'model': 'CSP-2900', 'mode
': 3, 'intKey': ['08', '02', '05', '09', '01', '07', '00', '04', '03', '06', '30', '10', '5
0', '40', '20'], 'verse': [1, 0, 1, 0, 0, 0, 1, 0, 0, 1], 'verseIdx': [1, 0, 1, 0, 0]}
NOTICE 5 4518  Mode: ENCRYPT
INFO 6 4555  Model: CSP-2900
INFO 6 4584  Rotors set: ECM
INFO 6 4612  Mode: ENCRYPT
INFO 6 4639  Reset Mode: OPERATE
INFO 6 4676  Rotor 08,1,XHFESZDNRBCGKQIJLTVMUOYAPW
INFO 6 4707  Rotor 02,0,WNDRIOZPTAXHFJYQBMSVEKUCGL
INFO 6 4738  Rotor 05,1,QSLRBTEKOGAICFWYVMHJNXZUDP
INFO 6 4768  Rotor 09,0,EZJQXMOGYTCSFRIUPVNADLHWBK
INFO 6 4797  Rotor 01,0,INPXBWETGUYSAOCHVLDMQKZJFR
INFO 6 4827  Rotor 07,0,CDFAJXTIMNBEQHSUGRYLWZKVPO
INFO 6 4865  Rotor 00,1,YCHLQSUGBDIXNZKERPVJTAWFOM
INFO 6 4896  Rotor 04,0,YWTAHRQJVLCEXUNGBIPZMSDFOK
INFO 6 4925  Rotor 03,0,TZGHOBKRVUXLQDMPNFWCJYEIAS
INFO 6 4955  Rotor 06,1,CHJDQIGNBSAKVTUOXFWLEPRMZY
INFO 6 4989  Rotor 30,1,4086153297
INFO 6 5018  Rotor 10,0,7591482630
INFO 6 5047  Rotor 50,1,6497135280
INFO 6 5075  Rotor 40,0,3980526174
INFO 6 5104  Rotor 20,0,3810592764
INFO 6 5240  IKey: 01789
INFO 6 5570  Key: MERDE SHITS 01789
INFO 6 5607  ---> code <T>
DEBUG 7 5685  Encrypt:T>V:H:K:O:Z:>Z
DEBUG 7 5722  Current Injection
DEBUG 7 5769  Rotors ctrl input: 345678 DEFGHI
DEBUG 7 5843  D>E:R:L:L:J:>J
DEBUG 7 5904  E>Y:O:T:X:G:>G
DEBUG 7 5963  F>Z:G:Q:S:E:>E
DEBUG 7 6021  G>X:T:I:V:R:>R
DEBUG 7 6078  H>I:M:F:A:W:>W
DEBUG 7 6137  I>S:S:V:U:Q:>Q
DEBUG 7 6196  Rotors ctrl output: 00001010010000001100001000
DEBUG 7 6251  Rotors index input : 0001110010
DEBUG 7 6308  3>18529
DEBUG 7 6359  4>72160
DEBUG 7 6408  5>51741
DEBUG 7 6479  8>33673
DEBUG 7 6520  Rotors index output: 1101000001
DEBUG 7 6579  Advance cipher rotors: [1, 0, 0, 1, 1]
DEBUG 7 6606  Advancement of control rotors
INFO 6 6677  Key: NERED SHHTS 01789
INFO 6 6724  ---> code <H>
DEBUG 7 6791  Encrypt:H>C:V:D:C:T:>T
DEBUG 7 6825  Current Injection
DEBUG 7 6868  Rotors ctrl input: 345678 DEFGHI
DEBUG 7 6926  D>E:R:T:X:G:>G
DEBUG 7 6984  E>Y:O:B:N:K:>K
DEBUG 7 7042  F>Z:G:H:J:S:>S
DEBUG 7 7099  G>X:T:W:K:I:>I
DEBUG 7 7157  H>I:M:V:U:Q:>Q
DEBUG 7 7214  I>S:S:M:H:D:>D
DEBUG 7 7265  Rotors ctrl output: 00010010101000001010000000
DEBUG 7 7318  Rotors index input : 0001110100
DEBUG 7 7371  3>18529
DEBUG 7 7421  4>72160
DEBUG 7 7485  5>51741
DEBUG 7 7538  7>47888
DEBUG 7 7577  Rotors index output: 1100000011
DEBUG 7 7633  Advance cipher rotors: [1, 1, 0, 0, 1]
DEBUG 7 7660  Advancement of control rotors
INFO 6 7729  Key: OFREC SHGTS 01789
INFO 6 7771  ---> code <E>
DEBUG 7 7838  Encrypt:E>C:K:Z:M:A:>A
DEBUG 7 7871  Current Injection
DEBUG 7 7912  Rotors ctrl input: 345678 DEFGHI
DEBUG 7 7970  D>E:R:G:F:N:>N
DEBUG 7 8028  E>Y:O:H:J:S:>S
DEBUG 7 8086  F>Z:G:O:Y:U:>U
DEBUG 7 8144  G>X:T:N:O:Y:>Y
DEBUG 7 8200  H>I:M:P:M:T:>T
DEBUG 7 8258  I>S:S:U:I:L:>L
DEBUG 7 8309  Rotors ctrl output: 00000000000101000011100010
DEBUG 7 8363  Rotors index input : 1000001110
DEBUG 7 8416  0>96314
DEBUG 7 8481  6>04256
DEBUG 7 8533  7>47888
DEBUG 7 8583  8>33673
DEBUG 7 8623  Rotors index output: 0001101010
DEBUG 7 8678  Advance cipher rotors: [0, 1, 1, 1, 0]
DEBUG 7 8705  Advancement of control rotors
INFO 6 8774  Key: OGSFC SHFTS 01789

Remarks :
1) For each encrypted (or decrypted) letter, the log displays the encryption details:
INFO 6 5607  ---> code <T>
DEBUG 7 5685  Encrypt:T>V:H:K:O:Z:>Z

The letter is encrypted as Z. The output of the first rotor gives the letter V. The output of the second rotor gives H, etc...

2) Then, we have the detail of the advancement of the encryption rotors mainly due to the control rotors.

2.1. We have the injection of electric current into the control rotors and the resulting currents output from the control rotors:

DEBUG 7 7912  Rotors ctrl input: 345678 DEFGHI
DEBUG 7 5843  D>E:R:L:L:J:>J
DEBUG 7 5904  E>Y:O:T:X:G:>G
DEBUG 7 5963  F>Z:G:Q:S:E:>E
DEBUG 7 6021  G>X:T:I:V:R:>R
DEBUG 7 6078  H>I:M:F:A:W:>W
DEBUG 7 6137  I>S:S:V:U:Q:>Q
DEBUG 7 6196  Rotors ctrl output: 00001010010000001100001000

Thus, the current generated at the input at the letter D comes out at the letter J, etc...

In the end, we have 6 cables which are electrified: 00001010010000001100001000
If we translate this table into letters:....E.G..J......QR....W...

2.2. At the input of the control rotors, we only have 10 entries, only four cables are electrified: 0001110010

DEBUG 7 6251  Rotors index input : 0001110010

2.3 At the output of the index rotors, we have: 1101000001

DEBUG 7 6308  3>18529
DEBUG 7 6359  4>72160
DEBUG 7 6408  5>51741
DEBUG 7 6479  8>33673
DEBUG 7 6520  Rotors index output: 1101000001

2.4. We deduce the encryption rotors which will move: 
[1, 0, 0, 1, 1]
That is to say, the first and the last two.
The key (for crypto rotors) changes from SHIT to NERED. The first rotor goes from M to N, the second and third do not move (they remain at ER), the fourth goes from D to E and the last rotor goes from E to D. Due to the fact that the machine used is a CSP -2900, the second and fourth rotors move forward instead of backward. But when a rotor is reversed, it moves forward.

DEBUG 7 6579  Advance cipher rotors: [1, 0, 0, 1, 1]
DEBUG 7 6606  Advancement of control rotors
INFO 6 6677  Key: NERED SHHTS 01789

2.5 The control rotors advance regularly: We go from SHIFTS to SHHTS. Index rotors do not move.



