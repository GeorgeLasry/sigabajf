# RotorIndx.py:
# rotro d'index avec uniquement 

import string
import sys

CHIFFRES = "0123456789"
N = 10


# =====================================
class ROTORI:
    def __init__(self, alpha):
        self.Index = 0
        self.Decal = []
        self.Decal_inv = []
        PI = alpha
        self.Pi = PI
        for i in range(N):
            j = CHIFFRES.index(PI[i])
            self.Decal.append((j - i + N) % N)
        tampon = list(range(N))
        for i in range(N):
            j = CHIFFRES.index(PI[i])
            tampon[j] = i
        for i in range(N):
            self.Decal_inv.append((tampon[i] - i + N) % N)

    def chiffre(self, lettre):
        return (lettre + self.Decal[(lettre + self.Index) % N]) % N

    def chiffre_inv(self, lettre):
        return (lettre - self.Decal_inv[(self.Index - lettre) % N]) % N

    def dechiffre(self, lettre):
        return (lettre + self.Decal_inv[(lettre + self.Index) % N]) % N

    def dechiffre_inv(self, lettre):
        return (lettre - self.Decal[(self.Index - lettre) % N]) % N

    def avance(self):
        self.Index = (self.Index + 1) % N

    def recule(self):
        self.Index = (self.Index - 1 + N) % N

    def rewind(self):
        self.Index = 0


# ================================================
class RotorIndx(ROTORI):
    def __init__(self, name, alpha, verse=0, debug=0):
        ROTORI.__init__(self, alpha)
        self.name = name
        self.Verse = verse
        self.Debug = debug
        self.DontMove = False

    def info(self):
        return f"Rotor {self.name},{self.Verse},{self.Pi}"

    def obtient_cle(self):
        return CHIFFRES[self.Index]

    def mise_a_la_cle(self, r):
        self.rewind()
        indx_r = CHIFFRES.index(r.upper())
        for i in range(indx_r): self.avance()

    def chiffre(self, x):
        if self.Verse:
            x = ROTORI.chiffre_inv(self, x)
        else:
            x = ROTORI.chiffre(self, x)
        return x

    def dechiffre(self, x):
        if self.Verse:
            x = ROTORI.dechiffre_inv(self, x)
        else:
            x = ROTORI.dechiffre(self, x)
        return x

    # ========================================================================
