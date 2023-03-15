import random


from core import boucle_jeu, console
from core.ansi import Color

from . import selection, fin_jeu, regles_jeu


class Joueur:
    """Represente un joueur, avec son nom, son score et sa couleur."""
    nom:str

    """Le nom du joueur."""

    score:int = 0
    """Le score du joeur."""

    couleur:Color
    """La couleur du joueur."""

    def __init__(self, nom, couleur, score = 0):
        # Cree un joueur
        self.nom = nom
        self.couleur = couleur
        self.score = score


# Ces 2 listes stoquent les memes données, mais dans un ordre different.
# Cela est possible caraa une classe, comme une liste est un object muable.
# Grace a cela, si on modifie le score d'un joueur dans `joeurs`,
# cela le modifiera aussi dans `classement` car il representent le même objet.
# Cela ne marcherai pas avec un tuple.

joueurs: list[Joueur] = None
"""Stoque les joueurs, dans l'ordre de jeu."""

classement:list[Joueur] = None
"""Stoque les joueurs, dans l'ordre du classement."""

tour:int = 0
"""Indice du joueur en train de jouer dans `joueurs`."""


TAILLE_GRILLE:int = 5
"""La taille de la grille"""

lignes:list[list[int]] = None
"""
Les lignes de la grille.
-1 si elles sont libre, sinon l'indice du joueur qui l'a prise.
"""

cases: list[list[int]] = None
"""
Les cases de la grille.
-1 si elles sont libre, sinon l'indice du joueur qui l'a prise.
"""

cases_remplies:int = 0
"""Le nombre total de cases remplie par tous le joueur."""



LARGEUR_RECT_JOUEUR = 20
"""La largeur du panneau du joueur."""

TAILLE_CASE: int = 3
"""La taille de la case en hauteur(inclu les bordures). *2 pour la largeur."""

CASE = ' '
"""Le character d'une case."""
POINT = '▀'
"""Le character d'un point ou coind  de case."""
LIGNE_H = '▀'
"""Le character d'une ligne horizontale."""

# Mis à ' ' car c'est la couleur du fond qui est change en fonction du joueur
LIGNE_V = ' '
"""Le character d'une ligne verticale."""


# Differents couleur pour les lignes, case et text des cases vides
COL_TEXT = 250
"""La couleur du numero d'une case vide."""
COL_LIGNE = 237
"""La couleur du ligne non prise."""
COL_BACK = 234
"""la couleur du fond d'une case vide."""



def cree_joueurs_classement(js: list[tuple[str, Color]]):
    """Cree la liste des joueurs et le classement à partir d'une liste de joueur comme celle de `seletion`."""

    # Recrée les joueurs avec leur nom et leur couleure
    joueurs = [Joueur(j[0], j[1]) for j in js]
    
    # rend l'ordre des joueurs aléatoire
    random.shuffle(joueurs)

    return joueurs, joueurs.copy()


def cree_grille_lignes(taille: int):
    """crée et retourne la grille des cotés de la bonne taille en fonction de la taille demandée."""

    # Cree la liste
    grille_ligne = []

    # Comptes les lignes
    ligne_hor = taille*[-1]
    ligne_ver = (taille+1)*[-1]


    # Onutlisie liste.copy() afin que tout les liste soient differentes
    # Ajoute une ligne de ligne_hor car il y en a une plus
    grille_ligne.append(ligne_hor.copy())

    # Rempli la matrice
    for _ in range(taille):
        grille_ligne.append(ligne_ver.copy())
        grille_ligne.append(ligne_hor.copy())
    
    return grille_ligne

#test taille_grille_cotes
# print (taille_grille_cotes(5,5))


def cree_grille_cases(taille: int):
    """crée et retourne la grille qui stocke les cases qui seront coloriées."""

    # Reinitialise le nombre de cases remplies
    global cases_remplies
    cases_remplies = 0

    # Cree la liste
    grille_cases = []

    # Compte le nombre le cases par ligne
    ligne = taille*[-1]

    # Remplit la matrice
    for i in range(taille):
        grille_cases.append(ligne.copy())
    
    return grille_cases

#test taille_grille_cases
#print (taille_grille_cases(3,3))


def init():
    """Initilalise les joueur et la grille de jeu."""

    global joueurs, lignes, cases, classement, tour, TAILLE_GRILLE

    # Change la taille de la grille
    TAILLE_GRILLE = selection.grille

    # Cree les lignes et les cases
    lignes = cree_grille_lignes(TAILLE_GRILLE)
    cases = cree_grille_cases(TAILLE_GRILLE)

    # Cree les joueurs et le classement.
    joueurs, classement = cree_joueurs_classement(selection.joueurs)

    # Qui commence le jeu
    tour = random.randint(0, len(joueurs)-1)

    # Montre les regles du jeu
    regles_jeu.provenance = etat
    boucle_jeu.set_etat(regles_jeu.etat)


def col_joueur(i:int)->Color:
    """
    Renvoie ls couleur d'un joueur ou celle d'une case vide si il n'existe pas.
    `fore` repesente la couleur des ligne, `back` celle des cases.
    """

    return joueurs[i].couleur if i >= 0 else Color(None, COL_LIGNE, COL_BACK)


def col_rang(i):
    """Renvoie la couleur et le style du texte associe au rang."""

    # Les 3 premiers ont une couleur particulière
    if (i == 1): 
        col_rang = Color([1, 4], 226) # Jaune, souligné
    elif (i == 2): 
        col_rang = Color([1, 4], 231) # Blanc, souligné
    elif (i == 3): 
        col_rang = Color([1, 4], 208) # Orange, souligné
    
    #  Pour les autres, la couleur se rapproche de plus en plus d'un gris sombre + italique
    elif(i-1 < 17):
        col_rang = Color(3, 25-i+4) # blanc de plus en plus sombre, italique

    # Apres un certain rang, la couleur ne change plus
    else:
        col_rang = Color(3, 235) # gris sombre, italique
    
    return col_rang


def col_ligne(l,c) -> int:
    """Renvoie la couleur de la ligne d'un joueur."""
    return col_joueur(lignes[l][c]).fore


def col_case(l, c) -> Color:
    """Renvoie la couleur de la case d'un joueur."""
    # Renvoie une couleur et non un int car une case affiche son numero de case en plus du fond, qui ppeut être de differente couleur.

    # Recupère la couleur du fond
    col = col_joueur(cases[l][c]).back

    # Si la case est vide, renvoie renvoie 2 couleure differente, sinon 2 couleur identiques afin de masquer le texte.
    return Color(None, COL_TEXT, COL_BACK+l%2+c%2) if cases[l][c] == -1 else Color(None, col, col)


def text_case(i:int, j:int) -> list[list[str]]:
    """Renvoie la texture d'une case avec son numero. Inclue tous les bords et coins."""

    # Avec les bords, une case est contitues de liste de 3 elements:
    # [
    #   [coin,    ligne_H, coin   ]
    #   [ligne_V, case,    ligne_V] TAILLE_CASE-1 fois
    #   [coin,    ligne_H, coin   ]
    # ]

    # Crée le milleur de la case
    c = [[LIGNE_V, CASE*(TAILLE_CASE*2-1), LIGNE_V] for _ in range(TAILLE_CASE-1)]

    # Ajoute le haut de la case
    c.insert(0, [POINT, LIGNE_H*(TAILLE_CASE*2-1), POINT])

    # Ajoute le base de la case
    c.append([POINT, LIGNE_H*(TAILLE_CASE*2-1), POINT])

    # Recupere le mileur de la texture 
    m_h, m_v = (TAILLE_CASE*2-1)//2, (TAILLE_CASE)//2

    # Ajoute le numero au milieu de la case
    c[m_v][1] = c[m_v][1][:m_h-1]+str(i)+str(j)+c[m_v][1][m_h+1:]

    return c


def affich_case(l,c):
    """Affiche la cases [l][c] avec ses bords."""

    # Cree la matrice des couleur, avec le meme shema que la fonction `text_case`
    # lignes_V : la couleur dele fond.
    # lignes_H : la couleur de le texte. comme elle fait partie du de la case, son fond est de la couleur de la case
    # case: couleur du fond. 
    # coins : la couleur de la ligne_V est dans le fond, le texte est toujours de la meme couleur

    # Recupere les couleurs utilisés plusieurs fois en dessous
    t = Color(fore=COL_TEXT)
    col_l = Color(back=col_ligne(2*l+1,c))
    col_r = Color(back=col_ligne(2*l+1,c+1))
    back = col_case(l,c)

    # Cree le mileu de la matrice
    col = [[col_l, back, col_r]] * (TAILLE_CASE-1)

    # Ajoute le haut
    col.insert(0, [
        col_l, Color(fore=col_ligne(2*l,c))+back, col_r
    ])

    # Ajoute le bas
    # Si c'est la dernire colone, il n'y a pas de cases en dessous et les points prennent leur couleur par defaut.
    col.append(
        [ # Avec une cases en dessous
            Color(back=col_ligne(2*l+1,c)) + t,
            Color(fore=col_ligne(2*(l+1),c), back=col_case(l-1,c).back),
            Color(back=col_ligne(2*l+1,c+1)) + t
        ] # Sans cases en dessous
        if l < TAILLE_GRILLE-1 else [
            t, Color(fore=col_ligne(2*(l+1),c)), t
        ]
    )
    # Affiche la case et calcule sa position sur l'ecran par rapport an centre.
    console.affiche(
        (console.WIDTH-TAILLE_GRILLE*TAILLE_CASE*2)/2+c*TAILLE_CASE*2,
        (console.HEIGHT-TAILLE_GRILLE*TAILLE_CASE)/2+l*TAILLE_CASE,
        text_case(l,c), col
    )


def affiche_grille():
    """Affiche la grille de jeu."""
    for l in range(TAILLE_GRILLE):
        for c in range(TAILLE_GRILLE):
            affich_case(l,c)
    

def affiche_joueur(i):
    """Affiche un joueur et les infos le concernant."""

    # Crée le rang du joueur
    r = rang_joueur(i)+1
    rang = str(r) + ("er" if r == '1' else "e")

    # Compte le nombre de tour à attendre
    t = (i-tour) % len(joueurs)

    # Determine la couleur et le texte a afficher

    if (t == 0): # Au joueur de jouer
        t = "En jeu"
        col_t = Color(1, 255) # Blanc

    elif (t == 1): # Joue au tour suivant
        t = "Tour suivant"
        col_t = Color([3, 5], 255) # blanc clignotant

    elif (t == 2): # Joue dans 2 tours
        t = "Dans 2 tours"
        col_t = Color(None, 255) # Blanc

    else: # Joue dans plus de 2 tours
        t = f"Dans {t} tours"
        col_t = Color(3, 8) # Blanc sombre italique
    
    # Recupère la couleur du joueur
    col = col_joueur(i)

    # Determine la position a laquelle afficher le joueur

    mid = len(joueurs)//2 # Le nombre de joueur a gauche de la grille de jeu

    x = 2 # Marge sur les bords
    y = 1 # Marge en gaut
    
    if (i < mid): # A gauche
        x = x
        y += i*4
    
    else: # A droite
        x = console.WIDTH-x-LARGEUR_RECT_JOUEUR
        y += (i-mid)*(3+1)
    

    # Affiche le fond
    console.affiche_rect(x, y, LARGEUR_RECT_JOUEUR, 3, ' ', col, (0,0))

    # Affiche son nom et son classement
    console.affiche_str(x, y, LARGEUR_RECT_JOUEUR, joueurs[i].nom, col, (0,0))
    console.affiche_str(x+LARGEUR_RECT_JOUEUR, y, LARGEUR_RECT_JOUEUR,rang, col_rang(r)+col, (1,0))

    # Affiche son score
    console.affiche_str(x+LARGEUR_RECT_JOUEUR/2, y+1, LARGEUR_RECT_JOUEUR, f'{joueurs[i].score} pts', col, (0.5, 0))

    # Affiche le nombre de tous qu'il a à attendre avant de jouer
    # C'est aussi cette zone d'entree qui sera utilisée lorsque le joueur va joueur
    console.affiche_entree(x+LARGEUR_RECT_JOUEUR/2, y+2, LARGEUR_RECT_JOUEUR,i, t, col_t+col, ancre=(0.5, 0))


def affiche_joueurs():
    """Affiche les joueurs."""
    for i in range(len(joueurs)):
        affiche_joueur(i)


def affiche():
    """Affiche l'interface de jeu."""

    # Affiche la grille
    affiche_grille()

    # Affiche les joueurs
    affiche_joueurs()
    



def convertir_position_en_ligne(case, cote) -> tuple[int,int]:
    """
    convertit la position (ex: coor="44", cote='z') en cellule de la matrice,
    renvoie les coordonnées d'une case de la matrice grille_cotes.
    """
    # trouve la ligneet la collone
    i = 1+2*case[0]
    j = case[1]

    # trouvee la ligne autour de la case
    if cote == 'z': # Au dessus
        ligne = i-1, j
    elif cote == 'q': # A gauche
        ligne = i, j
    elif cote == 's': # En bas
        ligne = i+1, j
    elif cote == 'd': # A droite
        ligne = i, j+1

    return ligne


def convertir_ligne_en_cases(ligne) -> tuple:
    """Renvoie les cases adjacentes à une ligne."""

    # Cases adjacentes
    adjs:list = []

    # Recupère la ligne de la case
    l = ligne[0]//2

    # Trouve les coordonnes des cases
    if(ligne[0] %2 == 0): # Ligne horizontale

        # Recupère les cases adj (dessus, dessous)
        for l_off in [-1,0]:
            if(0 <= l+l_off and l+l_off < TAILLE_GRILLE): # Verifie que la case existe
                adjs.append((l+l_off, ligne[1]))
    
    else: # Ligne verticale

        # Recupère les cases adj (gauche et droite)
        for c_off in [-1,0]:
            if(0 <= ligne[1]+c_off and ligne[1]+c_off < TAILLE_GRILLE): # Verifie que la case existe
                adjs.append((l, ligne[1]+c_off))

    return adjs


def ligne_possible(ligne) -> bool:
    """Vérifie si on peut mettre la ligne à l'endroit demandé."""
    return lignes[ligne[0]][ligne[1]] == -1


def mettre_ligne(ligne, joueur) -> int:
    """
    Pose une ligne de la bonne couleur là où le joueur l'a demandé et colorie les cases adj.
    Renvoie le nombre de cases colories.
    """
    global choix_c, choix_l
    # Pose la ligne du joiueur
    lignes[ligne[0]][ligne[1]] = joueur

    # Trouve les cases adj
    cases_adj: list = convertir_ligne_en_cases(choix_l)

    choix_c, choix_l = None, None
    # Essaie de colorie les cases adj
    colorie = 0
    for case in cases_adj:
        if test_case_fermee(case):  # Ne colortie que si la case est fermee
            # Colorie la case
            colorie_case(case)
            colorie =+ 1

    return colorie


def test_case_fermee(case:tuple[int,int]) -> bool:
    """Vérifie si les quatre côtés d'une cellule sont coloriés."""
    return  lignes[case[0]    *2  ][case[1]  ] != -1\
        and lignes[(case[0])  *2+1][case[1]  ] != -1\
        and lignes[(case[0])  *2+1][case[1]+1] != -1\
        and lignes[(case[0]+1)*2  ][case[1]  ] != -1


def colorie_case(case):
    """Colorie la case de la couleur du joueur et ajoute un point au score du joueur."""

    # Remplie la case
    global cases_remplies
    cases_remplies+=1

    # Actualise le score du joueur
    cases[case[0]][case[1]] = tour

    # Actualise le classement du joueur
    joueurs[tour].score += 1
    update_classement(tour)


def test_jeu_fini() -> bool:
    """Test si le jeu est fini."""
    return cases_remplies >= TAILLE_GRILLE**2


def tour_suivant() -> int:
    """Passe le tour au joueur suivant."""

    global tour

    # Passe le tour au joueur suivant
    tour = (tour+1)%len(joueurs)


def dans_grille(x, y) -> bool:
    """Verifie si la case est dans la grille."""
    return 0 <= x and x < TAILLE_GRILLE and 0 <= y and y < TAILLE_GRILLE


def rang_joueur_abs(i:int):
    """
    Renvoie le absolue rang du joueur (aucune egalité possible).
    Si 2 joueur on le même score, celui que y est arrivé en premier est devant.
    """

    # Recupèrer le joueur dans la liste de joueurs
    j = joueurs[i]

    # Rang abs, rang recherché
    rang, r = -1, 0 

    # Recherche le joueur dans le classement
    while (rang == -1 and r < len(classement)):
        if(classement[r] == j): # Test si c'est le bon joueur, si oui recupère son classement
            rang = r
        r+=1
    
    return rang


def rang_joueur(i:int):
    """
    Renvoie le rang du joueur.
    Si 2 joueur on le même score, ils ont le même rang.
    """

    # Part du rang absolu dou joueur
    r = rang_joueur_abs(i)

    # Remonte tous le joueur ayant le même score pour trouver le rang 
    while (r > 0 and classement[r-1].score == classement[r].score):
        r-=1
    
    return r


def update_classement(i):
    """Actualise le classement du joeur `i` si il a gagné des points de score."""

    # Recupère le rang absolu du joueur
    rang = rang_joueur_abs(i)
    r = rang

    # Trouve son nouveau rang (le 1er joueur qui a un classement superieur à lui)
    while (r > 0 and classement[r-1].score < classement[rang].score):
        r -= 1
    
    # Actualise son classement
    classement.insert(r, classement.pop(rang))

# La case et la ligne choisies par le joueur
choix_c:tuple[int,int] = None
choix_l:tuple[int,int] = None


def choix_case():
    """Recupere la case choise par le joueur si elle est valide."""

    global choix_c

    # Recupère la case choisi par le joueur
    # Tant que le joueur n'a pas commence son tour, il peut arreter la partie et demander les regles.
    console.info_entree(tour, "Choisisser votre case")
    entree: str = console.get_entree(tour, "",  "numero | retour").strip().lower()
    if(entree == ''): # Ne fait rien si l'entree est nulle
        ...
    if(entree in ['r', "retour"]): # Reviens au menu de selection des joueurs
        boucle_jeu.set_etat(selection.etat)

    elif(entree in ['c',"comment"]): # Montre les regles du jeu
        regles_jeu.provenance = etat
        boucle_jeu.set_etat(regles_jeu.etat)
    elif(not entree.isdigit() or len(entree) != 2): # N'entre pas un nombre entre 0 et '100'
        console.erreur_entree(tour, "Numéro non valide")

    else:
        # Recupere les coordonnées
        x, y = int(entree[0]), int(entree[1])

        if(not dans_grille(x,y)): # Verifie qu'elles sont dans la grille
            console.erreur_entree(tour, "Numéro hors de la grille")

        elif(test_case_fermee((x,y))): # Verifie que la case est selectionable
            console.erreur_entree(tour, "Cette case est fermée")

        else: # Choisi la case
            choix_c = (x,y)


def choix_ligne():
    """Recupere la ligne choise par le joueur autour de la case si elle est libre."""

    global choix_l

    # Recupère la ligne choisi par le joueur
    console.info_entree(tour, "Choisissez le côté")
    entree: str = console.get_entree(tour, "", "z | q | s | d").strip().lower()
    
    if(entree == ''):  # Ne fait rien si l'entree est nulle
        ...
    if(not entree in ["z", "q", "s", "d"]): # Verifie que le joueur a entré ce qu'il fallait
        console.info_entree(tour, "z | q | s | d")

    else: # Recupre la ligne
        ligne = convertir_position_en_ligne(choix_c, entree)

        if not ligne_possible(ligne): # Verifie que la ligne est possible
            console.erreur_entree(tour, "Ligne déjà prise!")

        else: # Choisi la ligne
            choix_l = ligne

 
def update():
    """Gère les entrées de l'utilisateur, case valide etc."""

    # Determine l'action a réaliser par le joeur
    if(choix_c == None): # Choisir sa case
        choix_case()
    
    elif(choix_l == None):  # Choisir sa ligne
        choix_ligne()

    else: # Pose la ligne du joueur
        colories = mettre_ligne(choix_l, tour)

        # Test la fin du jeu et change le tour
        if(colories == 0):  # Aucune case de fermée
            tour_suivant()
        
        elif test_jeu_fini():  # Regarde si le jeu se termine
            boucle_jeu.set_etat(fin_jeu.etat)
    

etat = boucle_jeu.Etat("Jeu", init, affiche, update)