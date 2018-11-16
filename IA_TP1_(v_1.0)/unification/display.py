from unification.unification import *

def mgu(exp1, exp2):
    d = unifier(exp1, exp2)
    if d is None or len(d) == 0:
        return False
    return d
