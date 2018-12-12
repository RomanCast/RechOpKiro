import numpy as np
import csv
import random as rd

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

# fonctions de louis

def cout_reseau(reseau, distances):
    """prend en entree un reseau de la forme : reseau = [[boucle],[chemin1],...,[cheminkR]]
    et renvoie le cout associe"""
    cout_res = 0
    boucle = reseau [0]
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
        if(distances[chaine_k[-1]][antenne]<d_min and len(chaine_k<5)):
            noeud_proche = chaine_k[-1]
            d_min = distances[noeud_proche][antenne]
            num_chem = k+1
    if(num_chem == 0):
        reseau.append([noeud_proche, antenne])
    else:
        reseau[num_chem].append(antenne)

# OK

def swap_dans_reseau(reseau, distances, i, j, meilleur = True):
    ancien_cout = cout_reseau(reseau, distances)
    boucle = reseau[0]
    if(i in boucle and j in boucle):
        new_boucle = reseau[0]
        index_i = new_boucle.index(i)
        index_j = new_boucle.index(j)
        new_boucle[index_i] = j
        new_boucle[index_j] = i
        new_reseau = new_boucle + [reseau[k] for k in range(1, len(reseau))]
        nouv_cout = cout_reseau(new_reseau, distances)
        if(nouv_cout < ancien_cout):
            reseau = new_reseau
            return(nouv_cout-ancien_cout)
        elif(meilleur == false):
            reseau = new_reseau
            return(nouv_cout-ancien_cout)
    elif(i in boucle):
        new_boucle = reseau[0]
        index_i = new_boucle.index(i)
        new_boucle[index_i] = j
        antennes_a_attacher = [i]
        new_reseau = [new_boucle]
        # OK
        for k in range(len(reseau)-1):
            antennes_a_attacher.extend(reseau[k+1][1:])
        antennes_a_attacher.remove(j)
        for a in antennes_a_attacher:
            insert_plus_proche(a, Nouv_Res, distances)
        nouv_cout = cout_reseau(Nouv_Res, distances)
        if(nouv_cout<ancien_cout):
            reseau = Nouv_Res
            return(nouv_cout-ancien_cout)
        elif(not meilleur):
            reseau = Nouv_Res
            return(nouv_cout-ancien_cout)


def mod_taille_cycle(R,antenne_dans_c,distances, meilleur = True):
     ancien_cout = cout_de_reseau(R,distances)
     Nouv_res = R[::]
     index_ant = R[0].index(antenne_dans_c)
     antenne = Nouv_res[0].pop(index_ant)
     antennes_a_attacher = [antenne]
     for k in range(len(Nouv_res)-1):
         if(Nouv_res[k+1][0] == antenne):
             Nouv_res[k+1].pop(0)
             antennes_fils = Nouv_res.pop(k+1)
             antennes_a_attacher.extend(antennes_fils)
    for ant in antennes_a_attacher:
        insert_plus_proche(ant, Nouv_res)
    nouv_cout = cout_de_reseau(Nouv_res,distances)
    if(nouv_cout<ancien_cout):
        R = Nouv_res
        return(nouv_cout-ancien_cout)
    elif(meilleur == False):
        R = Nouv_res
        return(nouv_cout-ancien_cout)


def descente_rap_cycle(R, distances, nb_swap):
    step = 0
    while(step<nb_swap):
            num1 = rd.randint(0,len(R[0])-1)
            num2 = num1
            while(num1==num2):
                num2 = rd.randint(0,len(R[0])-1)
            swap_dans_reseau(R, distances, R[0][num1], R[0][num2])
            step = step + 1
    print(cout_de_reseau(R,distances))

def descente_rap_res(R, distances, nb_swap):
    step = 0
    while(step<nb_swap):
            num1 = rd.randint(0,len(R[0])-1)
            num2_chaine = rd.randint(1,len(R)-1)
            num2_dans_chaine = rd.randint(0, len(R[num2_chaine])-1)
            swap_dans_reseau(R, distances, R[0][num1], R[num2_chaine][num2_dans_chaine])
            step = step + 1
    print(cout_de_reseau(R,distances))


def swap_entre_deux_res(A,i,j,distances, meilleur = True):
    ancien_cout_arch = cout_architecture(A,distances)
    num_chaine = rd.randint(1, len(A[i])-1)
    Nouv_R1 = A[i][::]
    Nouv_R2 = A[j][::]
    antenne_transferer = Nouv_R1[num_chaine].pop(-1)
    insert_plus_proche(antenne_transferer, Nouv_R2)
    nouv_cout_arch = ancien_cout_arch-(cout_de_reseau(A[i], distances)+cout_de_reseau(A[j], distances))+cout_de_reseau(Nouv_R1, distances)+cout_de_reseau(Nouv_R2, distances)
    if(nouv_cout_arch<ancien_cout_arch):
        A[i] = Nouv_R1
        A[j] = Nouv_R2
        return(nouv_cout_arch-ancien_cout_arch)
    elif(meilleur == False):
        A[i] = Nouv_R1
        A[j] = Nouv_R2
        return(nouv_cout_arch-ancien_cout_arch)
