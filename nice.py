#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 15:57:56 2018

@author: clementgrisi
"""
#%% NICE

from utils import *
from dumb import *

dist_matrix = DistMatrix('nice')
nb_distribution = nbDistribution('nice')

dumb_architecture = dumb_solution('nice')
print(dumb_architecture)

##

old_res = []
new_res = []
architecture_depart = read_solution('nice')
print('cout depart')
print(cout_architecture(architecture_depart, dist_matrix))

for i in range(nb_distribution):
    old_res.append(architecture_depart.pop(0))

new_res.append(descente_rap_reseau(old_res[0], dist_matrix, 10000))

for i in range(1, nb_distribution):
    new_res.append(descente_rap_boucle(old_res[i], dist_matrix, 10000))

architecture_arrivee = [new_res[k] for k in range(len(new_res))]

# reseau1 = architecture_depart.pop(0)
# reseau2 = architecture_depart.pop(0)
# reseau3 = architecture_depart.pop(0)
# test1 = descente_rap_boucle(reseau1, dist_matrix, 100000)
# test2 = descente_rap_boucle(reseau2, dist_matrix, 100000)
# test3 = descente_rap_boucle(reseau3, dist_matrix, 100000)
# architecture_arrivee = [test1] + [test2] + [test3]

print('cout arrivee')
print(cout_architecture(architecture_arrivee, dist_matrix))

# write_solution(architecture_arrivee, nb_distribution, 'nice')
