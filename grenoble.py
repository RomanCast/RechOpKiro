#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 15:57:56 2018

@author: clementgrisi
"""

from utils import *
from dumb import *

dist_matrix = DistMatrix('grenoble')
nb_distribution = nbDistribution('grenoble')

dumb_architecture = dumb_solution('grenoble')
print(dumb_architecture)

##

architecture_depart = read_solution('grenoble')
reseau_depart = architecture_depart.pop(0)
print(reseau_depart)
print('cout depart')
print(cout_reseau(reseau_depart, dist_matrix)) #2221
reseau_arrivee = descente_rap_boucle(reseau_depart, dist_matrix, 1000)
print('cout arrivee')
print(cout_reseau(reseau_arrivee, dist_matrix))
print(reseau_arrivee)

architecture_arrivee = [reseau_arrivee] + architecture_depart

#write_solution(architecture_arrivee, nb_distribution, 'grenoble')
