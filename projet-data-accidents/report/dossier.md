---
title: "Projet Data en Python — Accidents de la route"
subtitle: "Analyse du fichier BAAC, années 2005–2015"
author: "Rayan Leveque"
date: "Juin 2026"
lang: fr
---

# Page de garde

**M2 MIMO — Université Paris 1 Panthéon-Sorbonne**
**Année universitaire 2025-2026**

Projet : *Projet Data en Python — Accidents de la route*
Encadrants : Georges Grosz, Louis Giron

---

# En-tête

- **Membre du groupe** : Rayan Leveque
- **Période étudiée** : 2005 – 2015 inclus (Groupe 1, 11 années)
- **Outil d'IA générative utilisé** : **Claude Code** (Anthropic), modèle Claude Opus 4.7 (1M context)

## Note sur l'usage de l'outil

Claude Code est un **agent IA conversationnel** doté d'outils (lecture/écriture de fichiers, exécution de commandes shell, etc.), et non un LLM one-shot type ChatGPT. Le workflow n'a donc pas reposé sur des prompts uniques copiables, mais sur une **conversation itérative** avec l'agent, intégrée à l'environnement de développement (terminal).

En conséquence, la rubrique "prompt utilisé" du barème de référence (§1.4.1 du sujet) est remplacée dans ce dossier par une rubrique **"Travail avec l'agent"**, qui décrit pour chaque question :
- Le **contexte donné à l'agent** : contraintes, données d'entrée, format de sortie attendu.
- Les **itérations et décisions** : ce qui a été ajusté, ce qui a posé problème, ce qui a été validé.

Cette approche est honnête sur le workflow réel, et l'analyse de la stratégie d'usage d'un agent IA (vs prompting one-shot) est développée dans l'exposé.

---

# Table des matières

<!-- générée automatiquement par pandoc/typst -->

---

# 1. Récupération et formatage des données

## Question 0.0 — Téléchargement des données BAAC

**Rappel de la question :** récupérer les fichiers caracteristiques, lieux, vehicules, usagers pour les années 2005–2015, depuis [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/base-de-donnees-accidents-corporels-de-la-circulation/), ainsi que le PDF de description des bases.

**Travail avec l'agent.** Contexte : automatiser le téléchargement plutôt que de cliquer 45 fois sur des liens, en s'assurant d'exclure les `vehicules-immatricules-baac…` (piège du sujet). Itérations : première version basée sur les titres des ressources de l'API data.gouv.fr ; le filtre ratait `caracteristiques` à cause des accents (titres en `caractéristiques`), corrigé en normalisant via `unicodedata` et en matchant aussi le nom de fichier de l'URL.

**Fichier Python :** `python/download_data.py` *(hors barème — script utilitaire de setup, pas une réponse à une question notée)*.

**Résultat :** ~44 fichiers CSV + 1 PDF déposés dans `data/raw/`.

**Vérifications.** `ls data/raw/ | wc -l` confirme le compte attendu (4 types × 11 ans + 1 PDF). Échantillonnage manuel : ouverture de 2-3 CSV pour confirmer qu'ils correspondent bien au type annoncé.

---

## Question 1.1 — Conversion UTF-8, séparateur `,`

*(à compléter)*

---

## Question 1.2 — Vérification de structure et tableaux récapitulatifs

*(à compléter)*

---

## Question 1.3 — Enrichissement avec libellés des domaines énumérés

*(à compléter)*

---

# 2. Étude de la qualité des données

## 2.1. Intégrité référentielle

### Question 2.1 — Usager → Véhicule
*(à compléter)*

### Question 2.2 — Véhicule → ≥ 1 Usager
*(à compléter)*

### Question 2.3 *(facultative)* — Lieu → Accident
*(à compléter)*

### Question 2.4 *(facultative)* — Accident → un seul Lieu
*(à compléter)*

## 2.2. Domaines énumérés

### Question 3.1 — Répartition % des attributs énumérés (usagers)
*(à compléter)*

## 2.3. Valeurs absentes

### Question 4.1 — Taux de valeurs absentes (véhicules)
*(à compléter)*

## 2.4. Cohérence inter-attributs

### Question 5.1 — Incohérence `lum` × `hrmm`
*(à compléter)*

### Question 5.2 — Autre incohérence inter-attributs
*(à compléter)*

### Question 5.3 *(facultative)* — Troisième incohérence
*(à compléter)*

---

# 3. Requêtage et visualisation

### Question 6.1 — Accidents par tranche horaire d'1h
*(à compléter)*

### Question 6.2 — Tués cumulés par tranche d'âge et sexe
*(à compléter)*

### Question 6.3 — Top 10 départements (carte folium)
*(à compléter)*

### Question 6.4 — Question libre
*(à compléter)*

### Question 6.5 *(facultative)* — Carte animée par année
*(à compléter)*

---

# Conclusion / synthèse

*(à rédiger en fin de projet — bilan qualité des données, limites, pistes d'amélioration)*
