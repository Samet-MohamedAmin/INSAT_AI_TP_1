import json
from chainage_avant import *


class Test():
    def __init__(self,
                 file_faits='./base_1/bf_1.json',
                 file_regles='./base_1/br_1.json',
                 but='enfant(Oumeima,Ahmed)'):
        regles_declenchees = []

        with open(file_faits) as json_data:
            faits_liste = json.load(json_data)

        with open(file_regles) as json_data:
            regles_liste = json.load(json_data)

        self.base_regles = [Regle(i, x['premisse'], x['conclusion']) for i, x in enumerate(regles_liste)]
        self.base_faits = [Fait(f, -1) for faits in faits_liste for f in faits ]
        self.but = but

        self.bf_new_file = 'bf.json'

    def do_test(self):
        if self.but:
            if chainage_avant_sans_conflit(self.base_faits, self.base_regles, self.but):
                return 'goal "%s" was found' %self.but
            else:
                return 'goal "%s" was NOT found' %self.but
        else:
            chainage_avant_sans_conflit(self.base_faits, self.base_regles)
            bf_data_new = [x.name for x in self.base_faits]
            with open(self.bf_new_file, 'w') as bf_file:
                json.dump(bf_data_new, bf_file)
            return 'you can find the new bf in: %s' %self.bf_new_file
