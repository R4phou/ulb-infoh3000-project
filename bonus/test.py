# Liste de sous-listes de 4 éléments
lst = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]

# Récupération des listes résultantes en une seule ligne avec une compréhension de liste
lst1, lst2, lst3, lst4 = [sublst[0] for sublst in lst], [sublst[1] for sublst in lst], [
    sublst[2] for sublst in lst], [sublst[3] for sublst in lst]

# Affichage des listes résultantes
print(lst1)
print(lst2)
print(lst3)
print(lst4)
