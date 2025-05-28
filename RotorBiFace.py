# RotorBiFace.py:
# pseudo machine a chiffrer fait d'un seul rotot
# Contrairement a Hebern1Rot il n'y a pas de Permutations Keyboard et Lamps
# mais on peut inverser le rotor
# question: mode chiffre/dechiff doit-il au niveau superieur ???
# NEW VERSION: 1.1 sans le bug du rotor VERSE!!! 06/07/19

import string

ALPHA = string.ascii_uppercase

# =====================================
class ROTOR:
    def __init__(self, alpha):
        self.Index = 0
        self.Decal = []
        self.Decal_inv = []
        PI = alpha
        self.Pi = PI
        for i in range(26):
            j = ALPHA.index( PI[i] )
            self.Decal.append( (j - i + 26) % 26 )
        tampon = list(range(26))
        for i in range(26):
            j = ALPHA.index( PI[i] )
            tampon[j] = i
        for i in range(26):
            self.Decal_inv.append( (tampon[i] - i + 26)%26 )


        
    def chiffre(self, lettre ):
        return (lettre + self.Decal[ (lettre + self.Index)%26 ])%26

    def chiffre_inv(self, lettre ):
        return (lettre - self.Decal_inv[ (self.Index - lettre)%26 ])%26

    def dechiffre(self, lettre ):
        return (lettre + self.Decal_inv[ (lettre + self.Index)%26 ])%26

    def dechiffre_inv(self, lettre ):
        return (lettre - self.Decal[ (self.Index - lettre)%26 ])%26

    def avance(self):
        self.Index = (self.Index + 1)%26

    def recule(self):
        self.Index = (self.Index - 1 + 26)%26

    def rewind(self):
        self.Index = 0

    def set(self, index):
        self.Index = index

# ================================================
class RotorBiFace( ROTOR ):
    def __init__(self, name, alpha, verse=0, debug=0):
        ROTOR.__init__(self, alpha )
        self.name  = name
        self.Verse = verse
        self.Debug = debug
        self.DontMove = False
        print ('Create: ', self.name, alpha, self.Decal)


    def info(self):
        return  f"Rotor {self.name},{str(self.Verse)},{self.Pi}"

    def obtient_cle( self ):
        return ALPHA[ self.Index ]

    def mise_a_la_cle(self, r ):
        self.set(ALPHA.index( r.upper()))

    def chiffre(self, x):
        if self.Verse:
            x = ROTOR.chiffre_inv( self, x )
        else:
            x = ROTOR.chiffre( self, x )
        return x
        
    def dechiffre(self, x):
        if self.Verse:
            x = ROTOR.dechiffre_inv( self, x )
        else:
            x = ROTOR.dechiffre( self, x )
        return x 

    def avance1(self):
        if self.Verse:
            ROTOR.recule( self )
        else:
            ROTOR.avance( self )

    def recule1(self):
        if not self.Verse:
            ROTOR.recule(self)
        else:
            ROTOR.avance(self)

#========================================================================

