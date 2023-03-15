####################################################################################################
# ! ------------------------- Cet etat est fini mais n'est pas utilisé ------------------------- ! #
####################################################################################################

from core import boucle_jeu, console
from core.ansi import Color

from . import menu


def init():
    ...


def affiche():
    """Affiche le nom des créateurs du jeu"""

    console.affiche_str(console.WIDTH//2, 5, None, "Un jeu crée par :", Color(1), (0.5,0.5))

    console.affiche_str(console.WIDTH//2, 10, None, "Corentin JEANNE", ancre=(0.5,0.5))
    console.affiche_str(console.WIDTH//2, 12, None, "Louise MARC", ancre=(0.5,0.5))
    console.affiche_str(console.WIDTH//2, 14, None, "Abdallah SALHI", ancre=(0.5,0.5))
    
    console.affiche_entree(console.WIDTH//2, 19, None, ancre=(0.5, 0.5))


def update():
    """Attend l'entree de l'utilisateur pour retourner au menu principal"""

    console.get_entree(placeholder="Appuyer sur ENTER pour continuer")

    # Revient sur le menu principal
    boucle_jeu.set_etat(menu.etat)


etat = boucle_jeu.Etat("Credits", init, affiche, update)
