#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 15:57:56 2018

@author: clementgrisi
"""
#%% NICE

import numpy as np
import csv
import re
from utils import *

# LECTURE FICHIERS

dist_n = open('nice/distances.csv', 'r')
nodes_n = open('nice/nodes.csv', 'r')


# PARSING NODES

node_list_nice = [] # liste des noeuds sour la forme [ [x, y, 'type'], ...]

with open('nice/nodes.csv', 'r') as nodes_nice: # Lecture du fichier CSV et ajout à la liste des noeuds
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

def takeFirst(elem): # Ceci est une clé qui nous permet de trier la liste selon les distances, soit la première coordonnée des éléments de la liste
    return elem[0]

test1 = [ [[] for x in range(nbnode_nice)] for y in range(nbnode_nice)]

for i in range(nbnode_nice):
    for j in range(nbnode_nice):
        test1[i][j] = [DistancesNice[i][j], j]
    test1[i] = sorted(test1[i], key=takeFirst) # On construit une matrice d'éléments de taille (1,2) contenant la distance entre i et j, et le numéro j de l'élément. Ensuite, une colonne correspond à la liste triée en fonction de la distance de i aux différents éléments j, la première ligne étant donc toujours l'élément i lui même

test2 = [ [0 for x in range(nbnode_nice)] for y in range(nbnode_nice)]

for i in range(nbnode_nice):
    for j in range(nbnode_nice):
        test2[i][j]=test1[i][j][1] # Ici, on enlève juste la distance des éléments de la matrice précédente pour se retrouver avec une matrice de scalaires (l'élément (i,j) donne le numéro de l'élément étant le j ème plus proche de i )

node_list_nice_sorted = [ [(0,'rien') for x in range(nbnode_nice)] for y in range(nbnode_nice)]
for i in range(nbnode_nice):
    for j in range(nbnode_nice):
        node_list_nice_sorted[i][j]=(test2[i][j], node_list_nice[test2[i][j]][2]) # Enfin, on construit une matrice dont les éléments sont le numéro de l'élément le j eme plus proche de i et le type de point de cet élément ('distribution' ou 'terminal')

#%% CREATION SOLUTION REALISABLE

def insert_plus_proche(antenne,Reseau): # Cette fonction insère dans un réseau (i.e. une boucle et ses chaines) un élément en l'accrochant au plus proche élément et en créant donc une nouvelle chaine ou en complétant une dejà existante
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

## L'idée de la boucle qui suit est de créer une solution réalisable. L'idée étant qu'elle crée des boucles saturées de 30 éléments en partant du premier élément (une distribution) puis en allant à l'élément le plus près, puis le plus près de celui ci, et ainsi de suite jusqu'à avoir 30 éléments.
while(len(alreadyVisitedAntenna)<nbAntennas and len(alreadyVisitedDistribution)<=nbDistribution):
    instance = 1
    while (( node_list_nice_sorted[newAntenna][instance][0] in alreadyVisitedAntenna or node_list_nice_sorted[newAntenna][instance][1] == 'distribution')):
        instance += 1
    newAntenna = node_list_nice_sorted[newAntenna][instance][0]
    if len(boucle) < 30:
        boucle.append(newAntenna)
        alreadyVisitedAntenna.append(newAntenna)
        if (len(alreadyVisitedAntenna)==nbAntennas):
            architecture.append([boucle])
            for i in range(nbDistribution):
                if i not in alreadyVisitedDistribution:
                    architecture.append([[i]])
    else:
        architecture.append([boucle]) # On possède une liste de liste de liste à laquelle on ajoute les boucles ainsi créées, puis à laquelle on ajoutera les chaines plus tard. Un élément de architecture est un réseau, un élément d'un réseau est une boucle ou une chaine, et un élement d'une boucle ou d'une chaine est une antenne ou une distribution.
        while(newDistribution in alreadyVisitedDistribution or node_list_nice[newDistribution][2] != 'distribution'):
            newDistribution += 1
        alreadyVisitedDistribution.append(newDistribution)
        boucle = [newDistribution]

while(len(alreadyVisitedAntenna)<nbAntennas):
    instance = 1
    while (node_list_nice[instance][0] in alreadyVisitedAntenna or node_list_nice[instance][1] == 'distribution'):
        instance += 1
    newAntenna = instance
    alreadyVisitedAntenna.append(newAntenna)
    reseau = architecture[0]
    insert_plus_proche(newAntenna, reseau)
    architecture[0] = reseau


arch = [ [[0, 13, 10, 4, 6, 8, 14, 12, 17, 22, 20, 24, 29, 30, 33, 39, 45, 40, 36, 34, 38, 47, 51, 52, 55, 60, 58, 54, 44, 35]], [[1, 32, 31, 27, 23, 16, 19, 21, 25, 57, 43, 41, 46, 59, 62, 61, 63, 64, 67, 66, 65, 26, 28, 42, 48, 49, 50, 53, 56, 37]], [[2, 18, 11, 9, 5, 3, 7, 15]]]
print('cout depart')
print(cout_architecture(arch, DistancesNice))
reseau1 = arch.pop(0)
reseau2 = arch.pop(0)
reseau3 = arch.pop(0)
test1 = descente_rap_reseau(reseau1, DistancesNice, 100)
test2 = descente_rap_reseau(reseau2, DistancesNice, 100)
test3 = descente_rap_reseau(reseau3, DistancesNice, 100)
arch = [test1] + [test2] + [test3]
#architecture = [test1] + [test2] + [test3]
print('cout arrivee')
print(cout_architecture(arch, DistancesNice))

#print(architecture)
#write_solution(arch, nbDistribution, 'nice')
