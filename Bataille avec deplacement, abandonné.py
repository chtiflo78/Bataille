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


## A faire:
## - passer le canvas en argument dans les objets (voir l'autre exemple 2
## - représenter le déplacement des cartes (ne plus effacer le canevas à chaque fois)

import random
from tkinter import *
import time

fenetre_jeu=Tk()

############################## Définition des Classes #########################################

class Carte:
    
    nom_couleur=["trefle","carreau","coeur","pique"]
    nom_valeur=["as","2","3","4","5","6","7","8","9","10","valet","dame","roi"]
    dos_carte=PhotoImage(file="Images_cartes/dos_carte.gif")
    
    def __init__ (self,can,couleur,valeur,x,y,sens):  ## si sens=False, on affiche le dos de la carte
        
        self.can=can
        self.couleur=couleur
        self.valeur=valeur

        self.image=PhotoImage(file="Images_cartes/"+Carte.nom_valeur[self.valeur]+"_"+Carte.nom_couleur[self.couleur]+".gif")   ## ici on fait appel à un attribut hérité de la classe Carte, pas de l'instance => on écrit "Carte.nom_XX" et non pas "self.nom_XX"

        if sens:
            self.objet=self.can.create_image(x,y,anchor=NW,image=self.image)
        else:
            self.objet=self.can.create_image(x,y,anchor=NW,image=Carte.dos_carte)

##    def __str__ (self):
##        return Carte.nom_valeur[self.valeur]+" de "+Carte.nom_couleur[self.couleur]+"  "

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
        
    def afficher (self,x,y,sens):
        if sens:
            self.objet=self.can.create_image(x,y,anchor=NW,image=self.image)
        else:
            self.objet=self.can.create_image(x,y,anchor=NW,image=Carte.dos_carte)

    def deplacer(self,x2,y2,sens):

        self.origine_x,self.origine_y= self.can.coords(self.objet)
        self.destination_x,self.destination_y= x2,y2
        self.dx,self.dy =1,(self.destination_y-self.origine_y)/(self.destination_x-self.origine_x)
        
        def pas_a_pas():
            self.origine_x,self.origine_y= self.origine_x+self.dx,self.origine_y+self.dy
            self.can.coords(self.objet,self.origine_x,self.origine_y)
            if self.origine_x>self.destination_x:
                self.can.coords(self.objet,self.destination_x,self.destination_y)
                return
            self.can.after(1,pas_a_pas)

        pas_a_pas()

class Paquet:

    def __init__ (self,can):

        self.cartes=[]
        self.can=can
        for i in range(4):
            for j in range (13):
                position=i*13+j
                self.cartes.append(Carte(self.can,i,j,60-position/2,60-position/2,True))
        
##    def __str__ (self):
##        chaine=""
##        for position in range(len(self.cartes)-1,-1,-1):
##           chaine=chaine+str(position)+" "+str(self.cartes[position])+"\n"
##        return chaine

    def melanger (self):
        random.shuffle(self.cartes)
    
    def rajouter (self, carte_ajoutee):
        self.cartes.append(carte_ajoutee)

    def retirer (self):
        carte_retiree = self.cartes.pop()
        return carte_retiree
    
class Main(Paquet):      ## hérite de la classe Paquet

    def __init__ (self,can):
        self.cartes=[]
        self.can=can

    def afficher(self,x,y):
        for position in range(len(self.cartes)):
            self.cartes[position].afficher (x-position/2,y-position/2, False)
        self.can.create_text(150,125, text=str(len(main_gauche.cartes)+len(pot_gauche.cartes)),font=("Arial","16"))
        self.can.create_text(700,125, text=str(len(main_droite.cartes)+len(pot_droite.cartes)),font=("Arial","16"))

class Pot(Paquet):

    def __init__ (self):
        self.cartes=[]

    def __lt__ (self,other):
        return self.cartes[-1]<other.cartes[-1]

    def __gt__ (self,other):
        return self.cartes[-1]>other.cartes[-1]

    def afficher(self,x,y):
        for position in range(len(self.cartes)):
            self.cartes[position].afficher (x-position/2,y-position*30, True)

############################## Fonctions du jeu ###########################################

def melanger():

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

    
##    can1.delete("all")
##    can1.pack()

    main_gauche.afficher(100,175)
    main_droite.afficher(650,175)
    pot_gauche.afficher(275,175)
    pot_droite.afficher(475,175)
    can1.pack()
    bouton_distrib.config(state="disabled")
    bouton_jouer.config(state="active")

    
def distribuer():

    while len(paquet1.cartes)> 0:
        main_gauche.rajouter(paquet1.retirer())
        main_droite.rajouter(paquet1.retirer())
    afficher_jeu()

def ramasser():
    chaine=pot_gauche.cartes+pot_droite.cartes
    pot_gauche.cartes=[]
    pot_droite.cartes=[]
    return chaine
            
def jouer():
    
    if (len(main_gauche.cartes)+len(pot_gauche.cartes))<5 or (len(main_droite.cartes)+len(pot_droite.cartes))<5:
        can1.create_text(440,100, text=" !!! FINI !!! ",font=("Arial","24"))
    else:
        transfert=main_gauche.retirer()
        pot_gauche.rajouter(transfert)
        transfert.deplacer(400,400,True)
        pot_droite.rajouter(main_droite.retirer())

        afficher_jeu()                
               
        if pot_gauche < pot_droite:
            can1.create_text(540,375,text="Droite gagne",font=("Arial","18"))
            main_droite.cartes=ramasser()+main_droite.cartes
        else:
            if pot_gauche > pot_droite:
                can1.create_text(335,375, text="Gauche Gagne",font=("Arial","18"))
                main_gauche.cartes=ramasser()+main_gauche.cartes
            else:
                can1.create_text(440,375, text="!!! Bataille !!!",font=("Arial","18"))
                pot_gauche.rajouter(main_gauche.retirer())
                pot_droite.rajouter(main_droite.retirer())
       
############################## Boucle principale ############################################

fenetre_jeu.title("  -- Jeu de bataille --  ")

tapis_jeu=Canvas(width=900, height=400, bg="green")
tapis_jeu.pack(side=LEFT)
    
paquet1, main_gauche, main_droite, pot_gauche, pot_droite = Paquet(tapis_jeu), Main(tapis_jeu), Main(tapis_jeu), Pot(), Pot()

Button(fenetre_jeu, text="  Quitter  ", command=fenetre_jeu.quit).pack(side=BOTTOM)
bouton_raz=Button(fenetre_jeu, text=" Mélanger ",pady=10,command=melanger).pack()
bouton_distrib=Button(fenetre_jeu, text="Distribuer",pady=10,command=distribuer)
bouton_distrib.pack()
bouton_distrib.config(state="disabled")
bouton_jouer=Button(fenetre_jeu, text="    Jouer    ",pady=10,command=jouer)
bouton_jouer.pack()
bouton_jouer.config(state="disabled")

fenetre_jeu.mainloop()



