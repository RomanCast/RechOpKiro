# RechOpKiro

fichier dumb.py : 
regroupe le code permettant de calculer une solution admissible "débile"
on en a plus besoin maintenant

fichier utils.py : 
regroupe un certain nombre de fonction génériques à utiliser pour chaque ville :
- write solution : permet d'écrire une solution dans une fichier texte au bon format
- read solution : permet de construire l'architecture associée à une solution écrite dans un fichier texte 
- différentes fonctions de descentes locales (dans une boucle, dans un reseau, dans une architecture)

fichier grenoble.py (ou nice.py, ou pim.py) : regroupe le code a lancer dans le terminal
1) calcul d'une solution admissible "débile" avec dumb_solution('grenoble') (inutile maintenant)
2) lecture de la derniere solution enregistrée (read_solution('grenoble')) ; 
3) descente locale sur cette solution ; 
4) enregistrement de la nouvelle solution dans le fichier texte (write_solution)
