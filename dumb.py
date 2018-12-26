# CREATE A DUMB ARCHITECTURE SOLUTION

import numpy as np
import csv
import re

# PARSING NODES

def NodeList(ville):
    """
    input :
    1- string = ville : le nom de la ville
    output :
    1- list = node_list : liste des noeuds sour la forme [ [x, y, 'type'], ...]
    """
    node_list = []
    node_path = ville + '/nodes.csv'
    with open(node_path, 'r') as node_file: # Lecture du fichier CSV et ajout à la liste des noeuds
        nodes = csv.reader(node_file, delimiter=';')
        next(nodes)
        for row in nodes:
            node_list.append([float(row[0]), float(row[1]), row[2]])
    return(node_list)


def nbAntennas(ville):
    nb_antennas = 0
    temp = NodeList(ville)
    for i in range(len(temp)):
        if(temp[i][2] == 'terminal'):
            nb_antennas += 1
    return(nb_antennas)

def nbDistribution(ville):
    nb_distribution = 0
    temp = NodeList(ville)
    for i in range(len(temp)):
        if(temp[i][2] == 'distribution'):
            nb_distribution += 1
    return(nb_distribution)


# CREATING DISTANCE MATRIX (DistancesGrenoble)

def DistMatrix(ville):
    """
    input :
    1- string = ville : le nom de la ville
    output :
    1- list = dist_matrix : matrice des distances entre le noeud i et le noeud j
    """
    node_list = NodeList(ville)
    nb_node = len(node_list)
    dist_matrix = np.zeros((nb_node, nb_node))
    ligne = 0
    path = ville + '/distances.csv'
    file = open(path, 'r')
    for row in file.readlines():
        row.strip()
        i = ligne//nb_node
        j = ligne - nb_node*i
        dist_matrix[i][j] = int(row)
        ligne += 1
    return(dist_matrix)

#%% CREATING THE LIST OF CLOSEST NODES (node_list_grenoble_sorted)

# node_list_grenoble_sorted[i] = liste des noeuds les plus proches du noeud i

def takeFirst(elem): # Ceci est une clé qui nous permet de trier la liste selon les distances, soit la première coordonnée des éléments de la liste
    return elem[0]


def NodeListSorted(ville):
    node_list = NodeList(ville)
    nb_node = len(node_list)
    dist_matrix = DistMatrix(ville)
    temp1 = [ [[] for x in range(nb_node)] for y in range(nb_node)]
    for i in range(nb_node):
        for j in range(nb_node):
            temp1[i][j] = [dist_matrix[i][j], j]
        temp1[i] = sorted(temp1[i], key=takeFirst) # On construit une matrice d'éléments de taille (1,2) contenant la distance entre i et j, et le numéro j de l'élément. Ensuite, une colonne correspond à la liste triée en fonction de la distance de i aux différents éléments j, la première ligne étant donc toujours l'élément i lui même
    temp2 = [ [0 for x in range(nb_node)] for y in range(nb_node)]
    for i in range(nb_node):
        for j in range(nb_node):
            temp2[i][j]=temp1[i][j][1] # Ici, on enlève juste la distance des éléments de la matrice précédente pour se retrouver avec une matrice de scalaires (l'élément (i,j) donne le numéro de l'élément étant le j ème plus proche de i )
    node_list_sorted = [ [(0,'rien') for x in range(nb_node)] for y in range(nb_node)]
    for i in range(nb_node):
        for j in range(nb_node):
            node_list_sorted[i][j]=(temp2[i][j], node_list[temp2[i][j]][2]) # Enfin, on construit une matrice dont les éléments sont le numéro de l'élément le j eme plus proche de i et le type de point de cet élément ('distribution' ou 'terminal')
    return(node_list_sorted)


#%% CREATION SOLUTION REALISABLE

def insert_plus_proche(ville, antenne, reseau): # Cette fonction insère dans un réseau (i.e. une boucle et ses chaines) un élément en l'accrochant au plus proche élément et en créant donc une nouvelle chaine ou en complétant une dejà existante
    dist_matrix = DistMatrix(ville)
    noeud_proche = reseau[0][0]
    d_min = dist_matrix[reseau[0][0]][antenne]
    num_chem = 0
    for x in reseau[0]:
        if(dist_matrix[x][antenne]<d_min):
            noeud_proche = x
            d_min = dist_matrix[x][antenne]
    for k in range(len(reseau)-1):
        if(dist_matrix[reseau[k+1][-1]][antenne]<d_min and len(reseau[k+1])<5):
            noeud_proche = reseau[k+1][-1]
            d_min = dist_matrix[reseau[k+1][-1]][antenne]
            num_chem = k+1
    if(num_chem == 0):
        reseau.append([noeud_proche, antenne])
    else:
        reseau[num_chem].append(antenne)

def dumb_solution(ville):
    node_list = NodeList(ville)
    nb_node = len(node_list)
    dist_matrix = DistMatrix(ville)

    alreadyVisitedDistribution = []
    alreadyVisitedAntenna = []
    reseau = []
    architecture = []

    nb_distribution = nbDistribution(ville)
    nb_antennas = nbAntennas(ville)

    newDistribution = 0
    boucle = [newDistribution]
    alreadyVisitedDistribution.append(newDistribution)

    newAntenna = 0
    node_list_sorted = NodeListSorted(ville)

    ## L'idée de la boucle qui suit est de créer une solution réalisable. L'idée étant qu'elle crée des boucles saturées de 30 éléments en partant du premier élément (une distribution) puis en allant à l'élément le plus près, puis le plus près de celui ci, et ainsi de suite jusqu'à avoir 30 éléments.
    while(len(alreadyVisitedAntenna)<nb_antennas and len(alreadyVisitedDistribution)<=nb_distribution):
        instance = 1
        while (( node_list_sorted[newAntenna][instance][0] in alreadyVisitedAntenna or node_list_sorted[newAntenna][instance][1] == 'distribution')):
            instance += 1
        newAntenna = node_list_sorted[newAntenna][instance][0]
        if len(boucle) < 30:
            boucle.append(newAntenna)
            alreadyVisitedAntenna.append(newAntenna)
            if (len(alreadyVisitedAntenna)==nb_antennas):
                architecture.append([boucle])
                for i in range(nb_distribution):
                    if i not in alreadyVisitedDistribution:
                        architecture.append([[i]])
                break
        else:
            architecture.append([boucle]) # On possède une liste de liste de liste à laquelle on ajoute les boucles ainsi créées, puis à laquelle on ajoutera les chaines plus tard. Un élément de architecture est un réseau, un élément d'un réseau est une boucle ou une chaine, et un élement d'une boucle ou d'une chaine est une antenne ou une distribution.
            while((newDistribution<=nb_distribution) and (newDistribution in alreadyVisitedDistribution or node_list[newDistribution][2] != 'distribution')):
                newDistribution += 1
            alreadyVisitedDistribution.append(newDistribution)
            boucle = [newDistribution]

    while(len(alreadyVisitedAntenna)<nb_antennas):
        instance = 1
        while ((instance<nb_node) and ((instance in alreadyVisitedAntenna) or (instance in alreadyVisitedDistribution) or (node_list[instance][1] == 'distribution'))):
            instance += 1
        newAntenna = instance
        alreadyVisitedAntenna.append(newAntenna)
        reseau = architecture[0]
        insert_plus_proche(ville, newAntenna, reseau)
        architecture[0] = reseau

    return(architecture)
