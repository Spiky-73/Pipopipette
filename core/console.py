"""
Contient de nombreuses fonction permettant d'obetenir un affichage graphique de la console.

constantes:
    WIDTH, HEIGHT:
        Les dimentions de la console.

fonctions:
    set_titre(titre):
        Change le titre de la console.
    
    set_taille_console(w, h):
        Change la taille de la console.
    
    reset():
        Efface la console et réinitialise les entrées.

    pre_affiche():
        Prépare la console a un affichage.

    affiche(x,y, texture, color, ancre):
        Affiche un texture.

    affiche_rect(x,y, w,h, char, color, ancre):
        Affiche un rectange

    affiche_str(x,y, w, text, color, ancre) -> int:
        Affiche un chaine de caractère/

    affiche_entree(x,y, w, nom, defaut, col_on, col_off, ancre):
        Affiche un zone d'entrée.

    get_entree(nom, requete, placeholder) -> str:
        Récupère un entrée de l'utilisatuer.

    info_entree(nom, info, first):
        Ajoute un message d'info a une entrée.

    erreur_entree(nom, erreur):
        Ajoute un message d'info a une entrée.

    get_messages(nom):
        Recupère les messages d'une entrée.

classes:
    Entree:
        Les paramétres d'une zone d'entrée
"""
import os, copy

from . import ansi


WIDTH: int = 100
"""La largeur de la console."""
HEIGHT: int = 25
"""La hauteur de la console."""


def set_titre(titre:str):
    """Change le titre de la console."""
    os.system(f"title {titre}")


def set_taille_console(largeur: int, hauteur: int):
    """Change la taille de la console (en nombre de charactères)."""

    # actualise les contantes pour la longeur et hauteur de la console
    global WIDTH, HEIGHT
    WIDTH, HEIGHT = largeur, hauteur

    # Utilse le module os afin de pourvoir change la taille de la console
    os.system(f"mode con: cols={WIDTH} lines={HEIGHT}")


def reset():
    """Réinitialise les variables liés a l'affichage de la console, tel que les entrees et leur informations."""
    _entrees.clear()
    _infos.clear()
    pre_affiche()


def pre_affiche():
    """Prépare la console à un affichage."""

    #  Efface la console
    print(end=ansi.Screen.Clear())
    print(end = ansi.Cursor.Goto(0,0))

    # Efface les entrees de l'image d'avant.
    # Leurs infos ne sont pas éffaces car elles doivent être sauvegarder
    # si l'entrée est réutilisée lors de l'affichage suivant
    _entrees.clear()


def affiche(x: int, y: int, texture: list[list[str]], couleur:list[list[ansi.Color]], ancre:tuple[int,int]=(0,0)):
    """Affiche une texture avec les couleurs correspondantes.

    Une texture est une liste de lignes (liste d'élements)
    Chaque élement a sa propre couleur et elles sont toutes stoqués dans une liste de même dimention que `texture`
    L'élement `texture[i][j]` est associé avec la couleur `couleur[i][j]`.

    Args:
        x, y (int, int): Les coordonées a partir desquelles est affichée la texture
        texture (list[list[str]]): La texture a afficher
        couleur (list[list[ansi.Color]]): Les couleurs des élements de la texture
        ancre (tuple[int,int], optional): Le point d'ancrage de la texture du rectange (de 0 à 1). Defaults to (0,0).
    """

    # Stoque les lignes affiches, contenant les codes ansi et regoupant les éléments d'une ligne
    text_col:list[str] = []

    # Groupe les élement des lignes et ajoute leur code ansi
    for text, col in zip(texture, couleur):

        line = ""

        # Pour chaque élement de la ligne,
        # ajoute la couleur du text si spécifié (ou la réinitialise) puis le texte
        for t, c in zip(text, col):
            line+= (c.code() if c is not None else ansi.Color.Reset()) + t

        text_col.append(line)

    # Trouve les coordonnées a partir des quelles afficher la texture.
    # Pour cela, on modifie x et y avec l'ancre.
    # (0,0) représente le coin à gauche en haut de la texture et (1,1) celui à droite en bas
    # On utilise `texture` et non `text_col` car les codes ansi modifient la longueur de la ligne
    x = int(x-ancre[0]*len("".join(texture[0])))
    y = int(y-ancre[1]*len(texture))

    # Positionne le curseur et sauvegarde sa position pour savoir ou est le début de la ligne
    print(ansi.Cursor.Goto(x+1, y+1), end=ansi.Cursor.Save())

    # Affiche la texture
    # Entre chaque élément, la position sauvegardée descend d'une ligne, ce qui permet d'afficher chaque élément une ligne apres l'autre
    print(*text_col, sep=ansi.Cursor.Recall()+ansi.Cursor.Down(1)+ansi.Cursor.Save(), end=ansi.Color.Reset())


def affiche_rect(x:int,y:int, w:int, h:int, char:str = ' ', color:ansi.Color=None, ancre:tuple[int,int]=(0,0)):
    """Affiche un rectange aux coordonées x,y de couleur color, centre autours de l'ancre

    Args:
        x, y (int, int): les coordonnés du rectange
        w, h (int, int): la taille di rectange
        char (str, optional): Le char compossant le rectange. Defaults to ' '.
        color (ansi.Color, optional): La couleur du rectange. Defaults to None.
        ancre (tuple[int,int], optional): Le point d'ancrage de la texture du rectange (de 0 à 1). Defaults to (0,0).
    """
    
    affiche(x, y, [[char*int(w)]]*int(h), [[color]]*int(h), ancre)


def affiche_str(x: int, y: int, w: int, text: str | list[str], color: ansi.Color | list[ansi.Color] = None, ancre: tuple[int, int] = (0, 0)) -> int:
    """Affiche une chaine de caractère composé d'un ou plusieurs morceau de couleur différentes.

    Si la ligne est trop longue et que le retour a la ligne est active,
    elle est écrite sur plusieur ligne, en fontion des partie du texte

    Args:
        x, y (int, int): Les coordonés de la chaine
        w (int): La longeur max de la chaine avant un a la ligne automatique. Si None, Il est désactivé
        text (str | list[str]): Les morceau de la chaine
        couleur (ansi.Color | list[ansi.Color], optional): La couleur des morceau de la chaine. Defaults to None.
        ancre (tuple[int, int], optional): Le point d'ancrage de la chaine (de 0 à 1). Defaults to (0, 0).

    Returns:
        int: le nombre de lignes occupé par la chaine
    """

    ret = 0
    # Si les élement afficher sont déja des liste, la fonction continue
    if (type(text) is list):

        # Si le retour a la ligne est activé
        if(w is not None):

            # Recherche le point de coupe dans le text et prend au moins un élément
            c, l_tot = 0, 0
            while(l_tot < w and c < len(text)):
                l_tot += len(text[c])
                c+=1
                
        # ne coupe pas le texte
        else :
            c = len(text)

        # Affiche la partie qui n'a pas été coupée
        affiche(x, y, [text[:c]], [color[:c]], ancre)
        ret = 1

        # Affiche le reste du texte si il y en a, la ligne en dessous
        if(c > 0 and c < len(text)):
            ret += affiche_str(x, y+1, w, text[c:], color[c:], ancre)


    # sinon elle les convertie en liste
    else:
        ret = affiche_str(x, y, w, [text], [color], ancre)

    return ret

class Entree:
    """Les paramètres d'une zone d'entrée de la console. """

    x: int
    """La coordonée x de la zone."""
    y: int
    """La coordonée y de la zone."""

    w: int
    """La largeur de la zone."""

    on: ansi.Color
    """La couleur de la zone losqu'elle est selectionée."""
    off: ansi.Color
    """La couleur de la zone losqu'elle n'est pas selectionée."""

    ancre: tuple[int, int]
    """Le point d'ancrage de la zone."""

    derniere_entree:str
    """La dernière entrée de la zone."""

    def __init__(self, x: int, y: int, w: int, defaut:str, on: ansi.Color = None, off: ansi.Color = None, ancre: str = None):
        self.x:int = x; self.y:int = y
        self.w:int = w
        self.on:ansi.Color = on; self.off:ansi.Color = off
        self.ancre:tuple[int,int] = ancre
        self.derniere_entree = defaut


_entrees: dict[str, Entree] = {}
_infos: dict[str, list[tuple[str, ansi.Color]]] = {}


def affiche_entree(x: int, y: int, w: int|None, nom: str | int = None, defaut:str="", col_: ansi.Color = None, col_off: ansi.Color = None, ancre:tuple[int,int] = (0,0)):
    """Affiche un zone dédié a l'entrée utiisateur pour étre utilisée par `get_entrée`.

    Ne demande rien a l'utilisateur et ne renvoie rien.
    Utilisez `get_entree` pour récuperer une entree. 

    Si un nom n'est pas spécifié, l'entree a comme nom le nombre d'entrée précedent 

    Args:
        x (int): Les coordonnées de la zone d'entree
        y (int): _description_
        w (int | None): La largeur max de la zone d'entree. Defaults to None.
        nom (str | int, optional): le nom de la zone d'entree. Defaults to None.
        defaut (str, optional): La valeur a afficher lorque l'entrée n'est pas utilisée. Defaults to "".
        on (ansi.Color, optional): La couleur de l'entrée lorqu'elle est séléctionée. Defaults to None.
        off (ansi.Color, optional): La couleur de l'entrée lorqu'elle n'est pas séléctionée. 'on' par defaut.Defaults to None.
        ancre (tuple[int,int], optional): Le point d'ancrage de la chaine (de 0 à 1). Defaults to (0,0).
    """
    # Nome automatiquement l'entrée si elle n'est pas nommée.
    if (nom is None):
        nom = len(_entrees)

    if (col_ is None):
        col_ = ansi.Color()

    #  Stoque les paramaètres de l'entrée
    # Si off est nul, elle prend comme valeur on
    _entrees[nom] = Entree(x, y, w, defaut, col_, col_ if col_off == None else col_off, ancre)

    # Crée le champ d'informations pour l'entrée
    if (not nom in _infos): _infos[nom] = []

    # Affiche la valeur par defaut de l'entrée
    affiche_str(x, y, w, defaut, _entrees[nom].off, ancre)


def get_entree(nom: str|int = 0, requete: str = "", placeholder: str = None) -> str:
    """Demande une requete a l'utilisateur un utilisant l'entree `nom` et renvoie sa réponse.

    Une valeur de remplacement est affiche tant que l'utilisatuer n'ecrit pas.
    Si elle n'est pas spécifiée, la derniere entrée de l'utilisatuer est utilisée.

    Args:
        nom_entree (str | int, optional): Le nom de l'entree. Defaults to 0.
        requete (str, optional): La demande pour l'utilisatuer. Defaults to "".
        placeholder (str, optional): La valeur par defaut de l'entrée. S'efface lorsque l'user écrit. Defaults to None.

    Returns:
        str: La réponse de l'utilisateur
    """
    # racoucit l'apel a l'entrée
    e = _entrees[nom]

    # Deternine la valuer de la valeur par defaut
    if (placeholder == None): placeholder = e.derniere_entree
    
    # copie la couleur active afin de ne pas la changer car elle peut etre modifée dans la fonction
    placeholder_color = copy.deepcopy(e.on)

    # Rend le placeholder "transparent"
    if (2 not in placeholder_color.modes):
        placeholder_color.modes.append(2)

    # Affiche les info sur des lignes individuelles
    off_y = 1
    for i in _infos[nom]:
        off_y += affiche_str(e.x, e.y+off_y, e.w, i[0], i[1], e.ancre)

    # Efface la valeure active
    affiche_str(e.x, e.y, e.w, ' '*len(e.derniere_entree), e.off, e.ancre)

    # Affiche la requete
    affiche_str(e.x, e.y, e.w, [requete, placeholder], [e.on, placeholder_color], e.ancre)


    # se positione apès la requete.
    # on ne peut pas utiliser ansi.Cusor.Save() car `affiche` modifierait cette position
    if (len(placeholder) > 0): print(end=ansi.Cursor.Left(len(placeholder)))

    # Recupere la reponse de l'user
    e.derniere_entree = input(e.on.code()+ansi.Cursor.Save())

    # se positione apès la requete puis au debut du texte affiche par l'entrée
    print(end=ansi.Cursor.Recall())
    if (len(requete) > 0): print(end=ansi.Cursor.Left(len(requete)))

    # Efface tout le texte écrit
    print(e.off.code(), end=" "*(len(requete) + max(len(placeholder), len(e.derniere_entree))))

    # Efface toutes les infos
    off_y = 1
    for i in _infos[nom]:
        off_y += affiche_str(e.x, e.y+off_y, e.w, ' '*len(i[0]), None, e.ancre)

    # Suprime les infos
    _infos[nom].clear()

    # Affiche la réponse de l'utilisatuer
    affiche_str(e.x, e.y, e.w, requete + e.derniere_entree, e.off, e.ancre)

    # revoie la reponse
    return e.derniere_entree


def erreur_entree(nom:str, erreur:str):
    """Ajoute une message d'erreur pour une entree.

    Il est affiché sous l'entrée losque d'elle est sélectionée.

    Args:
        nom (str): Le nom de l'entrée.
        erreur (str): Le message d'erreur.
    """
    _infos[nom].append((erreur, ansi.Color(1,9,52)))


def info_entree(nom: str = 0, info: str = "", first:bool=False):
    """Ajoute une message d'information pour une entree.

    Il est affiché sous l'entrée losque d'elle est sélectionée.

    Args:
        nom (str): Le nom de l'entrée.
        erreur (str): Le message d'information.
        first (bool): Affiche l'info en première si vrai. Default to False.
    """

    # Ajoute l'entrée en haut de la liste si `first` est vrai
    if (not first):
        _infos[nom].append((info, ansi.Color(3, 12, 18)))
    else:
        _infos[nom].insert(0,(info, ansi.Color(3, 12,18)))


def get_messages(nom:str|int = 0) -> list[tuple[str, ansi.Color]]:
    """Renvoie les message liées a une entrée.

    Args:
        nom (str | int, optional): Le nom de l'entrée. Defaults to 0.

    Returns:
        list[tuple[str, ansi.Color]]: Les messafe de l'entrée
    """

    return _infos[nom]
