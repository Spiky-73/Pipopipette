from core import boucle_jeu, console
from core.ansi import Color

from . import menu, jeu, regles_jeu


COULEURS: list[Color] = [
    Color(None, 9,   88 ),
    Color(None, 11,  100),
    Color(None, 10,  28 ),
    Color(None, 14,  29 ),
    Color(None, 12,  18 ),
    Color(None, 200, 89 ),
    Color(None, 1,   52 ),
    Color(None, 3,   58 ),
    Color(None, 2,   22 ),
    Color(None, 6,   23 ),
    Color(None, 4,   17 ),
    Color(None, 163, 53 )
]
"""
Les couleur disponible.
Leur ordre a de l'important car un nouveau joueur prendra la premère couleur disponible,
donc les 6 version "claires" des couleurs puis les 6 "sombres."
"""


joueurs:list[tuple[str,Color]] = None
"""La liste des joueur et leur couleur."""

grille:int = 6
"""La taille de la grille."""

en_edition_joueur = -1
"""Le joueur qui est entrain d'être modifié."""


def set_action(action = None):
    """
    Change l'action a effection lors de l'actualisation.
    None pour redemander l'action.
    Prend comme argument une fonction sans argument: () -> None.
    """
    global _action_actuelle
    _action_actuelle = action

# L'action a effectuer lors de l'actualisation
# fonction: () -> None
_action_actuelle = None


def init():
    """
    Intilisalise l'etat de selection des joueurs.
    2 joueurs son selectionés par defaut.
    """

    global joueurs, en_edition_joueur

    # Intialise la liste de joueur
    joueurs = []

    # Ajoute 2 joueurs, un rouge et un bleu
    ajoute_joueur(None, 0)
    ajoute_joueur(None, 4)


LARGEUR_JOUEUR = 30
"""
La largeur du rectangle sur lequel est affiche un joueur.
Permet un affichar sur 3 collones.
"""


def affiche_joueur(j):
    """Affiche le joueur `i`."""

    # Calcule la position de l'affichace, dans l'ordre:
    #   1  2  3 
    #   4  5  6 
    #   7  8  9 
    #   10 11 12
    x = 2+(console.WIDTH-4)*(1+2*(j%3))/6
    y = 1+5*(j//3)

    # Affiche le fond
    console.affiche_rect(x,y,LARGEUR_JOUEUR, 4, color=joueurs[j][1], ancre=(0.5,0))

    # affiche le nom du joueur a gauche, son numéro a droite
    console.affiche_entree(x, y+1, LARGEUR_JOUEUR, f"{j} nom", joueurs[j][0], joueurs[j][1], ancre=(0.5,0))
    console.affiche_str(x+LARGEUR_JOUEUR/2-1, y, LARGEUR_JOUEUR, f"J{j+1}", joueurs[j][1]+Color(3), (1, 0))

    # Affiche sa couleur de ligne
    console.affiche_rect(x, y+2, LARGEUR_JOUEUR-4, 1, '▄', joueurs[j][1], ancre=(0.5, 0))

    # Utilise pour changer la couleur du joueur
    console.affiche_entree(x, y+3, LARGEUR_JOUEUR, f"{j} col", "", joueurs[j][1], ancre=(0.5,0))



def affiche():
    """Affiche l'interface de selection des joueurs."""

    # Affiche les joueurs un à un
    for j in range(len(joueurs)):
        affiche_joueur(j)

    # Affiche la taille de la grille de jeu
    console.affiche_str(console.WIDTH/2, console.HEIGHT-1, None, f"Grille de {jeu.TAILLE_GRILLE}x{jeu.TAILLE_GRILLE}", ancre=(0.5, 0))
    
    # entree de l'user
    console.affiche_entree(console.WIDTH/2, 21, None, "in", ancre=(0.5, 0))


def ajoute_joueur(nom:str = None, col:Color = None):
    """
    Ajoute un joueur.
    Si son nom n'est pas donnés, il prend "Joeur X" ou X est le plus petit entier possible a partir de 1.
    Si sa couleur n'est pas donnés, elle prend la première couleur de libre de `COULEURS`.
    """

    if(nom is None): # Nom par defaut

        # Liste les noms pris
        noms = [i[0] for i in joueurs]

        # Prends le premier "Joueur X" de libre, partant de 1
        i = 1
        while f"Joueur {i}" in noms: i+=1
        nom = f"Joueur {i}"

    if(col is None): # Nom par defaut

        # Liste les couleurs prises
        couleur_prises = [j[1] for j in joueurs]

        # Prends la première couleur de libr
        col = 0
        while COULEURS[col] in couleur_prises: col+=1

    # Ajoute le joueur
    joueurs.append([nom, COULEURS[col]])


def ajoute_joueurs():
    """
    Ajoute plusieurs joueurs au jeu.
    Demande a l'user le nombre de joueurs a ajouter.
    """
    
    if(len(joueurs) >= len(COULEURS)): # Verifie que on peut ajouter des joueurs
        console.info_entree('in', "Le nombre max de joueur est atteint")
        set_action()

    else: # Demand le nombre de joueurs à ajouter
        console.info_entree("in", "Entrez le nombre de joueur à ajouter ou + pour ajouter et éditer un joueur")

        # "normalise l'entree"
        n = console.get_entree("in", "Ajouter ", "nb | + | Retour").strip().lower()
        
        if(n in ['r',"retour"]): # Annule l'ajout
            set_action()

        elif(' ' in n): # Plusieurs mots/nombres
            console.erreur_entree(f"in", "entrez seulement 1 nombre")

        elif (n == '+'): # Si +, ajoute 1 joueurs et le modifie
            ajoute_joueur()
            modifie_joueur(len(joueurs)-1)

        elif(not n.isdigit()): # Nombre non valide
            console.erreur_entree(f"in", "Nombre invalide : entrez un nombre positif")
       
        else: # Ajoute n joueurs
            n = int(n)

            if(n+len(joueurs) > len(COULEURS)): # N'ajoute pas trop de joueurs
                n = len(COULEURS) - len(joueurs)

                # Informe l'utilisateur
                console.info_entree('in', f"Seulement {n} joueur on étés ajoutés")
            
            # Ajoute n joueurs
            for _ in range(n): ajoute_joueur()
            set_action()

    
def modifie_joueur_nom():
    """Demande et modifie le nom du joueur `en_edition_joueur`"""

    # Recupere les noms pris hors celui du joueur lui meme
    noms = [i[0] for i in joueurs]
    noms.remove(joueurs[en_edition_joueur][0])

    # Demande le nouveau nom 
    console.info_entree(f"{en_edition_joueur} nom", "Entrez votre nom")

    # Si le nom n'est pas mentione, il reste inchangé
    nom = console.get_entree(f"{en_edition_joueur} nom").strip() or joueurs[en_edition_joueur][0]
    
    if (len(nom) > jeu.LARGEUR_RECT_JOUEUR): # Nom trop long
        console.erreur_entree(f"{en_edition_joueur} nom", "Ce nom est trop long")

    elif(nom in noms): # Nom deja pris
        console.erreur_entree(f"{en_edition_joueur} nom", "Ce nom est déjà pris")
    
    else: # Change le mon puis edite la couleur
        joueurs[en_edition_joueur] = (nom,joueurs[en_edition_joueur][1])
        set_action(modifie_joueur_col)
    

def modifie_joueur_col():
    """Demande et modifie la couleur du joueur `en_edition_joueur`"""

    # Trouve les coordonnées de la bare de couleur dans le rect du joueur
    x = 2+(console.WIDTH-4)*(1+2*(en_edition_joueur % 3))/6
    y = 1+5*(en_edition_joueur//3)

    # Efface la bare de couleur
    console.affiche_rect(x, y+2, LARGEUR_JOUEUR-4, 1, ' ', joueurs[en_edition_joueur][1], ancre=(0.5, 0))

    # Liste les couleurs prises hors celle du joueur
    couleur_prises = [j[1] for j in joueurs]
    couleur_prises.remove(joueurs[en_edition_joueur][1])

    # Sert a cacher le texte 
    cache = Color(0,joueurs[en_edition_joueur][1].back,joueurs[en_edition_joueur][1].back)

    # Affiche les couleurs avec leur numéro a la place
    # les couleurs prises ne sont pas affichés car cachés
    console.affiche_str(
        x, y+2, LARGEUR_JOUEUR-4, 
        [f'{(i+1):2}' for i in range(len(COULEURS))],
        [(COULEURS[i] if not COULEURS[i] in couleur_prises else cache) for i in range(len(COULEURS))],
        (0.5,0)
    )

    # Recupere la couleure choisie or celle du joueur
    console.info_entree(f"{en_edition_joueur} col", "Entre ta couleur")
    col = console.get_entree(f"{en_edition_joueur} col").strip() or joueurs[en_edition_joueur][1]

    if(not col.isdigit()): # Couleure invalide
        console.erreur_entree(f"{en_edition_joueur} col", "Entrez un nombre positif")
    
    else: # change la couleur
        col = int(col)-1

        if(col <0 or col >= len(COULEURS)): # Couleur n'existant pas
            console.erreur_entree(f"{en_edition_joueur} col", f"Nombre entre 0 et {len(COULEURS)-1} (inclus)")

        elif(COULEURS[col] in couleur_prises): # Couleur deja prise
            console.erreur_entree(f"{en_edition_joueur} col", f"Cette couleur est deja prise")
       
        else: # Change la couleur du joueur et arrete l'edition
            joueurs[en_edition_joueur] = (joueurs[en_edition_joueur][0], COULEURS[int(col)])
            set_action()


def modifie_joueur(j:int = None):
    """Demande un joueur a modifier puis le modifie"""

    global en_edition_joueur

    if(j is None): # Si aucun joueur n'est specifié, le demande a l'user
        console.info_entree("in", "Entrez le numéro du joueur à modifier")
        j:str = console.get_entree("in", "Modifier ", "numero | Retour").lower()


    if(j == 'r' or j == "retour"): # Annule la modification
        set_action()

    elif(not j.isdigit()): # pas un nombre
        console.erreur_entree("in", "Numero invalide: num doit être un entrier positif")
    
    else: # Prepare a modifier le joueur
        j = int(j)-1

        if(j < 0 or j >= len(joueurs)): # Joueur invalide
            console.erreur_entree("in", "Ce joueur n'existe pas")

        else: # Modifie le nom du joueur, puis sa couleur
            en_edition_joueur = j
            set_action(modifie_joueur_nom)


def suprime_joueur(j:int = None):
    """Demande puis suprime un joueur."""

    if(len(joueurs) == 0): # Aucun joueur a suprimer
        console.info_entree("in", "Il n'y a pas de joueur à suprimer")
        set_action()
    else:
        if(j is None): # Demande le joueur si il n'est pas specifié
            console.info_entree("in", "Entrez le numéro du joueur à suprimer ou - pour suprimer le dernier joueur")
            j = console.get_entree("in", "Suprimer ", "num | - | Retour").lower().strip()
        
        if(j == "r" or j == "retour"): # Annule la surpession
            set_action()

        elif(' ' in j): # Plusieurs mots
            console.erreur_entree("in", "Selectionez seulement 1 joueur")

        elif(j == "-"): # Suprime le dernier joueur
            joueurs.pop(len(joueurs)-1)

        elif(not j.isdigit()): # Nombre invalide
            console.erreur_entree("in", "Numero invalide: N doit être un entrier positif")

        else: # surpime un joueur
            num = int(j)-1

            if(num < 0 or num >= len(joueurs)): # Joueur inexistant
                console.erreur_entree("in", "Ce joueur n'existe pas")

            else: # surprime le joeur j
                joueurs.pop(num)
                set_action()


def commence_partie():
    """Lance la partie avec les joueur et la taille de grille parametrées."""

    if(len(joueurs) < 2): # Impossible de jouer tout seul !
        console.erreur_entree('in', "Il faut au moins 2 joueur pour pouvoir jouer")

    else: # Lance le jeu
        boucle_jeu.set_etat(jeu.etat)


def taille_grille(t:int = None):
    """Demande et change la taille de la grille."""

    global grille

    if(t is None): # Demande la taille si elle n'est pas donnée
        console.info_entree("in", "taille de la grille (entre 2 et 8) inclus")
        t: str = console.get_entree("in", "Grille carrée de ", "taille")
    
    if(not t.isdigit()): # Pas un nombre
        console.erreur_entree("in", "Nombre invalide: entrez un entier entre 2 et 8 (inclus)")

    else: # Reupere la taille de la grille
        t = int(t)
        
        if (t < 2 or t > 8): # Verifie la taille de la grille
            console.erreur_entree("in", "Nombre invalide, entrez une valeur comprise entre 2 et 8")
       
        else: # Change la taille de la grille
            grille = t
            set_action()


def update():
    """Execute l'action a faire ou en demande un nouvelle a l'user."""

    if(_action_actuelle is not None): # Si il y a une modif a faire, l'execute
        _action_actuelle()

    else: # demande une nouvelle action

        if(len(console.get_messages('in')) == 0): # N'affiche pas le message de choix si il y d'autre message sur la console
            console.info_entree("in", "Ecrivez l'initiale de votre choix puis appuyez sur ENTRER")
        
        # Recupere le choix et le 'normalise'
        entree = console.get_entree( "in", "", "Ajouter joueur|Modifier joueur|Supprimer joueur|Taille grille|Comment jouer|Retour|Jouer").strip().lower() or 'j'
    
        # Change l'action en fonction des choix de l'user
        if(entree in ['j',"jouer"]):
            commence_partie()
        elif(entree in ['r',"retour"]):
            boucle_jeu.set_etat(menu.etat)
        elif(entree in ['a',"ajouter"]):
            set_action(ajoute_joueurs)
        elif(entree in ['m',"modifier"]):
            set_action(modifie_joueur)
        elif(entree in ['s',"suprimer"]):
            set_action(suprime_joueur)
        elif(entree in ['t',"taille","taille grille", "grille"]):
            set_action(taille_grille)
        elif(entree in ['c',"comment"]):
            regles_jeu.provenance = etat # pour ne pas perdre les joueures etc...
            boucle_jeu.set_etat(regles_jeu.etat)


etat = boucle_jeu.Etat("Selection des joueurs", init, affiche, update)
