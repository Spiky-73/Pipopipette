"""
  - Notre Pipopipette possède une interface graphique particulière (disponnible dans le dossier `core`) qui peut generer des bug visuels
si le terninal dans lequel il est excecuté ne supporte pas les codes ANSI. 
Pour une meilleure expérience, lancez le jeu dans une console non intégrée à un logiciel (tel que `cmd` ou `bash`)
ou directement avec python (click droit > ouvrir avec > python).

  - Pour excecuter les tests, lancez le fichier test.py

Merci de votre compréhension. :-)
            - Corentin, Louise et Abdallah

"""

from core import boucle_jeu
from etats import menu


if (__name__ == "__main__"): # Verifié seulement si le programme est lance directement, donc non importé
    boucle_jeu.start("Pipopipette", menu.etat)
