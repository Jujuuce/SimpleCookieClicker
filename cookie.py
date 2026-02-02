import tkinter as tk
from math import *
import random


root = tk.Tk()
root.title("Cookie")

l = 700 # La taille est modifiable, tous les paramètres sont proportionnels
(Hauteur,Largeur) = (l,l) # C'est plus simple si c'est un carré
Dessin=tk.Canvas(root,height=Hauteur,width=Largeur,bg="lavender")
Dessin.pack()


# J'aurai aimé que les gains (+) et les pertes (-) lorsque l'on clique soient un peu mieux fait mais je ne sais pas comment faire
# Le score bloque lorsqu'il dépasse 10^306, il faudrait régler ça
# J'aurai aimé que tictac() et donc que l'affichage s'actualise toutes les 10 ms, mais comme j'ai beaucoup de calcul, ça fait lag et le temps n'est pas juste
# Le cookie est vraiment moche


# Quelques variables pour simplifier

(c,k) = (l/4,l/1.5) # coordonées du cookie
delta = l/10
t = ((l/1.8)+(l-l/5.5))/2 # coordonnée de l'abscisse du texte des bonus
f1=f"LinuxLibertine {int(l/47)} bold"
f2=f"LinuxLibertine {int(l/23)} bold"
f3=f"LinuxLibertine {int(l/70)} bold"


# Les fonctions utilisées:

def disque(x,y,r,c):
    p = (x+r,y+r)
    q = (x-r,y-r)
    Dessin.create_oval(p,q,fill=c)
    
def rectangle(a,b,c):
    (xa,ya) = a
    (xb,yb) = b
    Dessin.create_rectangle(xa,ya,xb,yb,fill=c)

def texte2(x,y,t,f,c): # Fonction vu en cours pour ajouter du texte
    Dessin.create_text((x,y),text=t,font=f,fill=c)
    
def simplification(e): # Fonction pratique lorsque les nombres sont trop grands et difficiles à afficher, 1000000 devient 10.00 x 10^5
    if e > 1000000:
        f = 1
        d = float(e)
        b = float(e)
        while True:
            d = b/(10**f)
            if d > 100:
                f = f + 1
            else:
                d = format(d, '.2f')
                d = f"{d} x 10^{f}"
                return d
    else:
        return e

def minuterie(e): # Fonction pour voir le temps qui s'est écoulé à la fin
    h = 0
    m = 0
    s = e
    if s >= 1600:
        h = s // 1600
        s = s - h*1600
    if s >= 60:
        m = s // 60
        s = s - m*60
    if s > 1:
        rs = f"{s} secondes"
    else:
        rs = f"{s} seconde"
    if m > 1:
        rm = f"{m} minutes"
    else:
        rm = f"{m} minute"
    if h > 1:
        rh = f"{h} heures"
    else:
        rh = f"{h} heure"
    res = f"{rh} {rm} et {rs}"
    return res


def dessin_cookie(L):
    # Dessiner le cookie
    disque(c, k, l/5,'chocolate')
    # Placer les pépites de chocolat
    for e in L:
        (x,y) = e
        disque(x,y,l/50,'saddlebrown')


class État():
    def __init__(self): # Initialisation des variables qui vont changer
        self.score=0
        self.time=0
        self.bonus1=1
        self.coût1=10
        self.bonus2=0
        self.coût2=100
        self.bonus3=0
        self.coût3=1000
        self.coût4=10000
        self.pepites = []
        for i in range(30): # Détermine aléatoirement les coordonées des pépites, elles sont réinitialisées lorsqu'on fait une nouvelle partie
            x = random.randint(int(c-l/7), int(c+l/7))
            y = random.randint(int(k-l/7), int(k+l/7))
            self.pepites.append((x, y))
        self.stop = True # Option qui permet d'arreter le jeu et voir le score
        self.affichage()
    
        
    def affichage(self):
        Dessin.delete('all')
        dessin_cookie(self.pepites)
        for i in range(4,9): # Les rectangles pour les bonus
            rectangle((l/1.8,delta*i),(l-l/5.5,delta*i+delta),'white')
    
        rectangle((delta,delta),(l-delta,3*delta),'white') # Le rectangle du score
        # Texte du premier bonus (+1 per click)
        texte2(t,4.3*delta,"+1 par click",f1,'black')
        texte2(t,4.7*delta,f"coût : {simplification(self.coût1)}",f3,'black')
        texte2(t*1.33,4.5*delta,f"+{self.bonus1}/click",f1,'red')
        # Texte du second bonus (+10 per sec)
        texte2(t,5.3*delta,"+10 par seconde",f1,'black')
        texte2(t,5.7*delta,f"coût : {simplification(self.coût2)}",f3,'black')
        texte2(t*1.33,5.5*delta,f"+{self.bonus2}/sec",f1,'red')
        # Texte du troisième bonus (+2% per second)
        texte2(t,6.3*delta,"+2% par seconde",f1,'black')
        texte2(t,6.7*delta,f"coût : {simplification(self.coût3)}",f3,'black')
        texte2(t*1.33,6.5*delta,f"+{self.bonus3}%/sec",f1,'red')
        # Texte du quatrième bonus
        texte2(t,7.3*delta,"coût /10",f1,'black')
        texte2(t,7.7*delta,f"coût : {simplification(self.coût4)}",f3,'black')
        # Texte du bouton de fin de partie
        texte2(t,8.5*delta,"Stop!",f1,'black') 
        # Score actuel
        texte2(l/2,2*delta,simplification(self.score),f2,'black')
        
# Les 4 bonus sont simples est assez similaires, ils suivent tous le même schéma
def capture(event):
    if état.stop: # Si le jeu est en marche on a plein de possibilités:
        D = (c - event.x)**2 + (k - event.y)**2 # On vérifie la distance du curseur avec le centre du cookie
        if D < (l/5)**2: # Si le curseur est sur le cookie on augmente le score selon le bonus1
            état.score = état.score + état.bonus1 
            état.affichage() #Je dois faire cette commande sinon le score ne s'actualise que à tictac, soit toutes les secondes ce qui est trop long
            texte2(event.x,event.y-10,('+',état.bonus1),f1,'black') # Petit effet pour voir en direct combien on a rajouté mais c'est pas super
        elif event.x > l/1.8 and event.x < (l-l/5): # J'ai fait en sorte de n'avoir qu'une colonne de possibilité de click pour simplifier
            if event.y > 4*delta and event.y < 5*delta: # Cas où on click sur le premier bonus
                if état.score >= état.coût1 : # On vérifie qu'on a bien l'argent
                    état.bonus1 = état.bonus1 + 1
                    état.score = état.score - état.coût1 # On retire ce qu'on a payé
                    temp = état.coût1
                    état.coût1 = état.coût1 *2
                    état.affichage()
                    texte2(event.x,event.y-10,f"- {simplification(temp)}",f1,'black')
            elif event.y > 5*delta and event.y < 6*delta: # Cas où on click sur le deuxième bonus
                if état.score >= état.coût2 :
                    état.bonus2 = état.bonus2 + 10
                    état.score = état.score - état.coût2
                    temp = état.coût2
                    état.coût2 = état.coût2 *2
                    état.affichage() # *
                    texte2(event.x,event.y-10,f"- {simplification(temp)}",f1,'black')
            elif event.y > 6*delta and event.y < 7*delta: # Cas où on click sur le troisième bonus
                if état.score >= état.coût3 :
                    état.bonus3 = état.bonus3 + 2
                    état.score = état.score - état.coût3
                    temp = état.coût3
                    état.coût3 = état.coût3 *2
                    état.affichage() # *
                    texte2(event.x,event.y-10,f"- {simplification(temp)}",f1,'black')
            elif event.y > 7*delta and event.y < 8*delta: # Cas où on click sur le quatrième bonus
                if état.score >= état.coût4 : 
                    état.coût1 = max(1,état.coût1 // 10) # Un des problèmes a été qu'on pouvait réduire les coûts à 0 donc j'ai mis une limite à 1
                    état.coût2 = max(1,état.coût2 // 10)
                    état.coût3 = max(1,état.coût3 // 10)
                    état.score = état.score - état.coût4
                    temp = état.coût4
                    état.coût4 = état.coût4 *2
                    état.affichage()
                    texte2(event.x,event.y-10,f"- {simplification(temp)}",f1,'black')
            elif event.y > 8*delta and event.y < 9*delta: # Cas où on clique sur la fin de partie
                état.stop = False # On arrête tictac et le jeu
                rectangle((0,0),(Largeur,Hauteur),'red') # Je recouvre le jeu pour montrer qu'on ne peut plus y accéder
                # Je montre le score et le temps
                rectangle((1.5*delta,2*delta),(8.5*delta,6*delta),'white')
                (co1,co2) = (((2*delta)+(8*delta))/2,((2*delta)+(6*delta))/2)
                texte2(co1,co2-delta,'Terminé!',f2,'black') 
                texte2(co1,co2,f"Votre score : {simplification(état.score)}",f1,'black')
                texte2(co1,co2+delta,minuterie(état.time),f1,'black')
                # Je place deux boutons pour continuer ou recommencer
                rectangle((delta,8*delta),(4*delta,9*delta),'white')
                rectangle((6*delta,8*delta),(9*delta,9*delta),'white')
                texte2(2.5*delta,8.5*delta,'Continuer?',f1,'black')
                texte2(7.5*delta,8.5*delta,'Recommencer?',f1,'black')
    else: # Ne s'active que si état.stop == False , soit lorsque qu'on a appuyé sur 'Finish!'
        if event.y >= 8*delta and event.y <= 9*delta: # Comme précédement je mets les boutons sur la même ligne pour simplifier
            if event.x >= delta and event.x <= 4*delta: # Pour continuer, il faut juste à changer état.stop et à relancer tictac
                état.stop = True
                tictac()
            elif event.x >= 6*delta and event.x <= 9*delta: # Pour recommencer
                # Je réinitialise les variables 
                état.score = 0
                état.time=0
                état.bonus1=1
                état.coût1=10
                état.bonus2=0
                état.coût2=100
                état.bonus3=0
                état.coût3=1000
                état.coût4=10000
                état.pepites = []
                for i in range(30):
                    x = random.randint(int(c-l/7), int(c+l/7))
                    y = random.randint(int(k-l/7), int(k+l/7))
                    état.pepites.append((x, y))
                # Je relance comme précédemment
                état.stop= True
                tictac()
        


def tictac():
    if état.stop: # Si on est sur l'écran de fin de partie, tictac est en pause
        état.time = état.time + 1 # Pour garder une trace du temps que l'on affichera en fin de partie
        # L'incrémentation du score grâce aux bonus accumulés
        actuel = int(état.bonus3*état.score/100)
        état.score = état.score + état.bonus2 + actuel
        état.affichage()
        # Juste pour afficher le gain à chaque seconde
        texte2(l/2,delta/2,f"+ {simplification(état.bonus2+actuel)}",f1,'black')
        Dessin.after(1000,tictac)
        # Je voulais mettre moins de ms pour rajouter des animations mais ça me fait rajouter des calculs et ça fait un peu lag...
        # Des fois sans explications le tictac() ne fait pas 1000 ms mais ça n'arrive que rarement
        
        
état=État()
tictac()
root.bind('<ButtonPress>',capture)
root.mainloop() 