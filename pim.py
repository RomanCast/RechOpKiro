#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 16:00:00 2018

@author: clementgrisi
"""

#%% PIM

import numpy as np
import csv
from utils import *

# LECTURE FICHIERS

dist_p = open('pim/distances.csv', 'r')
nodes_p = open('pim/nodes.csv', 'r')


# PARSING NODES

node_list_pim = [] # liste des noeuds sour la forme [ [x, y, 'type'], ...]

with open('pim/nodes.csv', 'r') as nodes_pim: # Lecture du fichier CSV et ajout à la liste des noeuds
    nodes = csv.reader(nodes_pim, delimiter=';')
    next(nodes)
    for row in nodes:
        node_list_pim.append([float(row[0]), float(row[1]), row[2]])

nbnode_pim = len(node_list_pim)

# CREATING DISTANCE MATRIX (DistancesPim)

DistancesPim = np.zeros((nbnode_pim,nbnode_pim))

ligne = 0
for L in dist_p.readlines():
    L.strip()
    i = ligne//nbnode_pim
    j = ligne - nbnode_pim*i
    DistancesPim[i][j] = int(L)
    ligne += 1

#%% CREATING THE LIST OF CLOSEST NODES (node_list_pim_sorted)

# node_list_pim_sorted[i] = liste des noeuds les plus proches du noeud i

def takeFirst(elem): # Ceci est une clé qui nous permet de trier la liste selon les distances, soit la première coordonnée des éléments de la liste
    return elem[0]

test1 = [ [[] for x in range(nbnode_pim)] for y in range(nbnode_pim)]

for i in range(nbnode_pim):
    for j in range(nbnode_pim):
        test1[i][j] = [DistancesPim[i][j], j]
    test1[i] = sorted(test1[i], key=takeFirst) # On construit une matrice d'éléments de taille (1,2) contenant la distance entre i et j, et le numéro j de l'élément. Ensuite, une colonne correspond à la liste triée en fonction de la distance de i aux différents éléments j, la première ligne étant donc toujours l'élément i lui même

test2 = [ [0 for x in range(nbnode_pim)] for y in range(nbnode_pim)]

for i in range(nbnode_pim):
    for j in range(nbnode_pim):
        test2[i][j]=test1[i][j][1] # Ici, on enlève juste la distance des éléments de la matrice précédente pour se retrouver avec une matrice de scalaires (l'élément (i,j) donne le numéro de l'élément étant le j ème plus proche de i )

node_list_pim_sorted = [ [(0,'rien') for x in range(nbnode_pim)] for y in range(nbnode_pim)]
for i in range(nbnode_pim):
    for j in range(nbnode_pim):
        node_list_pim_sorted[i][j]=(test2[i][j], node_list_pim[test2[i][j]][2]) # Enfin, on construit une matrice dont les éléments sont le numéro de l'élément le j eme plus proche de i et le type de point de cet élément ('distribution' ou 'terminal')

#%% CONTRUCTION ARCHITECTURE D'UNE SOLUTION REALISABLE

def insert_plus_proche(antenne, Reseau): # Cette fonction insère dans un réseau (i.e. une boucle et ses chaines) un élément en l'accrochant au plus proche élément et en créant donc une nouvelle chaine ou en complétant une dejà existante
    noeud_proche = Reseau[0][0]
    d_min = DistancesPim[Reseau[0][0]][antenne]
    num_chem = 0
    #print(Reseau[0])
    for x in Reseau[0]:
        if(DistancesPim[x][antenne]<d_min):
            noeud_proche = x
            d_min = DistancesPim[x][antenne]
    for k in range(len(Reseau)-1):
        if(DistancesPim[Reseau[k+1][-1]][antenne]<d_min and len(Reseau[k+1])<5):
            noeud_proche = Reseau[k+1][-1]
            d_min = DistancesPim[Reseau[k+1][-1]][antenne]
            num_chem = k+1
    if(num_chem == 0):
        Reseau.append([noeud_proche, antenne])
    else:
        Reseau[num_chem].append(antenne)

alreadyVisitedAntenna = []
alreadyVisitedDistribution = []
architecture = []
reseau = []

nbAntennas = 0
for i in range(nbnode_pim): # calcul du nombre d'antennes
    if(node_list_pim[i][2] == 'terminal'):
        nbAntennas += 1

nbDistribution = 0
for i in range(nbnode_pim): # calcul du nombre de distribution
    if(node_list_pim[i][2] == 'distribution'):
        nbDistribution += 1

newDistribution = 0
boucle = [newDistribution]
alreadyVisitedDistribution.append(newDistribution) # on garde dans cette liste les distributions déjà visitées

newAntenna = 0

## L'idée de la boucle qui suit est de créer une solution réalisable. L'idée étant qu'elle crée des boucles saturées de 30 éléments en partant du premier élément (une distribution) puis en allant à l'élément le plus près, puis le plus près de celui ci, et ainsi de suite jusqu'à avoir 30 éléments.
while(len(alreadyVisitedAntenna)<nbAntennas and len(alreadyVisitedDistribution)<=nbDistribution):
    instance = 1
    while (( node_list_pim_sorted[newAntenna][instance][0] in alreadyVisitedAntenna or node_list_pim_sorted[newAntenna][instance][1] == 'distribution')):
        instance += 1
    newAntenna = node_list_pim_sorted[newAntenna][instance][0]
    if len(boucle) < 30:
        boucle.append(newAntenna)
        alreadyVisitedAntenna.append(newAntenna)
        if (len(alreadyVisitedAntenna)==nbAntennas):
            architecture.append([boucle])
            for i in range(nbDistribution):
                if i not in alreadyVisitedDistribution:
                    architecture.append([[i]])
            break
    else:
        architecture.append([boucle]) # On possède une liste de liste de liste à laquelle on ajoute les boucles ainsi créées, puis à laquelle on ajoutera les chaines plus tard. Un élément de architecture est un réseau, un élément d'un réseau est une boucle ou une chaine, et un élement d'une boucle ou d'une chaine est une antenne ou une distribution.
        while((newDistribution<=nbDistribution) and (newDistribution in alreadyVisitedDistribution or node_list_pim[newDistribution][2] != 'distribution')):
            newDistribution += 1
        alreadyVisitedDistribution.append(newDistribution)
        boucle = [newDistribution]

while(len(alreadyVisitedAntenna)<nbAntennas):
    instance = 1
    while ((instance<nbnode_pim-1) and ((instance in alreadyVisitedAntenna) or (instance in alreadyVisitedDistribution) or (node_list_pim[instance][1] == 'distribution'))):
        instance += 1
    newAntenna = instance
    alreadyVisitedAntenna.append(newAntenna)
    reseau = architecture[0]
    insert_plus_proche(newAntenna, reseau)
    architecture[0] = reseau


print('cout depart')
print(cout_architecture(architecture, DistancesPim))
# test = descente_rap_architecture(architecture, DistancesPim, 500)
reseau1 = architecture.pop(0)
reseau2 = architecture.pop(0)
reseau3 = architecture.pop(0)
reseau4 = architecture.pop(0)
reseau5 = architecture.pop(0)
reseau6 = architecture.pop(0)
reseau7 = architecture.pop(0)
reseau8 = architecture.pop(0)
reseau9 = architecture.pop(0)
reseau10 = architecture.pop(0)
reseau11 = architecture.pop(0)
test1 = descente_rap_reseau(reseau1, DistancesPim, 1000)
test2 = descente_rap_reseau(reseau2, DistancesPim, 1)
test3 = descente_rap_reseau(reseau3, DistancesPim, 1)
test4 = descente_rap_reseau(reseau4, DistancesPim, 1)
test5 = descente_rap_reseau(reseau5, DistancesPim, 1)
test6 = descente_rap_reseau(reseau6, DistancesPim, 1)
test7 = descente_rap_reseau(reseau7, DistancesPim, 1)
test8 = descente_rap_reseau(reseau8, DistancesPim, 1)
test9 = descente_rap_reseau(reseau9, DistancesPim, 1)
test10 = descente_rap_reseau(reseau10, DistancesPim, 1)
test11 = descente_rap_reseau(reseau11, DistancesPim, 1)
architecture = [test1] + [test2] + [test3] + [test4] + [test5] + [test6] + [test7] + [test8] + [test9] + [test10] + [test11]
print('cout arrivee')
print(cout_architecture(architecture, DistancesPim))

write_solution(architecture, nbDistribution, 'pim')
