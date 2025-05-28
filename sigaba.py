# sigaba.py: v0.6 JF Bouchaudy 14/05/24

import sys

import RotorIndx
import Syslog as syslog
from RotorBiFace import *

ALPHA = string.ascii_uppercase
N = 26
CHIFFRES = "0123456789"


# ==================================
def litRot(rep, un_rot):
    f = open("ROTORS/" + f"{rep}/" + un_rot + ".rot")
    alpha = f.readline()
    f.readline()
    nom = un_rot
    f.close()
    return [nom.rstrip(), alpha.rstrip()]


# ==================================
def litRI(rep, un_rot):
    f = open("ROTORS/" + f"{rep}/" + un_rot + ".ri")
    alpha = f.readline()
    f.readline()
    nom = f.readline()
    f.close()
    return [nom.rstrip(), alpha.rstrip()]


# ==================================

class Sigaba:
    POWER_OFF = 0
    PLAIN = 1
    RESET = 2
    CHIFFRE = 3
    DECHIFFRE = 4
    MASTER_SWITCH = POWER_OFF
    OPERATE = 0
    ZEROIZE = 1
    RESET_SWITCH = OPERATE
    ROT_FAST = 7
    ROT_MIDDLE = 8
    ROT_SLOW = 6
    CSP_889 = 0
    CSP_2900 = 1
    MODEL = CSP_889
    NAME_MODEL = ["CSP-889", "CSP-2900"]
    NAME_MODE = ["POWER_OFF", "PLAIN", "RESET", "ENCRYPT", "DECRYPT"]
    NAME_RSTSW = ["OPERATE", "ZEROIZE"]
    INJECTION = {CSP_889: [5, 6, 7, 8], CSP_2900: [3, 4, 5, 6, 7, 8]}
    CTRL_INDX = {
        CSP_889: [9, 1, 2, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8],
        CSP_2900: [9, 1, 2, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 10, 10, 10, 7, 7, 0, 0, 8, 8, 8, 8]
    }
    AVC_DIRECT = {CSP_889: [1, 1, 1, 1, 1], CSP_2900: [1, -1, 1, -1, 1]}
    IDX_TO_AVC = [0, 4, 4, 3, 3, 2, 2, 1, 1, 0]
    BLANK = "!"

    def __init__(self, **kargs):
        self.Counter = 0
        self.RstSwitch = Sigaba.OPERATE
        self.Rotors = []
        self.DEBUG = False
        self.IDENT = "ECM"
        if 'debug' in kargs:
            self.DEBUG = kargs['debug']
            self.IDENT = kargs['ident']
        if 'verse' in kargs:
            verse = kargs['verse']
        else:
            verse = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if 'rep' in kargs:
            self.Rep = kargs['rep']
        else:
            self.Rep = "ECM"
        if 'intKey' in kargs:
            intKey = kargs['intKey']
        else:
            intKey = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
                      "10", "20", "30", "40", "50"]
        for i in range(10):
            [nom, alpha] = litRot(self.Rep, intKey[i])
            self.Rotors.append(
                RotorBiFace(
                    intKey[i],
                    alpha,
                    verse[i],
                    0
                )
            )
        self.RotorsIdx = []
        if 'verseIdx' in kargs:
            verseIdx = kargs['verseIdx']
        else:
            verseIdx = [0, 0, 0, 0, 0]
        for i in range(5):
            [nom, alpha] = litRI(self.Rep, intKey[i + 10])
            self.RotorsIdx.append(
                RotorIndx.RotorIndx(
                    intKey[i + 10],
                    alpha,
                    verseIdx[i],
                    0
                )
            )
        if 'mode' in kargs:
            self.Mode = kargs['mode']
        else:
            self.Mode = Sigaba.POWER_OFF
        if 'model' in kargs:
            self.Model = Sigaba.NAME_MODEL.index(kargs['model'])
        else:
            self.Model = Sigaba.CSP_889
        if self.DEBUG:
            syslog.openlog(ident=self.IDENT)
            syslog.syslog(syslog.LOG_INFO, "kargs:" + str(kargs))
            syslog.syslog(syslog.LOG_NOTICE, "Mode: " + self.NAME_MODE[self.Mode])
        if self.Mode == Sigaba.POWER_OFF:
            sys.exit(1)

    def info(self):
        if self.DEBUG:
            syslog.syslog(syslog.LOG_INFO, "Model: " + Sigaba.NAME_MODEL[self.Model])
            syslog.syslog(syslog.LOG_INFO, "Rotors set: " + self.Rep)
            syslog.syslog(syslog.LOG_INFO, "Mode: " + self.NAME_MODE[self.Mode])
            syslog.syslog(syslog.LOG_INFO, "Reset Mode: " + self.NAME_RSTSW[self.RstSwitch])
            for i in range(10):
                syslog.syslog(syslog.LOG_INFO, self.Rotors[i].info())
            for i in range(5):
                syslog.syslog(syslog.LOG_INFO, self.RotorsIdx[i].info())

    def mise_a_la_cle(self, cle):
        for i in range(10):
            x = ALPHA.index(cle[i].upper())
            self.Rotors[i].mise_a_la_cle(ALPHA[x])
        if self.DEBUG:
            syslog.syslog(syslog.LOG_NOTICE, "Key: " + self.obtient_cle() +
                          " " + self.obtient_cle_idx())

    def obtient_cle(self):
        cle = ""
        for i in range(10):
            cle += self.Rotors[i].obtient_cle()
            if i == 4: cle += ' '
        return cle

    def obtient_cle_idx(self):
        cle = ""
        for i in range(5):
            cle += self.RotorsIdx[i].obtient_cle()
        return cle

    def set_mode(self, new_mode):
        self.Mode = new_mode
        self.reset_counter()
        if self.DEBUG:
            syslog.syslog(syslog.LOG_NOTICE, "Master Switch: " + self.NAME_MODE[self.get_mode()])

    def get_mode(self):
        return self.Mode

    def set_rstsw(self, new_mode):
        self.RstSwitch = new_mode
        if self.DEBUG:
            syslog.syslog(syslog.LOG_NOTICE, "Reset Mode: " + self.NAME_RSTSW[self.ResetSwitch])

    def get_rstsw(self):
        return self.RstSwitch

    def mise_a_la_cle_idx(self, cle):
        for i in range(5):
            x = CHIFFRES.index(cle[i].upper())
            self.RotorsIdx[i].mise_a_la_cle(CHIFFRES[x])
        if self.DEBUG:
            syslog.syslog(syslog.LOG_INFO, "IKey: " + self.obtient_cle_idx())

    def avance(self):

        if self.DEBUG:
            syslog.syslog(syslog.LOG_INFO, "Advance start: " + self.obtient_cle())

        ctrl_rotors_output = [0] * N
        indx_rotors_input = [0] * 11
        indx_rotors_output = [0] * 10
        avc = [0] * 5

        # 1 - Injection du courant
        if self.DEBUG:
            syslog.syslog(syslog.LOG_DEBUG, "Current Injection")
        tb_injection = Sigaba.INJECTION[self.Model]
        ch = "".join(list(map(str, tb_injection)))
        ch += " "
        for x in tb_injection:
            ch += ALPHA[x]
        if self.DEBUG:
            syslog.syslog(syslog.LOG_DEBUG, f"Rotors ctrl input: {ch}")

        # 2 - Passage par les rotors de controle
        for x in tb_injection:
            x = self.dechiffre_un_car(x, mode="CTRL")
            ctrl_rotors_output[x] = 1
        ch = "".join(list(map(str, ctrl_rotors_output)))
        if self.DEBUG:
            syslog.syslog(syslog.LOG_DEBUG, f"Rotors ctrl output: {ch}")

        # 2 - des rotors de controles aux rotors d'index
        for i in range(N):
            if ctrl_rotors_output[i]:
                idx = Sigaba.CTRL_INDX[self.Model][i]
                indx_rotors_input[idx] = 1
        ch = "".join(list(map(str, indx_rotors_input)))
        if self.DEBUG:
            syslog.syslog(syslog.LOG_DEBUG, f"Rotors index input : {ch[0:10]}")

        # 3 - On passe par les rotors d'index 
        for i in range(10):
            if indx_rotors_input[i]:
                ch = ""
                x = i
                ch += CHIFFRES[x] + ">"
                for j in range(5):
                    x = self.RotorsIdx[j].chiffre(x)
                    ch += CHIFFRES[x]
                indx_rotors_output[x] = 1
                if self.DEBUG:
                    syslog.syslog(syslog.LOG_DEBUG, f"{ch}")
        ch = "".join(list(map(str, indx_rotors_output)))
        if self.DEBUG:
            syslog.syslog(syslog.LOG_DEBUG, f"Rotors index output: {ch}")

        # 3 - des rotors d'index au mecanisme d'avancement des
        #     rotors chiffrants
        for i in range(10):
            if indx_rotors_output[i]:
                idx = Sigaba.IDX_TO_AVC[i]
                avc[idx] = 1

        # 4 - avancement des rotors chiffrants
        for i in range(5):
            if avc[i] and (Sigaba.AVC_DIRECT[self.Model][i] == 1):
                self.Rotors[i].recule1()
            if avc[i] and (Sigaba.AVC_DIRECT[self.Model][i] == -1):
                self.Rotors[i].avance1()
        if self.DEBUG:
            syslog.syslog(syslog.LOG_DEBUG, "Advance cipher rotors: " + str(avc))

        # 5 - avancement des rotors de controle
        if self.DEBUG:
            syslog.syslog(syslog.LOG_DEBUG, "Advancement of control rotors")
        self.avance_ctrl()
        if self.DEBUG:
            syslog.syslog(syslog.LOG_NOTICE, "Key: " + self.obtient_cle() +
                          " " + self.obtient_cle_idx())

    def avance_ctrl(self):
        if self.get_mode() == self.RESET:
            if self.DEBUG:
                print ("Advance Control - RESET - not advancing")
            return
        if self.DEBUG:
            print("Advance Control - advancing")
        if self.Rotors[self.ROT_FAST].obtient_cle() == "O":
            if self.Rotors[self.ROT_MIDDLE].obtient_cle() == "O":
                self.Rotors[self.ROT_SLOW].recule1()
            self.Rotors[self.ROT_MIDDLE].recule1()
        self.Rotors[self.ROT_FAST].recule1()


    def code(self, car):
        if self.DEBUG:
            cpt = "%04d" % (self.get_counter())
            syslog.syslog(syslog.LOG_NOTICE, f"---> {cpt}: code <{car}>")
        if self.get_mode() == self.PLAIN:
            if car in ALPHA + CHIFFRES + " -":
                new_car = car
            else:
                new_car = ""
            return new_car
        elif self.get_mode() == self.RESET:
            if car == Sigaba.BLANK and self.RstSwitch == Sigaba.ZEROIZE:
                print("BLANK")
                cle = self.obtient_cle()
                cle = cle[:5] + cle[6:]
                for i in range(10):
                    if cle[i] == 'O': continue
                    self.Rotors[i].recule()
                return ""
            if car in "12345" and self.RstSwitch == Sigaba.OPERATE:
                print("RESET, car: ", car)
                self.Rotors[4 + int(car)].recule()
            new_car = ""
        elif self.get_mode() == self.CHIFFRE:
            if not (car in ALPHA + " "):
                return ""
            if car.upper() == "Z":
                car = "X"
            if car == " ":
                car = "Z"
            x = ALPHA.index(car.upper())
            x = self.chiffre_un_car(x)
            new_car = ALPHA[x]
            if ((self.Counter + 1) % 5) == 0:
                new_car += " "
        elif self.get_mode() == self.DECHIFFRE:
            if not (car in ALPHA):
                return ""
            x = ALPHA.index(car.upper())
            x = self.dechiffre_un_car(x)
            new_car = ALPHA[x]
            if new_car == "Z":
                new_car = " "
        elif self.get_mode() == self.POWER_OFF:
            return ""
        else:
            raise Exception
        self.avance()
        self.Counter += 1
        return new_car

    def chiffre_un_car(self, x, mode="ROT_CHIF"):
        if mode == "ROT_CHIF":
            rot_min = 0
            rot_max = 5
            ch = "Encrypt:"
        else:
            ch = ""
            rot_min = 5
            rot_max = 10
        ch += f"{ALPHA[x]}>"
        for i in range(rot_min, rot_max):
            x = self.Rotors[i].chiffre(x)
            ch += f"{ALPHA[x]}:"
        new_car = x
        ch += f">{ALPHA[new_car]}"
        if self.DEBUG:
            syslog.syslog(syslog.LOG_NOTICE, ch)
        return new_car

    def chiffre_un_car_ctrl(self, x):
        ch = ""
        for i in reversed(range(5, 10)):  # 9,8,7,6,5
            ch += f"{ALPHA[x]}:"
            x = self.Rotors[i].chiffre(x)
        new_car = x
        ch += f">{ALPHA[new_car]}"
        if self.DEBUG:
            syslog.syslog(syslog.LOG_DEBUG, ch)
        return new_car

    def dechiffre_un_car(self, x, mode="ROT_CHIF"):
        if mode == "ROT_CHIF":
            ch = "Decrypt:"
            rot_max = 4
        else:
            ch = ""
            rot_max = 9
        ch += f"{ALPHA[x]}>"
        for i in range(5):
            x = self.Rotors[rot_max - i].dechiffre(x)
            ch += f"{ALPHA[x]}:"
        new_car = x
        ch += f">{ALPHA[new_car]}"
        if self.DEBUG:
            if mode == "ROT_CHIF":
                syslog.syslog(syslog.LOG_NOTICE, ch)
            else:
                syslog.syslog(syslog.LOG_DEBUG, ch)
        return new_car

    def zeroise(self):
        self.mise_a_la_cle("OOOOOOOOOO")

    def indicator_navy(self, cle):
        old_mode = self.get_mode()
        self.set_mode(Sigaba.RESET)
        cle = list(cle)
        self.zeroise()
        for i in range(5):
            while True:
                self.Rotors[i + 5].recule1()
                self.avance()
                if self.obtient_cle()[i + 5 + 1] == cle[i]:
                    break
        self.set_mode(old_mode)

    def get_counter(self):
        return self.Counter

    def reset_counter(self):
        self.Counter = 0

    def __del__(self):
        self.set_mode(Sigaba.POWER_OFF)
        if self.DEBUG:
            syslog.syslog(syslog.LOG_NOTICE, "---- Stop Logging -----")


# ========================================================================
if __name__ == "__main__":
    h = Sigaba(
        rep="ECM",
        intKey=["00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
                "10", "20", "30", "40", "50"],
        verse=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        verseIdx=[0, 0, 0, 0, 0],
        mode=Sigaba.CHIFFRE,
        model="CSP-889",
        debug=True,
        ident="LOG",
    )
    h.info()
    h.mise_a_la_cle_idx("00000")
    h.mise_a_la_cle("ABAZAXXPPX")

    # --- chiffre le texte PLAIN
    CRYPTO = ""
    h.zeroise()
    PLAIN = sys.stdin.readline()
    print("===>", PLAIN)
    for car in PLAIN:
        lettre = h.code(car)
        if type(lettre) != str:
            continue
        CRYPTO += lettre
        print(lettre, end="")
    print()

    # --- dechiffre le texte CRYPTO
    h.zeroise()
    h.set_mode(Sigaba.DECHIFFRE)
    for car in CRYPTO:
        lettre = h.code(car)
        if type(lettre) != str:
            continue
        print(lettre, end="")
    print()

    # --- On utilise un autre repertoire et le mode inverse
    h = Sigaba(
        rep="MOE",
        intKey=["4", "1", "2", "3", "5", "0", "9", "7", "6", "8", "10", "20", "30", "40", "50"],
        verse=[0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
        verseIdx=[0, 0, 0, 0, 0],
        mode=Sigaba.CHIFFRE,
        debug=True,
        ident="RST",
    )
    h.indicator_navy("MERDE")
    for car in PLAIN:
        lettre = h.code(car)
        if type(lettre) != str:
            continue
        print(lettre, end="")
    print()
