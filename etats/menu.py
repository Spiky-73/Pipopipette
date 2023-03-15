from core import boucle_jeu, console
from core.ansi import Color

from . import selection, regles_jeu


def init():
    pass


def affiche():
    """Affiche l'interface et les différents menu selectionables"""

    # Titre du jeu
    console.affiche_str(console.WIDTH//2, 5, None, "PIPOPIPETTE", Color(1,1), (0.5,0.5))
    
    # Affiche les menus selectionable
    console.affiche_str(console.WIDTH//2, 10, None, "JOUER", ancre=(0.5, 0.5))
    console.affiche_str(console.WIDTH//2, 12, None, "COMMENT JOUER",ancre=(0.5,0.5))
    console.affiche_str(console.WIDTH//2, 14, None, "QUITTER",ancre=(0.5,0.5))

    # Prepare la zone d'entree
    console.affiche_entree(console.WIDTH//2, 19, None, ancre=(0.5, 0.5))


def update():
    """Recuperer et utilise l'entree de l'utilisateur"""

    # Demande a l'utilisateur ce qu'il veut faire
    console.info_entree(info="Ecrivez l'initiale d'un des choix ci-dessus, puis appuyez sur ENTRER")

    # str.strip().lower permet de 'normaliser' la chaine : minuscule sans espace sur les bord
    entree = console.get_entree(placeholder="Jouer | Comment jouer | Quitter").strip().lower() or 'j'

    # Change parmis les menus en fonction du choix de l'utilisateur
    if(entree in ['j','jouer']):
        boucle_jeu.set_etat(selection.etat)
    # elif(entree == 'c' or entree == 'credits'):
    #     boucle_jeu.set_etat(credits.etat)
    elif(entree in ['c','cj','comment', 'r','regles']):
        regles_jeu.provenance = etat
        boucle_jeu.set_etat(regles_jeu.etat)
    elif(entree in ['q','quitter']):
        boucle_jeu.stop()


etat = boucle_jeu.Etat("Menu principal", init, affiche, update)
