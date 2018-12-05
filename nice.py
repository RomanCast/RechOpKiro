#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 15:57:56 2018

@author: clementgrisi
"""
#%% NICE

import numpy as np
import csv

# LECTURE FICHIERS

dist_n = open('nice/distances.csv', 'r')
nodes_n = open('nice/nodes.csv', 'r')


# PARSING NODES

node_list_nice = [] # liste des noeuds sour la forme [ [x, y, 'type'], ...]

with open('nice/nodes.csv', 'r') as nodes_nice:
    nodes = csv.reader(nodes_nice, delimiter=';')
    next(nodes)
    for row in nodes:
        node_list_nice.append([float(row[0]), float(row[1]), row[2]])

nbnode_nice = len(node_list_nice)

# CREATING DISTANCE MATRIX (DistancesNice)

DistancesNice = np.zeros((nbnode_nice,nbnode_nice))

ligne = 0
for L in dist_n.readlines():
    L.strip()
    i = ligne//nbnode_nice
    j = ligne - nbnode_nice*i
    DistancesNice[i][j] = int(L)
    ligne += 1

#%% CREATING THE LIST OF CLOSEST NODES (node_list_nice_sorted)

# node_list_nice_sorted[i] = liste des noeuds les plus proches du noeud i

def takeFirst(elem):
    return elem[0]

test1 = [ [[] for x in range(nbnode_nice)] for y in range(nbnode_nice)]

for i in range(nbnode_nice):
    for j in range(nbnode_nice):
        test1[i][j] = [DistancesNice[i][j], j]
    test1[i] = sorted(test1[i], key=takeFirst)

test2 = [ [0 for x in range(nbnode_nice)] for y in range(nbnode_nice)]

for i in range(nbnode_nice):
    for j in range(nbnode_nice):
        test2[i][j]=test1[i][j][1]

node_list_nice_sorted = [ [(0,'rien') for x in range(nbnode_nice)] for y in range(nbnode_nice)]
for i in range(nbnode_nice):
    for j in range(nbnode_nice):
        node_list_nice_sorted[i][j]=(test2[i][j], node_list_nice[test2[i][j]][2])

#%% CREATION SOLUTION REALISABLE

def insert_plus_proche(antenne,Reseau):
    noeud_proche = Reseau[0][0]
    d_min = DistancesNice[Reseau[0][0]][antenne]
    num_chem = 0
    #print(Reseau[0])
    for x in Reseau[0]:
        if(DistancesNice[x][antenne]<d_min):
            noeud_proche = x
            d_min = DistancesNice[x][antenne]
    for k in range(len(Reseau)-1):
        if(DistancesNice[Reseau[k+1][-1]][antenne]<d_min and len(Reseau[k+1])<5):
            noeud_proche = Reseau[k+1][-1]
            d_min = DistancesNice[Reseau[k+1][-1]][antenne]
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
for i in range(nbnode_nice):
    if(node_list_nice[i][2] == 'terminal'):
        nbAntennas += 1

nbDistribution = 0
for i in range(nbnode_nice):
    if(node_list_nice[i][2] == 'distribution'):
        nbDistribution += 1

newDistribution = 0
newAntenna = 0

boucle = [newDistribution]
alreadyVisitedDistribution.append(newDistribution)


while(len(alreadyVisitedAntenna)<nbAntennas and len(alreadyVisitedDistribution)<=nbDistribution):
    instance = 1
    while (( node_list_nice_sorted[newAntenna][instance][0] in alreadyVisitedAntenna or node_list_nice_sorted[newAntenna][instance][1] == 'distribution')):
        instance += 1
    newAntenna = node_list_nice_sorted[newAntenna][instance][0]
    if len(boucle) < 30:
        boucle.append(newAntenna)
        alreadyVisitedAntenna.append(newAntenna)
    else:
        architecture.append([boucle])
        while(newDistribution in alreadyVisitedDistribution or node_list_nice[newDistribution][2] != 'distribution'):
            newDistribution += 1
        alreadyVisitedDistribution.append(newDistribution)
        newAntenna = newDistribution
        boucle = [newDistribution]

if(len(boucle)<30):
    architecture.append([boucle])

while(len(alreadyVisitedAntenna)<nbAntennas):
    instance = 1
    while (node_list_nice[instance][0] in alreadyVisitedAntenna or node_list_nice[instance][1] == 'distribution'):
        instance += 1
    newAntenna = instance
    alreadyVisitedAntenna.append(newAntenna)
    reseau = architecture[0]
    insert_plus_proche(newAntenna, reseau)
    architecture[0] = reseau

print(architecture)