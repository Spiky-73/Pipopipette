"""
Permt de teste les fonction des differents etats.

Creez des tests dans differents fichiers sous forme de fonctions sans arguments dans /tests.

Pour appeller un ou plusieur test, assigner a `TEST` la fonction ou liste de fonctions.
Pour tester un ou plusieurs modules, assigner à `TEST` un module ou une liste de module.
"""

import inspect
import os

from tests import jeu

TEST:list = jeu
"""
Le module ou la fonction a tester.

Utilisez une liste pour tester plusieurs modules ou fonctions à la fois.
"""


def test(a_tester):
    """Test les fonctions d'un module ou une fontion

    Args:
        a_tester : Le module on la fonction a tester
    """

    if(inspect.ismodule(a_tester)): # Lance tous les test d'un module

        # Affiche le nom du module
        print("--------------- module "+a_tester.__name__+" ---------------")

        # Lance tous les test d'un module
        for f in inspect.getmembers(a_tester, inspect.isfunction):
            test(f[1])
        print()

    elif(inspect.isfunction(a_tester)): # Lance le test

        # Affiche le nom test
        print("fonction " + a_tester.__name__+":")

        # Lance le test
        a_tester()
        print()
    

if __name__ == "__main__":
    # Permet la reconnaisance des codes ANSI
    os.system("")
    if(type(TEST) is list): # Lance tous les test de la liste
        for e in TEST: test(e)

    else: # Lance le test individuel
        test(TEST)

    # Message de fin
    print("Tests finis !")