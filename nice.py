#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 15:57:56 2018

@author: clementgrisi
"""
#%% NICE

from utils import *
from dumb import *

we_are_dumb = False
dist_matrix = DistMatrix('nice')
nb_distribution = nbDistribution('nice')

if (we_are_dumb):
    dumb_architecture = dumb_solution('nice')

##

#%% descente dans reseau

# old_res = []
# new_res = []
# architecture_depart = read_solution('nice')
# print('cout depart')
# print(cout_architecture(architecture_depart, dist_matrix))
#
# for i in range(nb_distribution):
#     old_res.append(architecture_depart.pop(0))
#
# new_res.append(descente_rap_reseau(old_res[0], dist_matrix, 10000))
#
# for i in range(1, nb_distribution):
#     new_res.append(descente_rap_reseau(old_res[i], dist_matrix, 10000))
#
# architecture_arrivee = [new_res[k] for k in range(len(new_res))]
#
# print('cout arrivee')
# print(cout_architecture(architecture_arrivee, dist_matrix))


#%% descente dans architecture

architecture_depart = read_solution('nice')
#print(architecture_depart)
print('cout depart')
print(cout_architecture(architecture_depart, dist_matrix))
architecture_arrivee = descente_rap_architecture(architecture_depart, dist_matrix, 10000)
print('cout arrivee')
print(cout_architecture(architecture_arrivee, dist_matrix))
#print(architecture_arrivee)

write_solution(architecture_arrivee, nb_distribution, 'nice')
