# Projet RECHERCHE OPERATIONNELLE 

**Groupe de 3 étudiants**  
**Année : 2025**  
**Cours : Recherche Opérationnelle**

---

## Membres du Groupe et Répartition des Tâches

| Nom Prénom                 | Rôle | Tâches Réalisées |
|----------------------------|------|------------------|
| **KOUANG NTEP jACKY**      | Responsable dépôt + Génération + Nouvelles analyses | • `generate_graph.py` <br> • **Q7 : 4 jours (degré max) sur graphe réduit** <br> • **Q8 : 3 jours (proximité min) sur graphe réduit** |
| **BOUGONG A ABEGA**        | Analyse du graphe initial | • **Distribution des degrés + histogramme** <br> • **Top 5 degrés** <br> • **Distribution de proximité + histogramme** |
| **DONGMO MINTIDEM VANECK** | Simulation campagne + Visualisations | • **Q5 : 5 jours (degré max)** <br> • **Q6 : 7 jours (proximité min)** <br> • `remove_nodes.py` <br> • `visualize_all.py` (8 images) |



---

## Description du Projet

Ce projet simule une **campagne marketing** sur un **réseau de 250 clients**, modélisé par un **graphe pondéré** :
- **Sommets** : Clients (250).
- **Arêtes** : Contacts avec **poids = distance moyenne en jours** (1 à 6).
- **Objectif** : Identifier les clients clés et simuler la propagation d’une campagne.

### Tâches Réalisées
1. Génération aléatoire du graphe → `contacts_original.csv`.
2. Calcul des **degrés** + **distribution** + **top 5**.
3. Calcul de la **proximité** (somme des distances) + **top 5**.
4. **Campagne** : 
   - Q5 : 5 jours depuis le sommet de **degré max**.
   - Q6 : 7 jours depuis le sommet de **proximité min**.
5. Suppression des **10 sommets clés** → `contacts_reduced.csv`.
6. Sur le nouveau graphe :
   - Q7 : 4 jours depuis le **degré max**.
   - Q8 : 3 j# Projet Graphes – Campagne Marketing

--- 

### Étapes
1. Génération du graphe → `contacts_original.csv`
2. Analyse complète (degrés, proximité, top 5)
3. Campagne Q5 & Q6
4. Suppression des **10 sommets clés** → `contacts_reduced.csv`
5. **Nouvelles analyses Q7 & Q8** sur le graphe réduit
6. **8 visualisations automatiques**

---



## Structure du Projet
