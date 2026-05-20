# Présentation du Projet Data

**Auteurs :** Georges Grosz, Louis Giron  
**Date :** Mai 2026

---

## Planning détaillé

| Date | Horaire | Contenu |
|------|---------|---------|
| 06/05/2026 | 13h30–16h30 | Présentation du projet et exemples d'utilisation, bibliothèque Panda Folium |
| 03/06/2026 | 13h30–16h30 | TP projet : travail en classe, réponses aux questions, mises au point, déblocages |
| 11/06/2026 | 9h–12h | Soutenance du projet |

---

## Le projet

- Projet sur la qualité et la visualisation de données ouvertes.
- Réalisation en Python.
- Utilisation d'un outil d'IA générative (e.g. chatGPT) pour générer le code Python.
- Participation du professeur de Python : Louis Giron.
- 2 groupes de 2 étudiants + 1 groupe de 3 étudiants.
- Dossier projet à rendre le 08/06/2026 22h, points en moins si retard (1/j).
- Soutenance le 11/06/2026.

**Google drive des supports :**  
https://drive.google.com/drive/folders/18LXRB1paWlCNsUZMqvB_fACJhE4yWSBM?usp=drive_link

---

## Sujet — Les grandes étapes

1. **Récupérer les données** de data.gouv.fr sur les accidents de la route :  
   https://www.data.gouv.fr/fr/datasets/base-de-donnees-accidents-corporels-de-la-circulation/

2. **Analyser la qualité des données** avec du code Python généré par un outil IA gén :
   - Vérifier que les résultats sont corrects.

3. **Générer des visualisations** des données avec du code Python généré par un outil IA gén :
   - Choisir la meilleure visualisation.
   - Vérifier que les résultats sont corrects.

4. **En transverse** : analyser, commenter le code généré par l'outil et les résultats obtenus.

---

## Conseils et attendus

- Nécessité de comprendre et de commenter le code Python généré. Des questions de compréhension du code seront posées durant la soutenance.
- Pour plus d'efficacité avec l'outil de génération, faire les choses par étapes, une demande à la fois. Il peut être pertinent de découper un « gros » problème en plusieurs « petits » problèmes.
- Vérifier que les résultats générés par les programmes Python sont corrects, à minima par échantillonnage manuel, éventuellement utilisation de Excel ou un autre moyen et si besoin par un programme Python…
- Il faut travailler de manière itérative. On rédige un premier prompt, on analyse le programme généré et le résultat de l'exécution du programme généré. On identifie les problèmes, les améliorations. On corrige/complète le prompt et on itère.
- Les 2 groupes de 2 doivent faire toutes les questions et éventuellement les questions facultatives. Le groupe de 3 doit faire toutes les questions ET toutes les questions facultatives (qui ne le sont donc pas !).

---

## Modalités de contrôle

### Dossier Projet : 80 %

Pour chaque question (cf sujet) :
1. Prompt utilisé
2. Code généré (dans un fichier)
3. Réponse obtenue
4. Vérifications réalisées
5. Commentaires résultats obtenus
6. Commentaires sur le code python généré
7. Itérations réalisées et problèmes rencontrés

### Exposé : 20 % (Présentation 25' + 20' de questions)

- Analyse du travail réalisé, difficultés/réussites.
- Proposition (d'éléments) de bonnes pratiques et/ou d'une stratégie pour écrire des prompts efficaces dans le contexte de la qualité et de la visualisation de la donnée avec des programmes Python.

---

## Trucs et astuces

- Le cycle rédaction prompt, génération code, copie dans un fichier .py, exécution (itération sur le prompt).
- Transformer un fichier csv en fichier Excel.
- Modifier l'affichage d'un nombre 2.99E11 en nombre 299098765625.
- Utiliser les filtres sous Excel, figer la première ligne.
- Utiliser les tableaux croisés dynamiques pour :
  - Retirer les doublons d'une liste.
  - Compter le nombre de lignes en fonction d'un critère simple.
- Organiser l'arborescence des fichiers Données, Python, Résultats.
- Savoir référencer les répertoires de manière relative, exemple : `../Données`.
- Que faire quand le programme génère une ou des erreurs ?
- Pour faciliter la lecture utiliser un code couleur différent pour les prompts, les résultats/traces générés, les commentaires.
- Utiliser un bon éditeur de texte, par exemple : Notepad++.
