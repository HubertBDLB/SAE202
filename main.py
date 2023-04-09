"""
Fichier :                   main.py
Date de création :          2023-03-14
Date de modification :      2023-04-09
Auteurs :                   Maxime Perrot & Ryan Troadec, 1E 

IUT de Lannion - BUT Informatique, SAE 2.02 : Exploration algorithmique

Ce programme est une interface graphique permettant de visualiser et résoudre
le problème des n reines. Il utilise l'algorithme de backtracking pour trouver
toutes les solutions possibles.
"""


###########################
# Importation des modules #
###########################


import pygame
import tkinter as tk
from tkinter import messagebox


################################
# Constantes et initialisation #
################################


pygame.init()
pygame.font.init()

NOIR = (0, 0, 0) 
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
COTE = 50 # Taille d'une case
FONT = pygame.font.SysFont('Consolas', 30)


############################
# Définition des fonctions #
############################


class Fenetre:
    def __init__(self, n, ips):
        """
        Fonction qui initialise la fenêtre
        """
        # Variables
        self.n = n
        self.solutions = []

        # Initialiser l'échiquier
        tailleFenetre = [(n)*COTE, (n+1)*COTE]                      # Taille de la fenêtre
        self.plateau = [[0 for j in range(n)] for i in range(n)]    # Initialiser le plateau de jeu
        self.fenetre = pygame.display.set_mode(tailleFenetre)       # Définir les dimensions de la fenêtre
        pygame.display.set_caption(f"Problème des {n} reines")      # Définir le titre de la fenêtre

        # Résoudre le problème
        self.resoudre()
        self.afficherSolutions(ips)

    def afficher(self, numSolution, totalSolutions):
        """
        Fonction qui dessine l'échiquier et les reines
        """
        self.fenetre.fill((255, 255, 255)) # Définir la couleur de fond
        for ligne in range(self.n):
            for colonne in range(self.n):
                # Définir la couleur de la case
                if (ligne + colonne) % 2 == 0:  # Si la case est blanche
                    couleur = NOIR
                else:                           # Si la case est noire
                    couleur = BLANC

                pygame.draw.rect(
                    self.fenetre,                               # Surface
                    couleur,                                    # Couleur de la case
                    [COTE * colonne, COTE * ligne, COTE, COTE]  # Dimensions de la case
                )

                if self.plateau[ligne][colonne] == 1:
                    pygame.draw.circle(
                        self.fenetre,                                         # Surface
                        ROUGE,                                                # Couleur du cercle
                        (COTE * colonne + COTE//2, COTE * ligne + COTE//2),   # Centre du cercle
                        (COTE//2)-2                                           # Rayon du cercle
                    )
        
        texte = FONT.render(str(numSolution) + "/" + str(totalSolutions), False, (0, 0, 0)) # Créer le texte
        coordonnesTexte = (self.n*COTE - texte.get_width(), (self.n+1)*COTE - texte.get_height()) # Calculer les coordonnées du texte
        self.fenetre.blit(texte, coordonnesTexte) # Afficher le texte
        pygame.display.flip() # Mettre à jour l'affichage

    def estSur(self, ligne, colonne):
        """
        Fonction pour vérifier si une reine peut être placée dans la position (ligne, colonne)
        """
        for i in range(ligne):
            if self.plateau[i][colonne] == 1:
                return False
            j = ligne - i
            if colonne-j >= 0 and self.plateau[i][colonne-j] == 1:
                return False
            if colonne+j <= self.n-1 and self.plateau[i][colonne+j] == 1:
                return False
        return True

    def resoudre(self,row = 0):
        """
        Fonction qui résout le problème des n reines
        """

        if row == self.n: 
            self.solutions.append([list(row) for row in self.plateau])
            return
        for column in range(self.n): 
            if self.estSur(row, column):
                self.plateau[row][column] = 1
                self.resoudre(row+1)
                self.plateau[row][column] = 0

    def afficherSolutions(self, ips):
        """
        Fonction qui affiche toutes les solutions
        """
        numSolution = 0
        totalSolutions = len(self.solutions)

        for solution in self.solutions:
            self.plateau = solution
            self.afficher(numSolution, totalSolutions)
            pygame.time.delay(int((1/ips)*1000))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            numSolution += 1

def init():
    """
    Fonction qui crée la fenêtre qui demande et renvoie la taille de l'échiquier
    """

    # Créer la fenêtre
    fenetre = tk.Tk()
    fenetre.title("S2.02")
    fenetre.geometry("300x220")
    fenetre.resizable(width=False, height=False)

    # Variable de widget
    nSpinBox = tk.IntVar() # Valeur du spinbox (nombre de reines)
    nSpinBox2 = tk.IntVar() # Valeur du spinbox (nombre d'images par seconde)

    # Créer les widgets
    titre = tk.Label(       fenetre, text="Problème des n reines", font=("Arial", 20))
    cadre =     tk.Frame(   fenetre                                                 ) 
    cadre2 =    tk.Frame(   fenetre                                                 )
    label =     tk.Label(   cadre,   text="Nombre de reines"                        )
    spinbox =   tk.Spinbox( cadre,   from_=4, to=100, width=2, textvariable=nSpinBox)
    label2 =    tk.Label(   cadre2,  text="Solutions par seconde"                   )
    spinbox2 =  tk.Spinbox( cadre2,  from_=1, to=20, width=2, textvariable=nSpinBox2)
    button =    tk.Button(  fenetre, text="Valider", command=fenetre.destroy        )
    info =      tk.Label(   fenetre, text="Ryan Troadec & Maxime Perrot\nIUT de Lannion, BUT Informatique 1\nS2.02 Exploration algorithmique - 2023")

    # Afficher les widgets
    titre.pack(     ipadx=0,    ipady=0,    padx=0,     pady=0,     expand=True,    fill="x"                    )
    cadre.pack(     ipadx=0,    ipady=0,    padx=0,     pady=0,     expand=True,    fill="x"                    )
    label.pack(     ipadx=0,    ipady=5,    padx=10,    pady=5,     expand=True,    fill="x",   side="left"     )
    spinbox.pack(   ipadx=10,   ipady=5,    padx=10,    pady=5,     expand=True,    fill="x",   side="right"    )
    cadre2.pack(    ipadx=0,    ipady=0,    padx=0,     pady=0,     expand=True,    fill="x"                    )
    label2.pack(    ipadx=0,    ipady=5,    padx=10,    pady=5,     expand=True,    fill="x",   side="left"     )
    spinbox2.pack(  ipadx=10,   ipady=5,    padx=10,    pady=5,     expand=True,    fill="x",   side="right"    )
    button.pack(    ipadx=10,   ipady=10,   padx=0,     pady=0,     expand=True,    fill="both"                 )
    info.pack(      ipadx=0,    ipady=0,    padx=0,     pady=0,     expand=True,    fill="x"                    )
    

    # Lancer la fenêtre    
    fenetre.mainloop()

    # Renvoyer les valeurs des spinboxs
    return (nSpinBox.get(), nSpinBox2.get())

def main():
    """
    Fonction principale du programme
    """

    n,ips = init() # Récupère la taille de l'échiquier
    if n > 10:
        messagebox.showwarning("Attention", "Au delà de 10 reines, le programme peut être très lent")
    F = Fenetre(n,ips) # Crée la fenêtre


###############################
# Test du programme principal #
###############################


if __name__ == "__main__":
    main()