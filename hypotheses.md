# Hypothèses

## Proximité

Pour le calcul de la **proximité**:

- On somme la distance de chaque parcelle achetée avec le batiment le plus proche
- On renvoie 1000/distance totale afin de pouvoir maximiser ce score
- Le 1000 permet de ne pas avoir de nombres trop petits

## Productivité

Pour le calcul de la **productivité**:

- On somme les productivités des terrains achetés

## Compacité

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

La reproduction avec un crossover simple coupe ou un crossover uniforme n'a pas donné de bons résultats. L'alternative à été de répliquer les meilleures solutions puis de les faire muter minimum une fois.

## Mutation

La mutation des solutions consiste à échanger un terrain aléatoire avec un autre choisi également aléatoirement tout en s'assurant de respecter le budget.

# Gravitational Search Algorithm (GSA)
## Principe

Se base sur les lois de gravitation et du mouvement.
On associe à chaque individu d'une population une certaine masse dans un repère (spatio-temporel (en gros comme notre univers)) dans lequel il va évoluer.
à chaque itération, on actualise sa nouvelle masse, ainsi que sa vitesse et direction de déplacement dans le repère.

## Etapes

- identification de l'espace de recherche (espace de travail dans laquelle notre population va évoluer)
- Pour chacun des m individus:
  - initialisation d'un nombre de parcelles random
  - Evaluation des scores de chaque parcelle
  - Actualisation du fitness, best, worst (scores)
  - Calcul de la masse puis de forces d'attraction agissant sur chaque parcelle
  - Calcul de l'accélération et de la vitesse
  - Mise à jour de la position des parcelles
  - boucler de l'étape 3 jusqu'à l'étape précédente sur n itérations (ou jusqu'à ce que le budget soit dépassé)
  - S'assurer que le budget ne dépasse pas le budget max en supprimant un élément s'il dépasse et en en rachetant un s'il est trop faible
  - S'assurer qu'il n'achète pas 2 fois la même parcelle au sein d'un individu en remplaçant le doublon par une parcelle random
- Afficher les m individus optimisés sur la carte (les m individus = frontière de Pareto)

# PROMETHEE
3 critères
- Productivite
- Proximité
- Compacité


Implémentation de PROMETHEE II
- Chargement de la population PARETO optimale
- Chargement des scores de cette population
- Raisonnement en étapes
  - Calcul des préférences monocritères avec des seuils de préférences et d'indifférence
--> dans un premier temps, relation linéaire pour simplifier (peut être bientôt une fonction particulière)
  - Calcul de la somme pondérée des préférences monocritères (poids choisis)
  - Calcul des flux positifs et négatifs
  - Calcul des flux nets
  - Tri croissant des flux nets (car on cherche à minimiser!)
