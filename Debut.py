import random

class Carte:
    
    nom_couleur=["trefle","carreau","coeur","pique"]
    nom_valeur=["as","2","3","4","5","6","7","8","9","10","valet","dame","roi"]

    def __init__ (self, couleur, valeur):
        self.couleur=couleur
        self.valeur=valeur
        self.visible=False

    def __str__ (self):
        return Carte.nom_valeur[self.valeur]+" de "+Carte.nom_couleur[self.couleur]
        ## ici on fait appel à un attribut hérité de la classe Carte, pas de l'instance => on écrit "Carte.nom_XX" et non pas "self.nom_XX"

class Paquet:

    def __init__ (self):
        self.cartes=[]
        for i in range(4):
            for j in range (13):
                self.cartes.append(Carte(i,j))

    def __str__ (self):
        chaine=""
        for position in range(len(self.cartes)):
            chaine=chaine+str(self.cartes[position])+"\n"
        return chaine

    def melanger (self):
        random.shuffle(self.cartes)


paquet1=Paquet()
print(paquet1)
paquet1.melanger()
print(paquet1)




