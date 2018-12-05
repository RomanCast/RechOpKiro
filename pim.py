#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 16:00:00 2018

@author: clementgrisi
"""

#%% PIM

import numpy as np
import csv

# LECTURE FICHIERS

dist_p = open('pim/distances.csv', 'r')
nodes_p = open('pim/nodes.csv', 'r')


# PARSING NODES

node_list_pim = [] # liste des noeuds sour la forme [ [x, y, 'type'], ...]

with open('pim/nodes.csv', 'r') as nodes_pim:
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

def takeFirst(elem):
    return elem[0]

test1 = [ [[] for x in range(nbnode_pim)] for y in range(nbnode_pim)]

for i in range(nbnode_pim):
    for j in range(nbnode_pim):
        test1[i][j] = [DistancesPim[i][j], j]
    test1[i] = sorted(test1[i], key=takeFirst)

test2 = [ [0 for x in range(nbnode_pim)] for y in range(nbnode_pim)]

for i in range(nbnode_pim):
    for j in range(nbnode_pim):
        test2[i][j]=test1[i][j][1]

node_list_pim_sorted = [ [(0,'rien') for x in range(nbnode_pim)] for y in range(nbnode_pim)]
for i in range(nbnode_pim):
    for j in range(nbnode_pim):
        node_list_pim_sorted[i][j]=(test2[i][j], node_list_pim[test2[i][j]][2])

#%% CONTRUCTION ARCHITECTURE D'UNE SOLUTION REALISABLE

def insert_plus_proche(antenne,Reseau):
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
for i in range(nbnode_pim):
    if(node_list_pim[i][2] == 'terminal'):
        nbAntennas += 1

nbDistribution = 0
for i in range(nbnode_pim):
    if(node_list_pim[i][2] == 'distribution'):
        nbDistribution += 1

newDistribution = 0
boucle = [newDistribution]
alreadyVisitedDistribution.append(newDistribution)

newAntenna = 0

while(len(alreadyVisitedAntenna)<nbAntennas and len(alreadyVisitedDistribution)<=nbDistribution):
    instance = 1
    while (( node_list_pim_sorted[newAntenna][instance][0] in alreadyVisitedAntenna or node_list_pim_sorted[newAntenna][instance][1] == 'distribution')):
        instance += 1
    newAntenna = node_list_pim_sorted[newAntenna][instance][0]
    if len(boucle) < 30:
        boucle.append(newAntenna)
        alreadyVisitedAntenna.append(newAntenna)
    else:
        architecture.append([boucle])
        while((newDistribution<=nbDistribution) and (newDistribution in alreadyVisitedDistribution or node_list_pim[newDistribution][2] != 'distribution')):
            newDistribution += 1
        alreadyVisitedDistribution.append(newDistribution)
        newAntenna = newDistribution
        boucle = [newDistribution]

#if(len(boucle)<30):
#    architecture.append([boucle])

while(len(alreadyVisitedAntenna)<nbAntennas):
    instance = 1
    while ((instance<nbnode_pim-1) and ((instance in alreadyVisitedAntenna) or (instance in alreadyVisitedDistribution) or (node_list_pim[instance][1] == 'distribution'))):
        instance += 1
    newAntenna = instance
    alreadyVisitedAntenna.append(newAntenna)
    reseau = architecture[0]
    insert_plus_proche(newAntenna, reseau)
    architecture[0] = reseau


compteur = 0
architectureStr = []
for i in range(nbDistribution):
    architectureStr.append([])
    for j in range(len(architecture[i])):
        architectureStr[i].append([])
        print("\n", end="")
        if j == 0:
            print('b', end="")
            for k in range(len(architecture[i][j])):
                architectureStr[i][j].append(str(architecture[i][j][k]))
                print("",architecture[i][j][k], end="")

        else:
            print('c', end="")
            compteur +=1
            for k in range(len(architecture[i][j])):
                architectureStr[i][j].append(str(architecture[i][j][k]))
                print("",architecture[i][j][k], end="")

print("")
print(compteur, " ", nbnode_pim)

#print(" ".join(architectureStr))
#for k in range(nbDistribution):
#    print('b', " ".join(architectureStr[]))
