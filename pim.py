#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 16:00:00 2018

@author: clementgrisi
"""

#%% PIM

from utils import *
from dumb import *

we_are_dumb = False
dist_matrix = DistMatrix('pim')
nb_distribution = nbDistribution('pim')

if (we_are_dumb):
    dumb_architecture = dumb_solution('pim')

##


# print('cout depart')
# print(cout_architecture(architecture, dist_matrix))
# # test = descente_rap_architecture(architecture, dist_matrix, 500)
# reseau1 = architecture.pop(0)
# reseau2 = architecture.pop(0)
# reseau3 = architecture.pop(0)
# reseau4 = architecture.pop(0)
# reseau5 = architecture.pop(0)
# reseau6 = architecture.pop(0)
# reseau7 = architecture.pop(0)
# reseau8 = architecture.pop(0)
# reseau9 = architecture.pop(0)
# reseau10 = architecture.pop(0)
# reseau11 = architecture.pop(0)
# test1 = descente_rap_reseau(reseau1, dist_matrix, 10000)
# test2 = descente_rap_boucle(reseau2, dist_matrix, 10000)
# test3 = descente_rap_boucle(reseau3, dist_matrix, 10000)
# test4 = descente_rap_boucle(reseau4, dist_matrix, 10000)
# test5 = descente_rap_boucle(reseau5, dist_matrix, 10000)
# test6 = descente_rap_boucle(reseau6, dist_matrix, 10000)
# test7 = descente_rap_boucle(reseau7, dist_matrix, 10000)
# test8 = descente_rap_boucle(reseau8, dist_matrix, 10000)
# test9 = descente_rap_boucle(reseau9, dist_matrix, 10000)
# test10 = descente_rap_boucle(reseau10, dist_matrix, 10000)
# test11 = descente_rap_boucle(reseau11, dist_matrix, 10000)
# architecture = [test1] + [test2] + [test3] + [test4] + [test5] + [test6] + [test7] + [test8] + [test9] + [test10] + [test11]
# print('cout arrivee')
# print(cout_architecture(architecture, dist_matrix))
#
# write_solution(architecture, nb_distribution, 'pim')

old_res = []
new_res = []
architecture_depart = read_solution('pim')
print('cout depart')
print(cout_architecture(architecture_depart, dist_matrix))

for i in range(nb_distribution):
    old_res.append(architecture_depart.pop(0))

new_res.append(descente_rap_reseau(old_res[0], dist_matrix, 100))

for i in range(1, nb_distribution):
    new_res.append(descente_rap_boucle(old_res[i], dist_matrix, 100))

architecture_arrivee = [new_res[k] for k in range(len(new_res))]

# reseau1 = architecture_depart.pop(0)
# reseau2 = architecture_depart.pop(0)
# reseau3 = architecture_depart.pop(0)
# reseau4 = architecture_depart.pop(0)
# reseau5 = architecture_depart.pop(0)
# reseau6 = architecture_depart.pop(0)
# reseau7 = architecture_depart.pop(0)
# reseau8 = architecture_depart.pop(0)
# reseau9 = architecture_depart.pop(0)
# reseau10 = architecture_depart.pop(0)
# reseau11 = architecture_depart.pop(0)
# test1 = descente_rap_reseau(reseau1, dist_matrix, 1000)
# test2 = descente_rap_boucle(reseau2, dist_matrix, 1000)
# test3 = descente_rap_boucle(reseau3, dist_matrix, 1000)
# test4 = descente_rap_boucle(reseau4, dist_matrix, 1000)
# test5 = descente_rap_boucle(reseau5, dist_matrix, 1000)
# test6 = descente_rap_boucle(reseau6, dist_matrix, 1000)
# test7 = descente_rap_boucle(reseau7, dist_matrix, 1000)
# test8 = descente_rap_boucle(reseau8, dist_matrix, 1000)
# test9 = descente_rap_boucle(reseau9, dist_matrix, 1000)
# test10 = descente_rap_boucle(reseau10, dist_matrix, 1000)
# test11 = descente_rap_boucle(reseau11, dist_matrix, 1000)
# architecture_arrivee = [test1] + [test2] + [test3] + [test4] + [test5] + [test6] + [test7] + [test8] + [test9] + [test10] + [test11]
print('cout arrivee')
print(cout_architecture(architecture_arrivee, dist_matrix))

write_solution(architecture_arrivee, nb_distribution, 'pim')
