from etats import jeu, selection
from core.ansi import Color


def cree_grille_cases():
    grille = jeu.cree_grille_cases(3)
    print(*grille, sep = '\n')


def cree_grille_lignes():
    grille = jeu.cree_grille_lignes(3)
    print(*grille, sep='\n')


def cree_joueurs_classement():
    joueurs, _ = jeu.cree_joueurs_classement([
        ("Joueur 1", selection.COULEURS[0]),
        ("Joueur 2", selection.COULEURS[2]),
        ("Joueur 3", selection.COULEURS[8]),
    ])
    print("Joueurs:")
    [print(f"\t{j.nom}, {j.score}pts {j.couleur}CASE{Color.Reset()}") for j in joueurs]
    

def test_cases_fermee():
    jeu.lignes = jeu.cree_grille_lignes(3)
    print(*jeu.lignes, sep="\n")
    print("0,0: ", jeu.test_case_fermee((0,0)))

    jeu.lignes[0][0] = 1
    jeu.lignes[1][0] = 1
    jeu.lignes[2][0] = 1
    jeu.lignes[1][1] = 1

    jeu.lignes[0][1] = 1
    jeu.lignes[1][2] = 1
    jeu.lignes[2][1] = 1
    print(*jeu.lignes, sep="\n")
    print("0,0: ", jeu.test_case_fermee((0, 0)))
    print("1,0: ",jeu.test_case_fermee((1, 0)))
    print("0,1: ",jeu.test_case_fermee((0, 1)))


def dans_grille():
    jeu.TAILLE_GRILLE = 3
    print("TAille de la grile :", jeu.TAILLE_GRILLE)
    print("00 :", jeu.dans_grille(0,0))
    print("95 :", jeu.dans_grille(9,5))
    print("33 :", jeu.dans_grille(3,3))
    print("22 :", jeu.dans_grille(2,2))