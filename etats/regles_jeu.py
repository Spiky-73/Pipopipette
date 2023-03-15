from core import boucle_jeu, console


provenance = None
"""Le menu precedent auquel le jeu retourne apres cet etat."""


def init():
    ...


lignes = [
    "But du jeu : avoir le plus de cases coloriées par sa couleur.",
    "Chacun leur tour, les joueurs colorient l'un des traits du quadrillage du plateau de jeu.",
    "Lorsqu'un joueur colorie le dernier trait entourant une case, c'est-à-dire qu'il ferme la case,",
    "cette case se colorie de la couleur de ce joueur, et il gagne un point. Il peut également rejouer.",
    "",
    "Comment jouer?",
    "Ecrivez d'abord le numéro de la case dont vous souhaitez colorier un côté,",
    "puis appuyez sur entrée pour valider.",
    "Ecrivez ensuite quel côté vous souhaitez colorier, grâce aux touches suivantes :",
    "z -> haut",
    "q -> gauche",
    "s -> bas",
    "d -> droite",
    "A vous de jouer!"
]
"""Les lignes a afficher dans la console"""


def affiche():
    """Affiche les regles du jeu"""

    console.affiche_str(console.WIDTH/2, 3, None, "REGLES DU JEU", ancre=(0.5, 0))

    # Le nombre de ligne deja affichés
    i = 0
    # Affiche chaque ligne une à une car console.affiche_str ne permet l'affiche que d'une ligne à la fois.
    for l in lignes:
        # Compte le nombre de lignes affiches
        i += console.affiche_str(console.WIDTH/2,5+i, None, l, ancre=(0.5,0))
    
    # Zone d'entree de l'utilisateur
    console.affiche_entree(console.WIDTH//2, 5+i+3, None, ancre=(0.5, 0.5))


def update():
    """Attend l'entree de l'utilisatuer pour retourner à l'etat precendent"""
    
    console.get_entree(placeholder="Appuyer sur ENTER pour continuer")

    # N'utilise pas boucle_jeu.set_etat car cela reinitialiserait l'etat au lieu de le rependre
    boucle_jeu._etat = provenance


etat = boucle_jeu.Etat("Règles du jeu", init,affiche,update)

