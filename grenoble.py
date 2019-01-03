#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 15:57:56 2018

@author: clementgrisi
"""

from utils import *
from dumb import *

we_are_dumb = True
dist_matrix = DistMatrix('grenoble')
nb_distribution = nbDistribution('grenoble')

if (we_are_dumb):
    dumb_architecture = dumb_solution('grenoble')

##

#%% descente dans reseau

# old_res = []
# new_res = []
# architecture_depart = read_solution('grenoble')
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

print('début descente dans architecture')
architecture_depart = read_solution('grenoble')
print('cout depart')
print(cout_architecture(architecture_depart, dist_matrix))
architecture_arrivee = descente_rap_architecture(architecture_depart, dist_matrix, 100000)
print('cout arrivee')
print(cout_architecture(architecture_arrivee, dist_matrix))

#%% recuit simule dans architecture

# print('début recuit simulé')
# architecture_depart = dumb_architecture
# print('cout depart')
# print(cout_architecture(architecture_depart, dist_matrix))
# architecture_arrivee = recuit_simule_architecture(architecture_depart, dist_matrix, nb_it = 100000, k=5, Tinit=2000)
# print('cout arrivee')
# print(cout_architecture(architecture_arrivee, dist_matrix))


# write_solution(architecture_arrivee, nb_distribution, 'grenoble')
