# sigaba_tui.py 
# version 0.1 1er avril 2024

import getopt
import re

from sigaba import *

ALPHA = string.ascii_uppercase
CHIFFRES = "0123456789"


# ==================================
def usage():
    print("Usage:")
    print("Syntax: sigaba_tui.py [option...]")
    print("Example: ")
    print(" echo AAAAAAAAAAAAAAAA | python sigaba_tui.py \\")
    print("   -m CSP-889  \\")
    print("   -s ECM \\")
    print("   -I 00R:01:02:03:04R=05:06:07R:08:09=10:20:30:40:50 \\")
    print("   -E ABCDE:FGHIJ:01234 \\")
    print("   -c")
    print(" [Expected: JTSCA LXDRW OQKRX]")
    print(" -h             Help")
    print(" -D prefix      DEBUG, if prefix equal LOG, use STDOUT")
    print(" -m model       CSP-889 by default (it exists also the CSP-2900 model)")
    print(" -s set         The set of rotors (ECM by default)")
    print(" -I internal    Internal Key, by default:")
    print("                00:01:02:03:04=05:06:07:08:09=10:20:30:40:50")
    print("                If the rotor is in Reverse position, it is followed by 'R'")
    print("                Example:  00:01R:02:03R:....")
    print("                Separators: <space>, <,>, =, -, :")
    print(" -E external    External Key, OOOOO:OOOOO:00000 by default")
    print(" -N external    External Key but using Navy Indicator method, ex: -N MERDE")
    print(" -c/-d          The mode: Cipher/Decipher, by default: Power off")
    print(" [Note: order (I,E options): cipher rotors, ctrl rotors, index rotors]")


# ================================================
try:
    opts, args = getopt.getopt(sys.argv[1:],
                               "hD:m:s:I:E:N:cd", ["help", "debug=", "model=", "set=", "internal=",
                                                   "external=", "navy=", "cipher", "decipher", ])
except getopt.GetoptError as err:
    print(sys.argv[0], ": ", str(err))
    usage()
    sys.exit(2)
INTERNAL = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "20", "30", "40", "50"]
VERSE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
EXTERNAL = "OOOOOOOOOO00000"
MODE = Sigaba.POWER_OFF
MODEL = "CSP-889"
REP = "ECM"
DEBUG = False
IDENT = "LOG"
FLAG_EXT_KEY = False
FLAG_NAVY = False
EXTERN_NAVY = ""

for o, a in opts:
    print (o, a)
    if o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o in ("-D", "--debug"):
        DEBUG = True
        IDENT = a
    elif o in ("-m", "--model"):
        if a == "CSP-2900":
            MODEL = "CSP-2900"
    elif o in ("-s", "--set"):
        REP = a
    elif o in ("-I", "--internal"):
        a = (re.compile(r'[ :,=-]+')).sub(':', a)
        a = a.split(":")
        for i in range(15):
            if a[i][-1:] == "R":
                VERSE[i] = 1
                a[i] = a[i][:-1]
        INTERNAL = a
    elif o in ("-E", "--external="):
        if FLAG_EXT_KEY:
            assert False, "You must choose -E or -N"
        a = a.replace(":", "")
        a = a.replace("=", "")
        EXTERNAL = a.replace(" ", "")
    elif o in ("-N", "--navy="):
        if FLAG_EXT_KEY:
            assert False, "You must choose -E or -N"
        EXTERN_NAVY = a
        FLAG_NAVY = True
    elif o in ("-c", "--cipher"):
        MODE = Sigaba.CHIFFRE
    elif o in ("-d", "--decipher"):
        MODE = Sigaba.DECHIFFRE
    else:
        assert False, "unhandled option"

# ================================================
leTexte = "KWITNMCXSUVWIHTYIHPUZLBPZSVBSQXJRTLOMLZGVGLHJZRNTMKIBAYVZWEIOVUXUPVUIWLVNIVALETCZPTQFBGXJEVBFQKDZXKVNSIUUZLAECTHLDGJXSZCDWXKMYWSQKHSWKNNSANUNTSRACGRKIREWHQHDAGRTQNNBMKCDQBMHYZDJACOUBDFNCJPMJDNTOOTOHDNVODSHOWXLXEZPPVJWZVHEXXRHXZJWCPASBZHDIWJCPISIBDTHPMYXWMIBAYHKLONTBGKZAIYXGIXFRQICFLZSANMAVPOCCZEFKOKPMEPEPOYGDBRAPITACEX"
clair = ""
n = 0
for i in range(len(leTexte)):
    ch = leTexte[i]
    ch = ch.upper()
    for j in range(len(ch)):
        car = ch[j]
        clair += car
h = Sigaba(
    debug=DEBUG,
    ident=IDENT,
    rep=REP,
    model=MODEL,
    mode=MODE,
    intKey=INTERNAL,
    verse=VERSE[:10],
    verseIdx=VERSE[10:],
)
h.info()
h.mise_a_la_cle_idx(EXTERNAL[10:])
if FLAG_NAVY:
    h.indicator_navy(EXTERN_NAVY)
else:
    h.mise_a_la_cle(EXTERNAL[:10])
for car in clair:
    if not (car in ALPHA + CHIFFRES + " -"):
        continue
    crypto = h.code(car)
    if type(crypto) == None:
        continue
    print(crypto, end="")
print()
