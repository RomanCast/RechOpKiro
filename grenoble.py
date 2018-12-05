#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 15:57:56 2018

@author: clementgrisi
"""
#%% GRENOBLE

import numpy as np
import csv

# LECTURE FICHIERS

dist_G = open('grenoble/distances.csv', 'r')
nodes_G = open('grenoble/nodes.csv', 'r')


# PARSING NODES

node_list_grenoble = [] # liste des noeuds sour la forme [ [x, y, 'type'], ...]

with open('grenoble/nodes.csv', 'r') as nodes_grenoble:
    nodes = csv.reader(nodes_grenoble, delimiter=';')
    next(nodes)
    for row in nodes:
        node_list_grenoble.append([float(row[0]), float(row[1]), row[2]])

nbnode_grenoble = len(node_list_grenoble)

# CREATING DISTANCE MATRIX (DistancesGrenoble)

DistancesGrenoble = np.zeros((nbnode_grenoble,nbnode_grenoble))

ligne = 0
for L in dist_G.readlines():
    L.strip()
    i = ligne//nbnode_grenoble
    j = ligne - nbnode_grenoble*i
    DistancesGrenoble[i][j] = int(L)
    ligne += 1

#%% CREATING THE LIST OF CLOSEST NODES (node_list_grenoble_sorted)

# node_list_grenoble_sorted[i] = liste des noeuds les plus proches du noeud i

def takeFirst(elem):
    return elem[0]

test1 = [ [[] for x in range(nbnode_grenoble)] for y in range(nbnode_grenoble)]

for i in range(nbnode_grenoble):
    for j in range(nbnode_grenoble):
        test1[i][j] = [DistancesGrenoble[i][j], j]
    test1[i] = sorted(test1[i], key=takeFirst)

test2 = [ [0 for x in range(nbnode_grenoble)] for y in range(nbnode_grenoble)]

for i in range(nbnode_grenoble):
    for j in range(nbnode_grenoble):
        test2[i][j]=test1[i][j][1]

node_list_grenoble_sorted = [ [(0,'rien') for x in range(nbnode_grenoble)] for y in range(nbnode_grenoble)]
for i in range(nbnode_grenoble):
    for j in range(nbnode_grenoble):
        node_list_grenoble_sorted[i][j]=(test2[i][j], node_list_grenoble[test2[i][j]][2])

#%% CREATION SOLUTION REALISABLE

def insert_plus_proche(antenne,Reseau):
    noeud_proche = Reseau[0][0]
    d_min = DistancesGrenoble[Reseau[0][0]][antenne]
    num_chem = 0
    #print(Reseau[0])
    for x in Reseau[0]:
        if(DistancesGrenoble[x][antenne]<d_min):
            noeud_proche = x
            d_min = DistancesGrenoble[x][antenne]
    for k in range(len(Reseau)-1):
        if(DistancesGrenoble[Reseau[k+1][-1]][antenne]<d_min and len(Reseau[k+1])<5):
            noeud_proche = Reseau[k+1][-1]
            d_min = DistancesGrenoble[Reseau[k+1][-1]][antenne]
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
for i in range(nbnode_grenoble):
    if(node_list_grenoble[i][2] == 'terminal'):
        nbAntennas += 1

nbDistribution = 0
for i in range(nbnode_grenoble):
    if(node_list_grenoble[i][2] == 'distribution'):
        nbDistribution += 1

newDistribution = 0
boucle = [newDistribution]
alreadyVisitedDistribution.append(newDistribution)

newAntenna = 0

while(len(alreadyVisitedAntenna)<nbAntennas and len(alreadyVisitedDistribution)<=nbDistribution):
    instance = 1
    while (( node_list_grenoble_sorted[newAntenna][instance][0] in alreadyVisitedAntenna or node_list_grenoble_sorted[newAntenna][instance][1] == 'distribution')):
        instance += 1
    newAntenna = node_list_grenoble_sorted[newAntenna][instance][0]
    if len(boucle) < 30:
        boucle.append(newAntenna)
        alreadyVisitedAntenna.append(newAntenna)
        if (len(alreadyVisitedAntenna)==nbAntennas):
            architecture.append([boucle])
            for i in range(nbDistribution):
                if i not in alreadyVisitedDistribution:
                    architecture.append([[i]])
    else:
        architecture.append([boucle])
        while(newDistribution in alreadyVisitedDistribution or node_list_grenoble[newDistribution][2] != 'distribution'):
            newDistribution += 1
        alreadyVisitedDistribution.append(newDistribution)
        newAntenna = newDistribution
        boucle = [newDistribution]


while(len(alreadyVisitedAntenna)<nbAntennas):
    instance = 0
    while (instance in alreadyVisitedAntenna or node_list_grenoble[instance][2] == 'distribution'):
        instance += 1
    newAntenna = instance
    alreadyVisitedAntenna.append(newAntenna)
    reseau = architecture[0]
    insert_plus_proche(newAntenna, reseau)
    architecture[0] = reseau

print(architecture)
