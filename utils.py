import numpy as np
import csv
import re
import random as rd
import copy

# fonction ecrivant automatiquement une solution dans un fichier .txt
def write_solution(architecture, nbDistribution, ville):
    file = 'solutions/' + ville + '.txt'
    solution = open(file, 'w+')
    solution.truncate(0)
    for i in range(nbDistribution):
        for j in range(len(architecture[i])):
            if (j==0):
                solution.write('b')
                for k in range(len(architecture[i][j])):
                    solution.write(' ' + '%d' %architecture[i][j][k])
                solution.write("\n")

            else:
                solution.write('c')
                for k in range(len(architecture[i][j])):
                    solution.write(' ' + '%d' %architecture[i][j][k])
                solution.write("\n")

# fonction qui lit un fichier solution pour en faire une architecture2
def read_solution(ville):
    file = 'solutions/' + ville + '.txt'
    solution = open(file, 'r')
    nbDistribution = 0

    for row in solution:
        if (row[0] == 'b'):
            nbDistribution += 1

    nb_chaines = [0]*nbDistribution
    architecture = []
    reseau = []
    boucles = [[]]*nbDistribution
    chaines = [[]]*nbDistribution

    solution = open(file, 'r')
    rows = [row.rstrip('\n') for row in solution]
    j = -1
    for row in rows:
        if (row[0] == 'b'):
            k = 1
            i = rows.index(row)
            j = j+1
            while(i+k<len(rows) and rows[i+k][0] == 'c'):
                k=k+1
                nb_chaines[j]+=1

    print(nb_chaines)

    for i in range(nbDistribution):
        chaines[i] = [[]]*nb_chaines[i]

    solution = open(file, 'r')
    count_b = 0
    old_b = 0
    count_c = 0
    boucle = []
    temp = []

    for row in solution:
        row = row.rstrip('\n')
        for antenne in re.split(' ', row[2:]):
            if (row[0] == 'b'):
                boucle.append(int(antenne))
            elif (row[0] == 'c'):
                temp.append(int(antenne))
        if (count_b<nbDistribution):
            boucles[count_b] = [boucle[k] for k in range(len(boucle))]
        if (count_c < len(chaines[old_b])):
            chaines[old_b][count_c] = [temp[k] for k in range(len(temp))]
        temp = []
        boucle = []
        if (row[0] == 'b'):
            old_b = count_b
            count_b = count_b + 1
            count_c = 0
        elif (row[0] == 'c'):
            count_c += 1

    for i in range(len(boucles)):
        reseau.append(boucles[i])
        for k in range(nb_chaines[i]):
            reseau.append(chaines[i][k])
        architecture.append(reseau)
        reseau = []

    return(architecture)


# fonctions de louis

def cout_reseau(reseau, distances):
    """prend en entree un reseau de la forme : reseau = [[boucle],[chemin1],...,[cheminkR]]
    et renvoie le cout associe"""
    cout_res = 0
    boucle = reseau[0]
    for k in range(len(boucle)-1):
        cout_res = cout_res + distances[boucle[k]][boucle[k+1]]
    cout_res = cout_res + distances[boucle[-1]][boucle[0]]
    nb_chaine = len(reseau)-1
    for k in range(nb_chaine):
        chaine_k = reseau[k+1]
        for l in range(len(chaine_k)-1):
            cout_res = cout_res+distances[chaine_k[l]][chaine_k[l+1]]
    return cout_res

# OK

def cout_architecture(architecture, distances):
    cout_arch = 0
    for reseau in architecture:
        cout_arch = cout_arch + cout_reseau(reseau, distances)
    return(cout_arch)

# OK

def insert_plus_proche(antenne, reseau, distances):
    boucle = reseau[0]
    noeud_proche = boucle[0]
    d_min = distances[noeud_proche][antenne]
    num_chem = 0
    for x in boucle:
        if(distances[x][antenne]<d_min):
            noeud_proche = x
            d_min = distances[x][antenne]
    # en sortie de ce for, noeud_proche contient l'element de la boucle le plus proche de l'antenne a inserer
    for k in range(len(reseau)-1):
        chaine_k = reseau[k+1]
        if (chaine_k == []):
            test = 1
        # print('i = {}, j = {}'.format(chaine_k[-1], antenne))
        # print('distance = {}'.format(distances[chaine_k[-1]][antenne]))
        else:
            if(distances[chaine_k[-1]][antenne]<d_min and len(chaine_k)<5):
                noeud_proche = chaine_k[-1]
                d_min = distances[noeud_proche][antenne]
                num_chem = k+1
    if(num_chem == 0):
        reseau.append([noeud_proche, antenne])
    else:
        reseau[num_chem].append(antenne)

# OK

def insert_plus_proche_dans_architecture(antenne, architecture, distances):
    boucle = architecture[0][0]
    noeud_proche = boucle[0]
    d_min = distances[noeud_proche][antenne]
    num_chem = 0
    compteur = 0 # Va nous permettre de savoir dans quel réseau on se trouve
    for reseau in architecture:
        boucle = reseau[0]
        for x in boucle:
            if(distances[x][antenne]<d_min):
                noeud_proche = x
                d_min = distances[x][antenne]
                num_chem = 0 # En gros j'enregistre le numéro de chemin du meilleur noeud, mais si on trouve une meilleure antenne dans une boucle, alors il faut réinitialiser num_chem
                num_res = compteur
        # en sortie de ce for, noeud_proche contient l'element de la boucle le plus proche de l'antenne a inserer
        for k in range(len(reseau)-1):
            chaine_k = reseau[k+1]
            if (chaine_k == []):
                test = 1
            # print('i = {}, j = {}'.format(chaine_k[-1], antenne))
            # print('distance = {}'.format(distances[chaine_k[-1]][antenne]))
            else:
                if(distances[chaine_k[-1]][antenne]<d_min and len(chaine_k)<5):
                    noeud_proche = chaine_k[-1]
                    d_min = distances[noeud_proche][antenne]
                    num_chem = k+1
                    num_res = compteur
        compteur += 1
    if(num_chem == 0):
        architecture[num_res].append([noeud_proche, antenne])
    else:
        architecture[num_res][num_chem].append(antenne)

# swap dans reseau : échange deux éléments d'un reseau
# soit deux éléments de la boucle
# soit un élément de la boucle avec l'élément à la fin d'une chaine

def swap_dans_reseau(reseau, distances, i, j, meilleur = True):
    ancien_cout = cout_reseau(reseau, distances)
    boucle = reseau[0]

    # les antennes i et j sont dans la boucles : simple permutation
    if(i in boucle and j in boucle):
        new_boucle = copy.deepcopy(boucle)
        index_i = new_boucle.index(i)
        index_j = new_boucle.index(j)
        # la dite permutation
        new_boucle[index_i] = j
        new_boucle[index_j] = i
        new_chaines = [reseau[k] for k in range(1, len(reseau))]
        new_reseau = [new_boucle]
        # on rajoute les chaines à la nouvelle boucle
        new_reseau.extend(new_chaines)
        nouv_cout = cout_reseau(new_reseau, distances)
        if(nouv_cout < ancien_cout):
            return(new_reseau)
        else:
            return(reseau)
        # elif(meilleur == False):
        #     reseau = new_reseau
        #     return(nouv_cout-ancien_cout)

    # si seule l'antenne i est dans la boucle, on la swap avec j et on ratache chacune des antennes des chaines ensuite
    elif(i in boucle):
        new_boucle = copy.deepcopy(boucle)
        index_i = new_boucle.index(i)
        new_boucle[index_i] = j
        antennes_a_attacher = [i]
        new_reseau = [new_boucle]
        for k in range(len(reseau)-1):
            chaine_k = reseau[k+1]
            antennes_a_attacher.extend(chaine_k[1:])
        # on supprime j des antennes a attacher car on l'a deja mis dans la boucle
        antennes_a_attacher.remove(j)
        for a in antennes_a_attacher:
            insert_plus_proche(a, new_reseau, distances)
        nouv_cout = cout_reseau(new_reseau, distances)
        if(nouv_cout < ancien_cout):
            return(new_reseau)
        else:
            return(reseau)

    # idem si j est dans la boucle et i dans une chaine
    elif(j in boucle):
        new_boucle = copy.deepcopy(boucle)
        index_j = new_boucle.index(j)
        new_boucle[index_j] = i
        antennes_a_attacher = [j]
        new_reseau = [new_boucle]
        for k in range(len(reseau)-1):
            chaine_k = reseau[k+1]
            antennes_a_attacher.extend(chaine_k[1:])
        # on supprime i des antennes a attacher car on l'a deja mis dans la boucle
        antennes_a_attacher.remove(i)
        for a in antennes_a_attacher:
            insert_plus_proche(a, new_reseau, distances)
        nouv_cout = cout_reseau(new_reseau, distances)
        if(nouv_cout < ancien_cout):
            return(new_reseau)
        else:
            return(reseau)
        # elif(not meilleur):
        #     reseau = Nouv_Res
        #     return(nouv_cout-ancien_cout)

    # dans le cas ou aucune des 2 antenne n'est dans la boucle c'est un peu plus délicat
    # on doit trouver les deux chaines qui contiennent ces antennes
    else:
        new_boucle = copy.deepcopy(boucle)
        new_reseau = [new_boucle]
        antennes_a_attacher = []
        for k in range(len(reseau)-1):
            chaine_k = reseau[k+1]
            if (i in chaine_k):
                ind_chaine_i = k+1
                chaine_i = copy.deepcopy(chaine_k)
            if (j in chaine_k):
                ind_chaine_j = k+1
                chaine_j = copy.deepcopy(chaine_k)
        # on a maintenant indentifié les deux chaines contenant i et j
        # on procède au swap
        index_i = chaine_i.index(i)
        index_j = chaine_j.index(j)
        chaine_i[index_i] = j
        chaine_j[index_j] = i

        for k in range(len(chaine_i[index_i+1:])):
            a = chaine_i.pop()
            antennes_a_attacher.append(a)

        for k in range(len(chaine_j[index_j+1:])):
            a = chaine_j.pop()
            antennes_a_attacher.append(a)

        for k in range(len(reseau)-1):
            if (k+1 != ind_chaine_i and k+1 != ind_chaine_j):
                chaine_k = reseau[k+1]
                new_reseau.append(chaine_k)

        new_reseau.append(chaine_i)
        new_reseau.append(chaine_j)

        for a in antennes_a_attacher:
            insert_plus_proche(a, new_reseau, distances)

        nouv_cout = cout_reseau(new_reseau, distances)

        if(nouv_cout < ancien_cout):
            return(new_reseau)
        else:
            return(reseau)


def mod_taille_boucle(reseau , antenne_dans_c, distances, meilleur = True):
    ancien_cout = cout_reseau(reseau, distances)
    new_boucle = reseau[0]
    index_ant = new_boucle.index(antenne_dans_c)
    antenne = new_boucle.pop(index_ant)
    antennes_a_attacher = [antenne]
    new_reseau = new_boucle + [reseau[k] for k in range(1, len(reseau))]
    for k in range(len(new_reseau)-1):
        chaine_k = new_reseau[k+1]
        if(chaine_k[0] == antenne):
            new_reseau[k+1].pop(0)
            antennes_fils = new_reseau.pop(k+1)
            antennes_a_attacher.extend(antennes_fils)
    for ant in antennes_a_attacher:
        insert_plus_proche(ant, new_reseau, distances)
    nouv_cout = cout_reseau(new_reseau, distances)
    if(nouv_cout < ancien_cout):
        reseau = new_reseau
        return(nouv_cout-ancien_cout)
    elif(meilleur == False):
        reseau = new_reseau
        return(nouv_cout-ancien_cout)


def descente_rap_boucle(reseau, distances, nb_swap):
    step = 0
    boucle = reseau[0]
    temp = copy.deepcopy(reseau)
    ancien_cout = cout_reseau(reseau, distances)
    while(step < nb_swap):
        if (len(boucle)<3):
            break
        index1 = rd.randint(1,len(boucle)-1)
        index2 = rd.randint(1,len(boucle)-1)
        # print('wesh')
        while(index1 == index2):
            index2 = rd.randint(1,len(boucle)-1)
        res = swap_dans_reseau(temp, distances, boucle[index1], boucle[index2])
        nouv_cout = cout_reseau(res, distances)
        if (nouv_cout < ancien_cout):
            temp = res
            ancien_cout = nouv_cout
            step = step + 1
        else:
            step = step + 1
    return(temp)

def descente_rap_reseau(reseau, distances, nb_swap):
    step = 0
    boucle = reseau[0]
    temp = copy.deepcopy(reseau)
    ancien_cout = cout_reseau(reseau, distances)
    if (len(reseau) == 1):
        temp = descente_rap_boucle(reseau, distances, nb_swap)
    else:
        while(step < nb_swap):
            random_chaine_1 = reseau[rd.randint(0,len(reseau)-1)]
            random_chaine_2 = reseau[rd.randint(0,len(reseau)-1)]
            num_dans_chaine_1 = rd.randint(1, len(random_chaine_1)-1)
            num_dans_chaine_2 = rd.randint(1, len(random_chaine_2)-1)
            antenne_i = random_chaine_1[num_dans_chaine_1]
            antenne_j = random_chaine_2[num_dans_chaine_2]
            while (antenne_i == antenne_j):
                random_chaine_2 = reseau[rd.randint(0,len(reseau)-1)]
                num_dans_chaine_2 = rd.randint(1, len(random_chaine_2)-1)
                antenne_j = random_chaine_2[num_dans_chaine_2]
            res = swap_dans_reseau(reseau, distances, antenne_i, antenne_j)
            nouv_cout = cout_reseau(res, distances)
            if (nouv_cout < ancien_cout):
                temp = res
                ancien_cout = nouv_cout
                step = step + 1
            else:
                step = step + 1
    return(temp)


def swap_entre_deux_res(architecture, i, j, distances, meilleur = True):
    ancien_cout_arch = cout_architecture(architecture, distances)
    new_architecture = copy.deepcopy(architecture)
    reseau_i = architecture[i]
    reseau_j = architecture[j]
    boucle_i = reseau_i[0]
    boucle_j = reseau_j[0]

    rd_chaine_i =  reseau_i[rd.randint(0,len(reseau_i)-1)]
    rd_chaine_j =  reseau_j[rd.randint(0,len(reseau_j)-1)]

    if (len(rd_chaine_i)==1 and len(rd_chaine_j)==1):
        antenne_i = rd_chaine_i[0]
        antenne_j = rd_chaine_j[0]
    elif (len(rd_chaine_i)==1):
        antenne_i = rd_chaine_i[0]
        antenne_j = rd_chaine_j[rd.randint(1,len(rd_chaine_j)-1)]
    elif (len(rd_chaine_j)==1):
        antenne_j = rd_chaine_j[0]
        antenne_i = rd_chaine_i[rd.randint(1,len(rd_chaine_i)-1)]
    else:
        antenne_i = rd_chaine_i[rd.randint(1,len(rd_chaine_i)-1)]
        antenne_j = rd_chaine_j[rd.randint(1,len(rd_chaine_j)-1)]

    if(antenne_i in boucle_i and antenne_j in boucle_j):
        new_boucle_i = [reseau_i[0][k] for k in range (len(boucle_i))]
        new_boucle_j = [reseau_j[0][k] for k in range (len(boucle_j))]
        index_i = new_boucle_i.index(antenne_i)
        index_j = new_boucle_j.index(antenne_j)
        new_boucle_i[index_i] = antenne_j
        new_boucle_j[index_j] = antenne_i
        new_chaines_i = [reseau_i[k] for k in range(1, len(reseau_i))]
        new_chaines_j = [reseau_j[k] for k in range(1, len(reseau_j))]
        new_reseau_i = [new_boucle_i]
        new_reseau_j = [new_boucle_j]
        new_reseau_i.extend(new_chaines_i)
        new_reseau_j.extend(new_chaines_j)
        new_architecture[i] = new_reseau_i
        new_architecture[j] = new_reseau_j
        nouv_cout_arch = cout_architecture(new_architecture, distances)
        if(nouv_cout_arch < ancien_cout_arch):
            return(new_architecture)
        else:
            return(architecture)

    elif(antenne_i in boucle_i):
        new_boucle_i = copy.deepcopy(reseau_i[0])
        new_boucle_j = copy.deepcopy(reseau_j[0])
        index_i = new_boucle_i.index(antenne_i)
        new_boucle_i[index_i] = antenne_j
        antennes_a_attacher_i = []
        antennes_a_attacher_j = [antenne_i]
        new_reseau_i = [new_boucle_i]
        new_reseau_j = [new_boucle_j]

        for k in range(len(reseau_i)-1):
            chaine_i_k = reseau_i[k+1]
            antennes_a_attacher_i.extend(chaine_i_k[1:])
        for a in antennes_a_attacher_i:
            insert_plus_proche(a, new_reseau_i, distances)

        for k in range(len(reseau_j)-1):
            chaine_j_k = reseau_j[k+1]
            antennes_a_attacher_j.extend(chaine_j_k[1:])
        antennes_a_attacher_j.remove(antenne_j)
        for a in antennes_a_attacher_j:
            insert_plus_proche(a, new_reseau_j, distances)

        new_architecture[i] = new_reseau_i
        new_architecture[j] = new_reseau_j
        nouv_cout_arch = cout_architecture(new_architecture, distances)
        if(nouv_cout_arch < ancien_cout_arch):
            return(new_architecture)
        else:
            return(architecture)

    elif(antenne_j in boucle_j):
        new_boucle_i = copy.deepcopy(reseau_i[0])
        new_boucle_j = copy.deepcopy(reseau_j[0])
        index_j = new_boucle_j.index(antenne_j)
        new_boucle_j[index_j] = antenne_i
        antennes_a_attacher_j = []
        antennes_a_attacher_i = [antenne_j]
        new_reseau_i = [new_boucle_i]
        new_reseau_j = [new_boucle_j]

        for k in range(len(reseau_j)-1):
            chaine_j_k = reseau_j[k+1]
            antennes_a_attacher_j.extend(chaine_j_k[1:])
        for a in antennes_a_attacher_j:
            insert_plus_proche(a, new_reseau_j, distances)

        for k in range(len(reseau_i)-1):
            chaine_i_k = reseau_i[k+1]
            antennes_a_attacher_i.extend(chaine_i_k[1:])
        antennes_a_attacher_i.remove(antenne_i)
        for a in antennes_a_attacher_i:
            insert_plus_proche(a, new_reseau_i, distances)

        new_architecture[i] = new_reseau_i
        new_architecture[j] = new_reseau_j
        nouv_cout_arch = cout_architecture(new_architecture, distances)
        if(nouv_cout_arch < ancien_cout_arch):
            return(new_architecture)
        else:
            return(architecture)

    else:
        new_boucle_i = copy.deepcopy(reseau_i[0])
        new_boucle_j = copy.deepcopy(reseau_j[0])
        antennes_a_attacher_i = [antenne_j]
        antennes_a_attacher_j = [antenne_i]
        new_reseau_i = [new_boucle_i]
        new_reseau_j = [new_boucle_j]

        for k in range(len(reseau_i)-1):
            chaine_i_k = reseau_i[k+1]
            antennes_a_attacher_i.extend(chaine_i_k[1:])
        antennes_a_attacher_i.remove(antenne_i)
        for a in antennes_a_attacher_i:
            insert_plus_proche(a, new_reseau_i, distances)

        for k in range(len(reseau_j)-1):
            chaine_j_k = reseau_j[k+1]
            antennes_a_attacher_j.extend(chaine_j_k[1:])
        antennes_a_attacher_j.remove(antenne_j)
        for a in antennes_a_attacher_j:
            insert_plus_proche(a, new_reseau_j, distances)

        new_architecture[i] = new_reseau_i
        new_architecture[j] = new_reseau_j
        nouv_cout_arch = cout_architecture(new_architecture, distances)
        if(nouv_cout_arch < ancien_cout_arch):
            return(new_architecture)
        else:
            return(architecture)

    # elif(meilleur == False):

def swap_entre_deux_res2(architecture, i, j, distances, meilleur = True):
    ancien_cout_arch = cout_architecture(architecture, distances)
    new_architecture = copy.deepcopy(architecture)
    reseau_i = architecture[i]
    reseau_j = architecture[j]
    boucle_i = reseau_i[0]
    boucle_j = reseau_j[0]

    rd_chaine_i =  reseau_i[rd.randint(0,len(reseau_i)-1)]
    rd_chaine_j =  reseau_j[rd.randint(0,len(reseau_j)-1)]

    while (len(rd_chaine_i)==1 or len(rd_chaine_j)==1):
        rd_chaine_i =  reseau_i[rd.randint(0,len(reseau_i)-1)]
        rd_chaine_j =  reseau_j[rd.randint(0,len(reseau_j)-1)]

    antenne_i = rd_chaine_i[rd.randint(1,len(rd_chaine_i)-1)]
    antenne_j = rd_chaine_j[rd.randint(1,len(rd_chaine_j)-1)]

    if(antenne_i in boucle_i and antenne_j in boucle_j):
        new_boucle_i = copy.deepcopy(boucle_i)
        new_boucle_j = copy.deepcopy(boucle_j)
        index_i = new_boucle_i.index(antenne_i)
        index_j = new_boucle_j.index(antenne_j)
        new_boucle_i[index_i] = antenne_j
        new_boucle_j[index_j] = antenne_i
        new_chaines_i = [reseau_i[k] for k in range(1, len(reseau_i))]
        new_chaines_j = [reseau_j[k] for k in range(1, len(reseau_j))]
        new_reseau_i = [new_boucle_i]
        new_reseau_j = [new_boucle_j]
        new_reseau_i.extend(new_chaines_i)
        new_reseau_j.extend(new_chaines_j)
        new_architecture[i] = new_reseau_i
        new_architecture[j] = new_reseau_j
        nouv_cout_arch = cout_architecture(new_architecture, distances)
        if(nouv_cout_arch < ancien_cout_arch):
            return(new_architecture)
        else:
            return(architecture)

    elif(antenne_i in boucle_i):
        new_boucle_i = copy.deepcopy(boucle_i)
        new_boucle_j = copy.deepcopy(boucle_j)
        index_i = new_boucle_i.index(antenne_i)
        new_boucle_i[index_i] = antenne_j
        antennes_a_attacher_i = []
        antennes_a_attacher_j = [antenne_i]
        new_reseau_i = [new_boucle_i]
        new_reseau_j = [new_boucle_j]

        for k in range(len(reseau_i)-1):
            chaine_i_k = reseau_i[k+1]
            antennes_a_attacher_i.extend(chaine_i_k[1:])
        for a in antennes_a_attacher_i:
            insert_plus_proche(a, new_reseau_i, distances)

        for k in range(len(reseau_j)-1):
            chaine_j_k = reseau_j[k+1]
            antennes_a_attacher_j.extend(chaine_j_k[1:])
        antennes_a_attacher_j.remove(antenne_j)
        for a in antennes_a_attacher_j:
            insert_plus_proche(a, new_reseau_j, distances)

        new_architecture[i] = new_reseau_i
        new_architecture[j] = new_reseau_j
        nouv_cout_arch = cout_architecture(new_architecture, distances)
        if(nouv_cout_arch < ancien_cout_arch):
            return(new_architecture)
        else:
            return(architecture)

    elif(antenne_j in boucle_j):
        new_boucle_i = copy.deepcopy(reseau_i[0])
        new_boucle_j = copy.deepcopy(reseau_j[0])
        index_j = new_boucle_j.index(antenne_j)
        new_boucle_j[index_j] = antenne_i
        antennes_a_attacher_j = []
        antennes_a_attacher_i = [antenne_j]
        new_reseau_i = [new_boucle_i]
        new_reseau_j = [new_boucle_j]

        for k in range(len(reseau_j)-1):
            chaine_j_k = reseau_j[k+1]
            antennes_a_attacher_j.extend(chaine_j_k[1:])
        for a in antennes_a_attacher_j:
            insert_plus_proche(a, new_reseau_j, distances)

        for k in range(len(reseau_i)-1):
            chaine_i_k = reseau_i[k+1]
            antennes_a_attacher_i.extend(chaine_i_k[1:])
        antennes_a_attacher_i.remove(antenne_i)
        for a in antennes_a_attacher_i:
            insert_plus_proche(a, new_reseau_i, distances)

        new_architecture[i] = new_reseau_i
        new_architecture[j] = new_reseau_j
        nouv_cout_arch = cout_architecture(new_architecture, distances)
        if(nouv_cout_arch < ancien_cout_arch):
            return(new_architecture)
        else:
            return(architecture)

    else:
        new_boucle_i = copy.deepcopy(reseau_i[0])
        new_boucle_j = copy.deepcopy(reseau_j[0])
        antennes_a_attacher_i = [antenne_j]
        antennes_a_attacher_j = [antenne_i]
        new_reseau_i = [new_boucle_i]
        new_reseau_j = [new_boucle_j]

        for k in range(len(reseau_i)-1):
            chaine_i_k = reseau_i[k+1]
            antennes_a_attacher_i.extend(chaine_i_k[1:])
        antennes_a_attacher_i.remove(antenne_i)
        for a in antennes_a_attacher_i:
            insert_plus_proche(a, new_reseau_i, distances)

        for k in range(len(reseau_j)-1):
            chaine_j_k = reseau_j[k+1]
            antennes_a_attacher_j.extend(chaine_j_k[1:])
        antennes_a_attacher_j.remove(antenne_j)
        for a in antennes_a_attacher_j:
            insert_plus_proche(a, new_reseau_j, distances)

        new_architecture[i] = new_reseau_i
        new_architecture[j] = new_reseau_j
        nouv_cout_arch = cout_architecture(new_architecture, distances)
        if(nouv_cout_arch < ancien_cout_arch):
            return(new_architecture)
        else:
            return(architecture)



def descente_rap_architecture(architecture, distances, nb_swap):
    step = 0
    ancien_cout = cout_architecture(architecture, distances)
    temp = copy.deepcopy(architecture)
    while(step < nb_swap):
        indice_reseau_1 = rd.randint(0, len(architecture)-1)
        indice_reseau_2 = rd.randint(0, len(architecture)-1)
        while (indice_reseau_1 == indice_reseau_2):
            indice_reseau_2 = rd.randint(0, len(architecture)-1)
        res = swap_entre_deux_res2(temp, indice_reseau_1, indice_reseau_2, distances)
        nouv_cout = cout_architecture(res, distances)
        if (nouv_cout < ancien_cout):
            temp = res
            ancien_cout = nouv_cout
            step = step + 1
        else:
            step = step + 1
    return(temp)


def recuit_simule_architecture(architecture, distances, nb_it = 1000, k=15, Tinit=1000):
    step = 0
    Temp = Tinit
    ancien_cout = cout_architecture(architecture, distances)
    temp = copy.deepcopy(architecture)
    while(step < nb_it):
        indice_reseau_1 = rd.randint(0, len(architecture)-1)
        indice_reseau_2 = rd.randint(0, len(architecture)-1)
        while (indice_reseau_1 == indice_reseau_2):
            indice_reseau_2 = rd.randint(0, len(architecture)-1)
        res = swap_entre_deux_res2(temp, indice_reseau_1, indice_reseau_2, distances)
        nouv_cout = cout_architecture(res, distances)

        if(step%k == 0):##on fait baisser la temperature
            Temp = Temp*0.9

        ecart = nouv_cout-ancien_cout##on calcule la variation du cout
        if (ecart<0):##si on ameliore
            temp = res
            ancien_cout = nouv_cout
            step = step + 1

        else:
            proba = np.exp(-ecart/Temp)
            if(rd.random()<proba):
                temp = res
                ancien_cout = nouv_cout
                step = step + 1
            else:
                step = step + 1
    return(temp)
