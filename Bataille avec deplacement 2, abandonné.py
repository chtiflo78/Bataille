#############################################################################################
##
## Jeu bataille
##
## Florent Spriet, Mars 2020
##
## Ce qui est intéressant:
## - Une classe (Paquet ou Main/Pot) d'objets (Carte), héritage de Main/Pot depuis Paquet
## - La manipulation des listes d'objet
## - Des classes standards avec des métodes standard qui peuvent facilement être réutilisées
## 
#############################################################################################

## faire calcul de distance mieux foutu
## finir le déplacement des cartes
## retablir la gestion du sens des cartes
## voir si il y a moyen de faire une fonction déplacer plus esthétique


import random
from tkinter import *
import math

fenetre_jeu=Tk()

############################## Définition des Classes #########################################

class Carte:
    
    nom_couleur=["trefle","carreau","coeur","pique"]
    nom_valeur=["as","2","3","4","5","6","7","8","9","10","valet","dame","roi"]
    dos_carte=PhotoImage(file="Images_cartes/dos_carte.gif")

   
    def __init__ (self,can,couleur,valeur,x,y,sens):

        self.can=can
        self.couleur,self.valeur=couleur,valeur
        self.x,self.y =x,y
        self.sens=sens
        self.image=PhotoImage(file="Images_cartes/"+Carte.nom_valeur[self.valeur]+"_"+Carte.nom_couleur[self.couleur]+".gif")  ## ici on fait appel à un attribut hérité de la classe Carte, pas de l'instance => on écrit "Carte.nom_XX" et non pas "self.nom_XX"

        self.affiche()

    def affiche(self):
        if self.sens:
            self.objet=self.can.create_image(self.x,self.y,anchor=NW,image=self.image)
        else:
            self.objet=self.can.create_image(self.x,self.y,anchor=NW,image=Carte.dos_carte)
        self.can.update()
 
##    def __str__ (self):
##        return Carte.nom_valeur[self.valeur]+" de "+Carte.nom_couleur[self.couleur]+"  "

    def deplace(self,dest_x,dest_y,sens):   ## sens est le sens final

        dist=math.sqrt((dest_x-self.x)**2+(dest_y-self.y)**2)
        pente_x,pente_y=(dest_x-self.x)/dist,(dest_y-self.y)/dist
        for position in range(0,int(dist),20):
            self.can.coords(self.objet,self.x+pente_x*position,self.y+pente_y*position)
            self.can.update()
        self.x,self.y=dest_x,dest_y
        self.sens=sens
        self.can.coords(self.objet,self.x,self.y)
        self.can.delete(self.objet)
        self.affiche()
        
    def __lt__ (self,other):

        a=self.valeur
        b=other.valeur
        if a==0: a=13
        if b==0: b=13
        return a<b

    def __gt__ (self,other):

        a=self.valeur
        b=other.valeur
        if a==0: a=13
        if b==0: b=13
        return a>other.valeur

class Paquet:

    def __init__ (self,can,x,y):
        self.can=can
        self.x,self.y =x,y
        self.cartes=[]
        for i in range(4):
            for j in range (13):
                self.cartes.append(Carte(self.can,i,j,self.x-(j+13*i)/2,self.y-(j+13*i)/2,True))

##    def __str__ (self):
##        chaine=""
##        for position in range(len(self.cartes)-1,-1,-1):
##           chaine=chaine+str(position)+" "+str(self.cartes[position])+"\n"
##        return chaine

    def melanger (self):
        random.shuffle(self.cartes)
    
    def rajouter(self,carte_ajoutee):
        self.cartes.append(carte_ajoutee)

    def retirer(self):
        carte_retiree = self.cartes.pop()
        return carte_retiree

class Main(Paquet):      ## hérite de la classe Paquet

    def __init__ (self,can,x,y):
        self.can=can
        self.x,self.y =x,y
        self.cartes=[]
        
    def afficher(self):
        for position in range(len(self.cartes)):
            self.cartes[position].afficher (self.x-position/2,self.y-position/2, False)
            self.can.create_text(self.x+50,self.y-35, text=str(len(main_gauche.cartes)+len(pot_gauche.cartes)),font=("Arial","16"))

class Pot(Paquet):

    def __init__ (self,x,y):
        self.cartes=[]
        self.x,self.y =x,y

    def __lt__ (self,other):
        return self.cartes[-1]<other.cartes[-1]

    def __gt__ (self,other):
        return self.cartes[-1]>other.cartes[-1]

    def afficher(self
                 ):
        for position in range(len(self.cartes)):
            self.cartes[position].afficher (self.x-position/2,self.y-position*30, True)

############################## Fonctions du jeu ###########################################


def raz():

    global paquet1, main_gauche, main_droite, pot_gauche, pot_droite
    
    paquet1, main_gauche, main_droite, pot_gauche, pot_droite = Paquet(tapis_jeu,60,60), Main(tapis_jeu,100,275), Main(tapis_jeu,650,275), Pot(275,275), Pot(475,275)
    
    paquet1.melanger()
    bouton_distrib.config(state="active")
    bouton_jouer.config(state="disabled")

def afficher_jeu():

##    print("----------")
##    print("Main Gauche")
##    print(main_gauche)
##    print("Main Droite")
##    print(main_droite)
##    print("----------")
##    print("Pot Gauche")
##    print(pot_gauche)
##    print("Pot Droite")
##    print(pot_droite)    
    pass
    
def distribuer():

    position=0
    while len(paquet1.cartes)> 0:
        passage=paquet1.retirer()
        passage.deplace(main_gauche.x-position/2,main_gauche.y-position/2,False)
        main_gauche.rajouter(passage)
        passage=paquet1.retirer()
        passage.deplace(main_droite.x-position/2,main_droite.y-position/2,False)
        main_droite.rajouter(passage)
        position=position+1
    bouton_distrib.config(state="disabled")
    bouton_jouer.config(state="active")

def ramasser():
    position=0
    while len(pot_gauche.cartes)>0:
        pot_gauche.cartes[position].deplace(300,100,True)
        position=position+1
    chaine=pot_gauche.cartes+pot_droite.cartes
    pot_gauche.cartes=[]
    pot_droite.cartes=[]
    return chaine
            
def jouer():
    
    if (len(main_gauche.cartes)+len(pot_gauche.cartes))<5 or (len(main_droite.cartes)+len(pot_droite.cartes))<5:
        tapis_jeu.create_text(440,100, text=" !!! FINI !!! ",font=("Arial","24"))
    else:
        passage=main_gauche.retirer()
        passage.deplace(pot_gauche.x,pot_gauche.y,True)
        pot_gauche.rajouter(passage)
        passage=main_droite.retirer()
        passage.deplace(pot_droite.x,pot_droite.y,True)
        pot_droite.rajouter(passage)    
               
        if pot_gauche < pot_droite:
            tapis_jeu.create_text(540,475,text="Droite gagne",font=("Arial","18"))
            main_droite.cartes=ramasser()+main_droite.cartes
            tapis_jeu.update()
        else:
            if pot_gauche > pot_droite:
                tapis_jeu.create_text(335,475, text="Gauche Gagne",font=("Arial","18"))
                main_gauche.cartes=ramasser()+main_gauche.cartes
            else:
                tapis_jeu.create_text(440,475, text="!!! Bataille !!!",font=("Arial","18"))
                pot_gauche.rajouter(main_gauche.retirer())
                pot_droite.rajouter(main_droite.retirer())
       
############################## Boucle principale ############################################

fenetre_jeu.title("  -- Jeu de bataille --  ")

tapis_jeu=Canvas(width=900, height=500, bg="green")
tapis_jeu.pack(side=LEFT)

Button(fenetre_jeu, text="  Quitter  ", command=fenetre_jeu.destroy).pack(side=BOTTOM)
bouton_raz=Button(fenetre_jeu, text="     RAZ     ",pady=10,command=raz).pack()
bouton_distrib=Button(fenetre_jeu, text="Distribuer",pady=10,command=distribuer)
bouton_distrib.pack()
bouton_distrib.config(state="disabled")
bouton_jouer=Button(fenetre_jeu, text="    Jouer    ",pady=10,command=jouer)
bouton_jouer.pack()
bouton_jouer.config(state="disabled")

fenetre_jeu.mainloop()



