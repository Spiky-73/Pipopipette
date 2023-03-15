"""
Permet de créer un jeu avec différent menu.

Contient les fonction nécessaire pour obtenir une boucle de jeu et gérer différents états.

Pour créer un jeu, créez un fichier contenat un Etat et appelez `start` avec cet etat.

classes:
    Etat:
        Représente un état avec un affichage et des entrees.
        Stoque les differentes fonctions caractérisant l'etat.

fonctions:
    set_etat(nouv_etat):
        Change l'etat actif du jeu.

    start(nom, etat_init):
        Lance le jeu à l'etat souhaité.

    stop():
        Arrète le jeu.
"""


from typing import Callable
from . import console

class Etat:
    """
    Represente un état possible que peut prendre le jeu.
    Chaque état est stoqué dans son propre module (fichier .py).

    Chaque état est composé de 3 fonctions:
    - une fonction d'initialisastion `init()` qui initialise les variables nécessaires au fonctionnement de l'état.
    - une fontion d'affichage `affiche()` qui affiche tout les éléments à afficher.
    - une fonction d'actualisation `update()` qui utilise les entrés de l'utilisateur.

    Chaque état est stoque dans une variable de son module sous la forme:  `etat = Etat(init, affiche, update)`.
    Pour changer d'état, on appelle `boucle_jeu.set_etat(<etat>.etat)`.
    """

    nom:str
    """Le nom de l'etat"""

    # Fonction initialisant l'état
    _init: Callable[[], None]

    # Fonction affichant l'état
    _affiche: Callable[[], None]

    # Fonction affichant l'état
    _update: Callable[[], None]


    def __init__(self, nom, init: Callable[[], None], affiche: Callable[[], None], update: Callable[[], None]):
        # Initialise les differents membres
        self.nom = nom
        self._init = init
        self._affiche = affiche
        self._update = update
    
    def init(self):
        """Initialise l'état."""
        self._init()
    
    def update(self):
        """Affiche l'état."""
        self._update()
    
    def affiche(self):
        """Actualise l'etat"""
        self._affiche()

jeu: str
"""Le nom du jeu"""

# Stoque le nom de l'état actuel du jeu.
_etat: Etat = None


# Est ce que le jeu est lancé ou non
_en_jeu: bool = False


def set_etat(nouv_etat: Etat):
    """Change l'état du jeu à `nouv_etat` et l'initialise.
    Si ce dernier est nul, le jeu s'arrète.

    Args:
        nouv_etat (Etat): Le nouvel etat du jeu.
    """

    global _etat, _en_jeu

    # Change l'etat du jeu
    _etat = nouv_etat

    # Arrete je jeu si il est nul
    if (_etat is None):
        _en_jeu = False

    # L'initialise s'il n'est pas nul et continue le jue
    else:
        _en_jeu = True
        console.set_titre(jeu+" : "+_etat.nom)
        _etat.init()
    
    # Efface la console et la prepare pour un nouvel etat
    console.reset()


def start(nom:str, etat_init: Etat):
    """Lance le jeu `nom` à l'etat `etat_init`."""
    global jeu

    # Paramètre la taille de la console et son nom
    jeu = nom
    console.set_titre(nom)
    console.set_taille_console(100, 25)

    # Lance le jeu à l'etat specifié.
    set_etat(etat_init)

    # Actif tant que l'utilisateur de quite pas le jeu
    while (_en_jeu):

        # Efface l'écran et affiche l'état actuel
        console.pre_affiche()
        _etat.affiche()

        # Actualise l'état actuel
        _etat.update()


def stop():
    """Arrete le jeu."""

    set_etat(None)
