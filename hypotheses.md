# Hypothèses

## Proximité

Pour le calcul de la **proximité**:

- On somme la distance de chaque parcelle achetée avec le batiment le plus proche
- On renvoie 1000/distance totale afin de pouvoir maximiser ce score
- Le 1000 permet de ne pas avoir de nombres trop petits

## Productivité

Pour le calcul de la **productivité**:

- On somme les productivités des terrains achetés

##Compacité
Pour le calcul de la **compacité**:

- On somme la distance entre chaque terrain acheté et on essaye de minimiser
- On renvoie 1000/distance totale entre chaque terrain acheté
- Même raison de multiplication par 1000

# Algorithme génétique

- Génération de population
- Evaluation du score

## Sélection

Sélection par dominance de Pareto:

Pour chaque individu de la population, on calcule le nombre d'individu qui le dominent
(par comparaison avec tous les autres membres de la population) qu'on stocke dans un dictionnaire  
Cf **sort_by_dominance(scores_pop)**

La comparaison entre 2 individus se fait via **if_dominated(ind1, ind2)**:  
-> renvoie vrai si ind2 domine ind1 et false dans les autres cas  
(attention: false peut signifier que ind1 domine ind2 mais dans notre utilisation osef)

Enfin, on sélectionne la moitié des individus qui ont le score le plus bas dans le dictionnaire  
Cf **selection_dominance_Pareto(population, scores_pop)**

## Reproduction
Un crossover uniforme à été utilisé pour la reproduction des solutions. Cela consiste à prendre aléatoirement du parent 1 ou 2.
## Mutation <---
