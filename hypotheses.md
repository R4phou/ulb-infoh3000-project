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

# Algorithme génétioque

- Génération de population
- Evaluation du score
- Sélection <---
- Reproduction
- Mutation <---
