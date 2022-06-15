from enum import Enum


class Teletel(Enum):
    """
    constantes des touches de fonction du Minitel
    en mode Vidéotex ou Mixte
    """

    ENVOI = 1
    RETOUR = 2
    REPETITION = 3
    GUIDE = 4
    ANNULATION = 5
    SOMMAIRE = 6
    CORRECTION = 7
    SUITE = 8
    CONNEXION_FIN = 9