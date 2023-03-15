"""
Regroupe les principeaux codes ansi afin de créer des couleurs, déplacer le cursuer et effacer la console.

Pour avoir une liste compléte des codes ansi utilisable:
    https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#escape

constantes:
    ESC:
        Charactère d'echappement

    CSI, OSC, DCS:
        Différents codes par lequels commences les codes ansi.

classes:
    Color:
        Génére les codes ansi pour les modes et couleurs de la console.

    Cursor:
        Contient les codes ansi permetant de déplacer le curseur sur la console.

    Screen:
        Contient les codes ansi permetant d'afficher des partie de la console.
"""

# Tous les codes ansi doivent commencer par ce charactère
ESC = "\033"
"""Code d'echapement dela console"""

# Ces 'escape codes' caractérise chaque code ansi et tous commence par une de ces chaine
CSI = ESC+'['
"""Control Sequence Introducer"""

OSC = ESC+']'
"""Operating System Command"""

DCS = ESC+'P'
"""Device Control String"""



class Color:
    """
    Génére les codes ansi pour les modes et couleurs de la console.
    """

    modes: list[int]
    """Les modes de la couleur (gras, italique....). Nombres entre 0 et 9 (inclus)."""

    fore:int
    """La couleur du text. Nombre entre 0 et 255 (inclus)."""

    back:int
    """La couleur du fond. Nombre entre 0 et 255 (inclus)."""


    def __init__(self, modes: list[int]=None, fore:int=None, back:int=None):
        # Initialise les variable de la couleur grave aux parametres

        # Garantie que modes est une liste
        self.modes = [] if modes is None else modes.copy() if type(modes) is list else [modes]

        # Initialise les couleurs du text et du fond
        self.fore = fore
        self.back = back

    def __add__ (self, other):
        # Ahjoute les couleurs et retourne la nouvelle couleur
        return Color(
            # Les modes sont combinés et indépendant des couleurs originelles
            self.modes.copy()+other.modes.copy(),

            # Les couleur tu text et du fond sont modifies seulement si elles ne sont pas initialisés
            # dans la couleur a gauche de l'operateur
            other.fore if self.fore is None else self.fore,
            other.back if self.back is None else self.back
        )

    def code(self) -> str:
        """Génère un code ansi permetant ce changer la couleur de la console.

        Returns:
            str: Le code ansi correspondant la la couleur.
        """

        # Réinitialise la couleur de la console afin que `None` corresponde à la couleur par defaut
        code = Color.Reset()

        # Ajoute les modes 
        if(len(self.modes) > 0):
            code+=CSI+";".join(map(str, self.modes))+"m"

        # Ajoute la couleur du text
        if(self.fore is not None):
            code += CSI + "38;5;" + str(self.fore) + "m"

        # Ajoute la couleur du fond
        if(self.back is not None):
            code += CSI + "48;5;" + str(self.back) + "m"
        
        return code
    
    def __str__(self) -> str:
        return self.code()

    def Reset() -> str:
        """Génére un code ansi réinitialisant la couleur de la console.

        Returns:
            str: le code ansi réinitialisant la couleur de la console.
        """

        return CSI + "0m"



class Cursor:
    """Contient les codes ansi permetant de déplacer le curseur sur la console."""

    def Goto(x:int,y:int) -> str:
        """Place le curseur sur la yème ligne, xème colonne (origine (1,1))."""
        return CSI + str(y) + ';' + str(x) + 'H'

    def Up(n:int) -> str:
        """Deplace le curseur de `n` lignes vers le haut."""
        return CSI + str(n)+'A'

    def Down(n:int) -> str:
        """Deplace le curseur de `n` lignes vers le bas."""
        return CSI + str(n)+'B'

    def Right(n:int) -> str:
        """Deplace le curseur de `n` lignes vers la gauche."""
        return CSI + str(n)+'C'

    def Left(n:int) -> str:
        """Deplace le curseur de `n` lignes vers le droite."""
        return CSI + str(n)+'D'

    def Save() -> str:
        """
        Sauvegarde la position du curseur. Une seule position peut être utiliser la fois.
        Utilisez `Cursor.Recall()` pour revenir a cette position.
        """
        return ESC + "7"

    def Recall() -> str:
        """
        Retourne à la derniere postion sauvgarder du curseur.
        Utilisez `Cursor.Save()` sauvegarder sa position.
        """
        return ESC + "8"


class Screen:
    """Contient les codes ansi permetant d'afficher des partie de la console."""

    def Clear() -> str:
        """Efface l'ecran."""
        return CSI+'2J'

