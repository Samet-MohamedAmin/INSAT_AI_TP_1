from unification.expression import Expression
from unification.display import *


## Declaration des Classes Regle et Fait 
class Regle:
    def __init__(self, id=0, premisse=[], conclusion=[], etat=True):
        self.premisse = premisse
        self.conclusion = conclusion
        self.id = id
        self.etat = etat


class Fait:
    def __init__(self, name, id=-1):
        self.id_regle = id
        self.name = name


# retourner true si l'instance n'est pas dans la base des faits
def conclusion_not_exist(instance, BF):
    for x in BF:
        if x.name == instance:
            return False
    return True


# retourner la conclusion apres l'unification
def conclure(unification, conclusion):
    for key, value in unification:
        conclusion = conclusion.replace(key, value)
    return conclusion


def test_but(base_faits=[], but=""):
    if not but: return False
    but = but.lower()
    for fait in base_faits:
        if fait.name.lower() == but:
            return True
    return False


def ajout_conclusion(conclusion, unification, base_faits, bf_new, but=""):
    result = conclure(unification, conclusion)
    if conclusion_not_exist(result, base_faits):
        fait = Fait(result, -1)
        base_faits.append(fait)
        bf_new.append(fait)
        if test_but(base_faits, but):
            return True


# Chainage Avant avec but Sans Conflit (moteur d'ordre 1)
def chainage_avant_sans_conflit(base_faits, base_regles, but=""):
    if test_but(base_faits, but): return True
    while True:
        bf_new = []
        for regle in base_regles:
            for fait in base_faits:
                unification = mgu(Expression(regle.premisse[0]), Expression(fait.name))
                if unification:
                    for conclusion in regle.conclusion:
                        if ajout_conclusion(conclusion, unification, base_faits, bf_new, but):
                            return True
        if not bf_new:
            return False
    return False