####################################################################################################
# ! ---------------------------- Cet etat n'est ni utilisé, ni fini ---------------------------- ! #
####################################################################################################

# Il a été remplacé par regles_jeu mais nous avons quand même gardé le fichier #

from core import boucle_jeu, console


def tuto_init():
    ...


def tuto_affiche():

    console.affiche_str(0, 5, "Tutoriel", f"^{console.WIDTH}", color="1")

    console.affiche_str(0, 10, "Placer une case", f"^{console.WIDTH}")
    console.affiche_str(0, 12, "> <numero_de_case> endroit", f"^{console.WIDTH}")
    console.affiche_str(
        0, 14, "les numeros de cases sont ecrits dans les cases", f"^{console.WIDTH}")
    console.affiche_str(0, 14, "endroit est: z pour haut, ", f"^{console.WIDTH}")

    console.affiche(24, 10, ["z(^)", "q(<)", "s(v) ", "d(>)"])


def tuto_update():

    console.affiche_entree(50, 19, "", 5)

    # Revient sur le menu principal
    boucle_jeu.set_etat("Menu")
