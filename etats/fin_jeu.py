from core import boucle_jeu, console, ansi
from . import menu, jeu 


def init():
    ...


def affich_joueur(j):
    """Affiche la place, le nom et le score d'un joueur"""

    # Coordonnée y en fonction du rang absolu pour eviter que un joueur n'en cache un autre
    y = (console.HEIGHT-5-len(jeu.classement))/2+jeu.rang_joueur_abs(j)

    # Le rang du jeur (int)
    r = jeu.rang_joueur(j)+1

    # Crée le rang du joueur (str)
    rang = str(r)+("er" if r == 1 else "e")

    # Affiche en 2 partie: le rang vers la gauche, puis le nom et le score vers la droite pour centre les ':'
    console.affiche_str(console.WIDTH/2, y, None,[rang, " : "], [jeu.col_rang(r)+jeu.joueurs[j].couleur,jeu.joueurs[j].couleur], (1,0))
    console.affiche_str(console.WIDTH/2, y, None,f"{jeu.joueurs[j].nom}, {jeu.joueurs[j].score} pts", jeu.joueurs[j].couleur, (0,0))


def affiche():
    """Affiche le classement des joueurs"""

    # Affiche chaque joeur un à un
    for i in range (len(jeu.joueurs)):
        affich_joueur(i)

    # Zone d'entree
    console.affiche_entree(console.WIDTH/2,console.HEIGHT-3, None,None, "", ansi.Color(fore=253),None, (0.5,0))


def update():
    """Recupere l'entree de l'utilisateur et change d'etat en fonction."""
    
    # Demande a l'utilisateur ce qu'il veut faire et 
    console.info_entree(info="Ecrivez l'initiale d'un des choix ci-dessus, puis appuyez sur ENTRER")

    # Recupere et 'normalise' le choix
    entree = console.get_entree(placeholder="Menu principal | Rejouer | Quitter").strip().lower() or 'm'

    # Change parmis les menus en fonction du choix de l'utilisateur
    if (entree in ['m',"menu","menu menu princiapal"]):
        boucle_jeu.set_etat(menu.etat)
    elif (entree in ['r',"rejouer"]):
        # Relance le jeu avec le mêmes parametres (joueur, grille)
        boucle_jeu.set_etat(jeu.etat)
    elif (entree in ['q',"quitter"]):
        boucle_jeu.stop()


etat = boucle_jeu.Etat("Classement final", init,affiche,update)

