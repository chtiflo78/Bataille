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

import random
from tkinter import *
import math
from tkinter.messagebox import *

fenetre_jeu=Tk()

############################## Definition des classes #########################################       

class Carte:
    
    nom_couleur=["trefle","carreau","coeur","pique"]
    nom_valeur=["as","2","3","4","5","6","7","8","9","10","valet","dame","roi"]
    dos_carte=PhotoImage(file="Images_cartes/dos_carte.gif")

    def __init__ (self,parent,couleur,valeur):
        self.parent=parent
        self.couleur,self.valeur=couleur,valeur
        self.image=PhotoImage(file="Images_cartes/"+Carte.nom_valeur[self.valeur]+"_"+Carte.nom_couleur[self.couleur]+".gif")  ## ici on fait appel à un attribut hérité de la classe Carte, pas de l'instance => on écrit "Carte.nom_XX" et non pas "self.nom_XX"

    def affiche(self,x,y,sens):
        if sens:
            self.parent.create_image(x,y,anchor=NW,image=self.image)
        else:
            self.parent.create_image(x,y,anchor=NW,image=Carte.dos_carte)
 
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

class Paquet:

    def __init__ (self,parent,x,y):
        self.parent=parent
        self.x,self.y =x,y
        self.cartes=[]
        for i in range(4):
            for j in range (13):
                self.cartes.append(Carte(self.parent,i,j))
                self.cartes[j+13*i].affiche(self.x-(j+13*i)/2,self.y-(j+13*i)/2,False)
                
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

    def __init__ (self,parent,x,y):
        self.parent=parent
        self.x,self.y =x,y
        self.cartes=[]
        
    def afficher(self):
        for position in range(len(self.cartes)):
            self.cartes[position].affiche(self.x-position/2,self.y-position/2,False)
            self.parent.create_text(self.x+50,self.y-35, text=str(len(self.cartes)),font=("Arial","16"))

class Pot(Paquet):

    def __init__ (self,parent,x,y):
        self.parent=parent
        self.cartes=[]
        self.x,self.y =x,y

    def __lt__ (self,other):
        return self.cartes[-1]<other.cartes[-1]

    def __gt__ (self,other):
        return self.cartes[-1]>other.cartes[-1]

    def afficher(self):
        for position in range(len(self.cartes)):
            self.cartes[position].affiche(self.x-position/2,self.y-position*30, True)
       
############################## Boucle prinicpale ############################################

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

    tapis_jeu.delete("all")
    main_gauche.afficher()
    main_droite.afficher()
    pot_gauche.afficher()
    pot_droite.afficher()

def distribuer():

    position=0
    while len(paquet1.cartes)> 0:
        main_gauche.rajouter(paquet1.retirer())
        main_droite.rajouter(paquet1.retirer())
    bouton_distrib.config(state="disabled")
    bouton_jouer.config(state="active")
    afficher_jeu()

def ramasser():
    chaine=pot_gauche.cartes+pot_droite.cartes
    pot_gauche.cartes=[]
    pot_droite.cartes=[]
    return chaine
            
def jouer():
    
    if (len(main_gauche.cartes)+len(pot_gauche.cartes))<5 or (len(main_droite.cartes)+len(pot_droite.cartes))<5:
        tapis_jeu.create_text(440,100, text=" !!! FINI !!! ",font=("Arial","24"))
    else:
        pot_gauche.rajouter(main_gauche.retirer())
        pot_droite.rajouter(main_droite.retirer())
        afficher_jeu()
        
        if pot_gauche < pot_droite:
            tapis_jeu.create_text(540,475,text="Droite gagne",font=("Arial","18"))
            main_droite.cartes=ramasser()+main_droite.cartes
        else:
            if pot_gauche > pot_droite:
                tapis_jeu.create_text(335,475, text="Gauche Gagne",font=("Arial","18"))
                main_gauche.cartes=ramasser()+main_gauche.cartes
            else:
                tapis_jeu.create_text(440,475, text="!!! Bataille !!!",font=("Arial","18"))
                pot_gauche.rajouter(main_gauche.retirer())
                pot_droite.rajouter(main_droite.retirer())

def demarrer():
    if askyesno("Confirmation Nouvelle Partie","Nouvelle partie ?"):
        tapis_jeu.delete("all")

        global paquet1, main_gauche, main_droite, pot_gauche, pot_droite
        paquet1, main_gauche, main_droite, pot_gauche, pot_droite = Paquet(tapis_jeu,60,60), Main(tapis_jeu,100,275), Main(tapis_jeu,650,275), Pot(tapis_jeu,275,275), Pot(tapis_jeu,475,275)

        paquet1.melanger()
        bouton_distrib.config(state="active")
        bouton_jouer.config(state="disabled")

def quitter():
    if askyesno("Confirmation Quitter","Quitter ?"):
        fenetre_jeu.destroy() 

fenetre_jeu.title("  -- Jeu de bataille --  ")

menubar=Menu(fenetre_jeu)
menu= Menu(menubar,tearoff=0)
menu.add_command(label="Nouvelle partie",command=demarrer)
menu.add_separator()
menu.add_command(label="Quitter",command=quitter)
menubar.add_cascade(label="Menu", menu=menu)
fenetre_jeu.config(menu=menubar)

tapis_jeu=Canvas(width=900, height=500, bg="green")
tapis_jeu.pack(side=LEFT)

bouton_distrib=Button(fenetre_jeu, text="Distribuer",pady=10,command=distribuer)
bouton_distrib.pack()
bouton_distrib.config(state="disabled")
bouton_jouer=Button(fenetre_jeu, text="    Jouer    ",pady=10,command=jouer)
bouton_jouer.pack()
bouton_jouer.config(state="disabled")

fenetre_jeu.mainloop()



