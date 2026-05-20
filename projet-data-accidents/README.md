# Projet Data — Accidents de la route

Projet M2 MIMO, année 2025-2026 (Georges Grosz / Louis Giron).
Étude de la qualité et visualisation du fichier BAAC (data.gouv.fr) pour les années 2005–2015 (Groupe 1), avec génération du code Python via **Claude Code** (outil d'IA générative retenu — agent, pas LLM one-shot).

Toutes les questions sont traitées, **y compris les facultatives** (2.3, 2.4, 5.3, 6.5).

## Arborescence

```
.
├── docs/         Sujet et supports de cours (PDF)
├── data/         Données BAAC
│   ├── raw/         Fichiers d'origine téléchargés (caracteristiques, lieux, vehicules, usagers)
│   ├── utf8/        Fichiers ré-encodés UTF-8, séparateur ',' (sortie Q1.1)
│   └── enriched/    Fichiers avec libellés des domaines énumérés (sortie Q1.3)
├── python/       Programmes Python (un fichier questionXY.py par question)
├── results/      Traces d'exécution, fichiers reponseXY.*, visualisations, cartes
└── report/       `dossier.md` (source) → `dossier.pdf` (livrable final, généré via pandoc/typst)
```

Chemins relatifs depuis `python/` : `../data`, `../results`. Voir `python/common.py`.

## Convention de nommage

Pour chaque question X.Y du sujet :
- code  → `python/questionXY.py`
- sortie → `results/reponseXY.*`

## Questions à traiter

| # | Sujet |
|---|-------|
| 1.1 | Conversion UTF-8, séparateur `,` |
| 1.2 | Vérification structure + tableaux récap (lignes/an + cumul) |
| 1.3 | Enrichissement des valeurs énumérées avec libellés |
| 2.1 | Intégrité : usager → véhicule |
| 2.2 | Intégrité : véhicule → ≥ 1 usager |
| 2.3 *(fac.)* | Intégrité : lieu → accident |
| 2.4 *(fac.)* | Intégrité : accident → un seul lieu |
| 3.1 | Répartition % des attributs énumérés (usagers) |
| 4.1 | Taux de valeurs absentes (véhicules) |
| 5.1 | Incohérences `lum` × `hrmm` |
| 5.2 | Autre incohérence inter-attributs |
| 5.3 *(fac.)* | Troisième incohérence inter-attributs |
| 6.1 | Accidents par tranche horaire d'1h |
| 6.2 | Tués cumulés par tranche d'âge (5 ans) et sexe |
| 6.3 | Top 10 départements (carte folium) |
| 6.4 | Question libre (≥ 2 tables, hors camembert) |
| 6.5 *(fac.)* | Reprise de 6.3 en gif animé par année |

## Échéances

- **08/06/2026 22h** — rendu du dossier sur Google Drive (mail à georges.grosz@gmail.com et louis@giron-dom.eu).
- **11/06/2026 9h–12h** — soutenance.
