# Introduction-au-traitement-d-image
Projet du cours "Introduction au traitement d'image" du printemps 2017

# Introduction

L'objectif de ce projet est de développer un programme en python qui permet l'analyse d'images satellites.

Dans un premier temps, il s'agira de récolter les statistiques descriptives liées aux pixels qui composent l'image satellite.
En outre, un travail de visulation de ces données et statistiques sera nécessaire.

Dans un deuxième temps, ce programme devra permettre la classification des pixels dans différentes catégories d'occupation du sol.
La méthode doit encore être déterminée; Analyse d'image supervisée ? non supervisée ? basée objets ? Toutes puis comparaison des méthodes?


# Statistiques descriptives

Lorsqu'on lui donne une image en argument, le programme retourne quelques statistiques descriptives (module ImageStat):
- Valeurs max et min des pixels (RGB -> 6 valeurs)
- La somme des pixels
- Valeurs moyenne des pixels (RGB -> 3 valeurs)
- Valeurs médiane des pixels (RGB -> 3 valeurs)
- L'écart type (RGB -> 3 valeurs)

# Classification des pixels

K-means
    Première classification non supervisée, et par pixel (module scipy.cluster.vq): K-means.
    Cette méthode permet de classifier chaque pixel dans un nombre de groupes définit par l'utilisateur.
    Observations: Effet "poivre sel". Les objets ne sont pas très bien définis.
    
    


