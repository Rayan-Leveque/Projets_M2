# Projet Data en Python — Accidents de la route

**Année universitaire :** 2025-2026  
**Auteurs :** Georges Grosz, Louis Giron  
**Emails :** georges.grosz@gmail.com, louis@giron-dom.eu

---

## Historique des versions

| Date | Rédacteur | Modifications |
|------|-----------|---------------|
| 11/03/2026 | GGR | Première version du document |
| 30/03/2026 | GGR | V2 — simplifications |
| 23/04/2026 | GGR | V3 — nouvelles simplifications |
| 26/04/2026 | GGR | Corrections |

---

## 1. Introduction

### 1.1. Pour commencer

Ce projet a pour ambition de :
- Mettre en pratique des activités autour de la data tel qu'un « data scientist » pourrait le faire.
- Rendre concrets certains des concepts présentés dans le cours « Maitriser la data ».
- Utiliser des outils de l'IA générative orientés textes (tel que ChatGPT) pour générer des programmes Python pour répondre aux questions proposées.
- Analyser les programmes générés, les résultats fournis et vérifier qu'ils sont corrects.

Les données utilisées sont issues des données ouvertes proposées par le gouvernement français (data.gouv.fr). Elles concernent les accidents de la route en France.

Le projet est réalisable sur un « PC bureautique » ou sur un Mac. Il faut disposer de moyen pour exécuter des programmes Python et d'un bon éditeur de texte (par exemple : notepad++). Aucun outil de l'IA générative n'est recommandé, chacun choisit celui qu'il souhaite utiliser.

### 1.2. Les données

Le sujet du projet est l'étude de la base de données annuelle des accidents corporels de la circulation routière. Ces données sont disponibles en accès libre sur data.gouv.fr. Dans un souci de simplification, on se concentre sur les années 2005 à 2017 (car il y a eu des changements de format dans les fichiers après 2017).

Cette base de données comporte les informations sur chaque accident corporel qui a eu lieu en France sur la période. La saisie des informations décrivant l'accident est effectuée par l'unité des forces de l'ordre (police, gendarmerie, etc.) qui est intervenue sur le lieu de l'accident. Ces saisies sont rassemblées dans une fiche intitulée Bulletin d'Analyse des Accidents Corporels. L'ensemble de ces fiches constitue le fichier national des accidents corporels de la circulation dit « Fichier BAAC » administré par l'Observatoire National Interministériel de la Sécurité Routière "ONISR".

Ces données répertorient l'intégralité des accidents corporels de la circulation, intervenus durant une année précise en France métropolitaine, dans les départements d'Outre-mer (Guadeloupe, Guyane, Martinique, La Réunion et Mayotte depuis 2012) avec une description simplifiée. Cela comprend des informations concernant :
- Les caractéristiques de l'accident,
- Le lieu de l'accident,
- Le ou les véhicules impliqués,
- La ou les victimes.

> **Dans la suite du document, on se limite à l'analyse des accidents situés dans la France métropolitaine.**

### 1.3. Organisation

Afin d'avoir des résultats différents pour chaque groupe, la répartition des années à analyser par groupe est la suivante :

| Groupe | Années |
|--------|--------|
| Groupe 1 | 2005 à 2015 incluses |
| Groupe 2 | 2006 à 2016 incluses |
| Groupe 3 | 2007 à 2017 incluses |

Par exemple, le groupe 1 doit travailler uniquement sur les données des années 2005 à 2015 incluses.

### 1.4. Attendus

#### 1.4.1. Le dossier

Le dossier du projet doit être rendu le 8 juin 2026 avant 22h. Il doit être déposé dans le google drive dans le dossier du groupe.

**Lien :** https://drive.google.com/drive/folders/18LXRB1paWlCNsUZMqvB_fACJhE4yWSBM?usp=sharing

Un mail doit être envoyé à georges.grosz@gmail.com et à louis@giron-dom.eu pour nous informer du dépôt.

Le dossier comporte :
- Un document PDF de présentation globale,
- Un dossier avec tous les fichiers des programmes Python utilisés,
- Un dossier avec toutes les données utilisées ainsi que celles qui sont générées,
- Un dossier avec la trace de l'exécution/visualisation générée par les différents programmes.

Le document PDF contient les éléments suivants.

**En en-tête**, après la page de garde et la table des matières :
- Les membres du groupe,
- La période étudiée,
- L'outil d'IA générative utilisé et sa version.

**Et pour chacune des questions ci-dessous**, les réponses attendues doivent avoir le format suivant :
1. Rappel de la question traitée,
2. Le prompt utilisé (quand applicable),
3. Le nom du fichier Python qui contient le code exécuté (exemple : pour la question 2.2, le fichier Python associé sera nommé `question22.py`), merci de vérifier que le fichier est dans le dossier des programmes Python,
4. Le résultat de l'exécution du code Python (quand applicable) et/ou le ou les noms de fichiers générés exécuté (exemple : pour la question 2.2, le fichier réponse associé sera nommé `réponse22.txt` — ou tout autre extension), merci de vérifier que le fichier ou les fichiers générés sont dans le dossier des traces,
5. La solution/analyse proposée et/ou des commentaires sur les corrections/ajustements/itérations réalisés et/ou les vérifications réalisées et/ou la description du ou des fichiers générés.

Il est essentiel de vérifier que les exécutions des différents programmes générés par une IA générative fournissent des résultats corrects. Ce peut être soit en modifiant les données manuellement, soit par des calculs réalisés via Excel ou par tout autre moyen. **Une réponse à une question sans vérification aura au mieux la moitié des points.**

La concision et la clarté du dossier sont des éléments importants de l'évaluation. Il faut fournir le plus d'indications démontrant le déroulé de votre travail et vos résultats mais de la manière la plus synthétique possible. Cela passe principalement par des commentaires appropriés.

Les groupes de 3 personnes doivent traiter toutes les questions facultatives.

#### 1.4.2. L'exposé

L'exposé sera réalisé le jeudi 11 juin 2026 au matin. L'objectif est :
1. De présenter les principaux enseignements sur la rédaction des prompts (règles d'écriture), les difficultés rencontrées et leurs résolutions.
2. De présenter une analyse du code généré.

Prévoir 25' de présentation (35' pour le groupe 3 personnes) et 20' de questions.

---

## 2. Le travail à réaliser

### 2.1. Récupération et formatage des données

#### Question 0

**0.0** — Pour récupérer les données, il faut se rendre sur :  
https://www.data.gouv.fr/fr/datasets/base-de-donnees-accidents-corporels-de-la-circulation/

et télécharger les fichiers correspondants aux années assignées à votre groupe projet dans un répertoire "Données" à créer.

Plus précisément pour chacune des années de la période étudiée, il faut télécharger les fichiers des quatre types suivants :
- **caractéristiques**,
- **lieux**,
- **véhicules** (attention aux différents nommages des fichiers (avec `-` ou `_`), ne pas prendre les fichiers nommés `vehicules-immatricules-baac…`),
- **usagers**.

Il faut également télécharger le fichier `description-des-bases-de-donnees-onisr-annees-2005-a-2018.pdf` qui décrit la structure des différentes tables et chaque attribut dans le détail. Avant de commencer le travail, il est conseillé de lire attentivement ce document.

#### Questions 1

**1.1** — Par précaution, à l'aide d'un programme Python, transformer le codage de tous les fichiers de données au format utf-8 et s'assurer que le séparateur est bien `,`.

**1.2** — Vérifier par programme que pour chaque type de fichier (caractéristiques, lieux, véhicules et usagers), les fichiers des différentes années ont une structure conforme à la documentation. Faire 4 tableaux récapitulatifs avec le nombre de lignes par année présents dans chaque fichier et le cumul pour chaque type.

**1.3** — Pour tous les fichiers obtenus en 1.1, générer une nouvelle version de chacun de ces fichiers où toutes les valeurs de tous les domaines énumérés sont complétées avec le libellé correspondant.

Par exemple dans la documentation, le champ `lum` de `caractéristiques` est décrit de la manière suivante :

| Code | Libellé |
|------|---------|
| 1 | Plein jour |
| 2 | Crépuscule ou aube |
| 3 | Nuit sans éclairage public |
| 4 | Nuit avec éclairage public non allumé |
| 5 | Nuit avec éclairage public allumé |

Ainsi, la valeur 1 pour le champ `lum` doit être transformée en `"1 - Plein jour"`, la valeur 2 en `"2 - Crépuscule ou aube"`, etc.

Vérifier que la transformation est correcte. Porter une attention particulière à l'attribut `catv` de vehicule.

---

### 2.2. Etude de la qualité des données

L'étude de la qualité des données comporte une dimension métier. Afin de faciliter l'analyse et la lecture des données, il faut utiliser les données générées au 1.3.

#### 2.2.1. Etude de l'intégrité référentielle

Il s'agit de vérifier la cohérence des références réalisées entre les différents fichiers (via les numéros d'accident — `NumAcc` — et numéro de véhicule — `Num_Veh`). Pour toutes les questions ci-dessous, si des données incohérentes existent, elles doivent être toutes listées dans un fichier dédié, analysées et commentées.

##### Questions 2

**2.1** — Vérifier par programme que chaque usager fait référence à un véhicule présent dans les véhicules.

**2.2** — Et inversement, vérifier par programme que chaque véhicule décrit dans les véhicules est associé à au moins un usager.

**2.3** — *(question facultative)* Vérifier par programme que chaque lieu fait référence à un accident présent dans les caractéristiques.

**2.4** — *(question facultative)* Et inversement, vérifier par programme que chaque accident décrit dans les caractéristiques se déroule bien sur un et un seul lieu.

#### 2.2.2. Etude de l'utilisation des domaines énumérés

Pour un attribut défini par un type énuméré, il est intéressant d'étudier la répartition en % des différentes valeurs. Si une valeur est utilisée dans un nombre important de cas, ce peut être normal mais ce peut aussi être parce que la valeur a été mal choisie. Dans ce cas, il faudrait aller poser la question au métier afin d'affiner cette valeur et de rendre la liste plus pertinente, plus discriminante.

Par exemple, si on étudie la forme géométrique d'un logo et que l'on a pour valeur ronde, ovale ou polygonale, il est probable que polygonale soit imprécis et qu'il faille remplacer cette valeur par carré, rectangle, losange, etc.

Si un attribut énuméré possède une valeur de type « non renseigné » ou « autre » et que l'utilisation de cette valeur est importante, cela indique certainement que la liste des valeurs a été mal choisie et qu'elle devrait être révisée par le métier afin de diminuer l'usage de valeurs non significatives.

Pour les fichiers BAAC, la liste des valeurs de tous les domaines énumérés est fournie dans la documentation `description-des-bases-de-donnees-onisr-annees-2005-a-2018.pdf`.

Il faut également vérifier que les valeurs présentes dans les fichiers sont bien celles décrites dans la documentation.

##### Question 3

**3.1** — Faire un programme qui détaille la répartition en % des valeurs pour tous les attributs énumérés du fichier des usagers. Commenter le résultat.

#### 2.2.3. Analyse des valeurs absentes

Une valeur absente est une donnée qui n'a pas été renseignée lors de la saisie (ou qui n'est pas applicable). Dans les fichiers CSV des accidents, elle peut apparaître sous la forme d'une cellule vide, d'un point (`.`) ou d'un code dédié comme `-1`, conformément à la documentation. Les valeurs absentes doivent être distinguées des valeurs numériques réelles afin d'éviter des interprétations erronées lors des analyses statistiques.

Dans les fichiers des caractéristiques, une valeur absente peut apparaître sous plusieurs formes (selon la documentation) :
- cellule vide
- `.`
- `-1` (code "non renseigné")
- parfois `0` (selon l'attribut)

En fonction du taux de valeurs absentes, l'interprétation proposée est la suivante :
- **taux faible (< 5 %)** → variable bien renseignée
- **taux modéré (5–15 %)** → variable exploitable avec prudence
- **taux élevé (> 15–20 %)** → variable fragile (biais possibles)

##### Question 4

**4.1** — Faire un programme qui mesure le taux de valeurs absentes pour chaque champ du fichier des véhicules et interpréter les résultats.

#### 2.2.4. Analyse de la cohérence inter-attributs

On va chercher à détecter des incohérences entre les valeurs de 2 (ou plus) attributs. Par exemple, dans `caracteristiques`, on dispose des attributs `hrmm` et `lum`. Si pour un accident, l'heure est `0020` (minuit et 20') et l'attribut `lum` est « Plein jour », on a une incohérence car il ne fait pas plein jour autour de minuit.

##### Questions 5

**5.1** — Compter le nombre d'accidents pour lesquels il y a une incohérence entre les attributs `lum` et `hrmm`, afficher les 10 premiers et générer le rapport complet dans un fichier. Commenter les résultats.

**5.2** — Identifier une situation différente (autre que `lum` et `hrmm`) où il pourrait avoir des incohérences inter-attributs. Calculer le nombre de ligne en incohérence, afficher les 10 premières lignes et générer le rapport complet dans un fichier. Commenter les résultats.

**5.3** — *(question facultative)* Identifier une autre situation différente des deux précédentes où il pourrait avoir des incohérences inter-attributs. Calculer le nombre de ligne en incohérence, afficher les 10 premières lignes et générer le rapport complet dans un fichier. Commenter les résultats.

---

### 2.3. Requêtage et visualisation des résultats

Il faut faire un programme Python pour générer une réponse à chacune des questions suivantes. Il faut choisir le bon format de visualisation, les bons libellés, la bonne légende et les bonnes couleurs (quand applicable). Si la question est ambigüe, énoncer une formulation qui ne l'est pas et traiter cette dernière.

La lecture du résultat de chaque question doit être commentée.

##### Questions 6

**6.1** — Afficher le nombre d'accidents par tranche horaire d'une heure.

**6.2** — Fournir un graphique qui présente le nombre de tués cumulé sur la période du projet par tranche d'âge (de 5 années) et par sexe.

**6.3** — Quels sont les 10 départements avec le plus d'accidents ? Il faut faire l'affichage sur une carte de France en utilisant la bibliothèque folium.

**6.4** — Question libre à définir, utiliser au moins 2 types de table (parmi caracteristiques, lieux, vehicules et usagers) et un type d'affichage autre que les précédents (camembert exclu).

**6.5** — *(question facultative)* Reprendre la question 6.3 et faire un gif animé de la carte par année (utiliser par exemple Canva pour la génération du gif).
