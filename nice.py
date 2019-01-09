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
# new_res.append(descente_rap_reseau(old_res[0], dist_matrix, 100000))
#
# for i in range(1, nb_distribution):
#     new_res.append(descente_rap_reseau(old_res[i], dist_matrix, 100000))
#
# architecture_arrivee = [new_res[k] for k in range(len(new_res))]
#
# print('cout arrivee')
# print(cout_architecture(architecture_arrivee, dist_matrix))


#%% descente dans architecture

# architecture_depart = read_solution('nice')
# #print(architecture_depart)
# print('cout depart')
# print(cout_architecture(architecture_depart, dist_matrix))
# architecture_arrivee = descente_rap_architecture(architecture_depart, dist_matrix, 10000)
# print('cout arrivee')
# print(cout_architecture(architecture_arrivee, dist_matrix))
# #print(architecture_arrivee)


#%% recuit simule dans architecture

print('début recuit simulé')
architecture_depart = read_solution('nice')
print('cout depart')
print(cout_architecture(architecture_depart, dist_matrix))
architecture_arrivee = recuit_simule_architecture(architecture_depart, dist_matrix, nb_it = 10000, k=15, Tinit=2000)
print('cout arrivee')
print(cout_architecture(architecture_arrivee, dist_matrix))

#write_solution(architecture_arrivee, nb_distribution, 'nice')

# dep = [[[0, 2, 3, 5], [2, 6, 8]], [[1, 7, 9], [7, 11, 12]]]
# print('dep_architecture = {}'.format(dep))
# temp = insert_plus_proche_dans_architecture(4, dep, dist_matrix)
# fin = insert_plus_proche_dans_architecture(10, temp, dist_matrix)
# print('fin_architecture = {}'.format(fin))

print('')
print(architecture_depart)
print('')
print(architecture_arrivee)
