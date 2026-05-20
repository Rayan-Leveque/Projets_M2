#!/usr/bin/env bash
# Pipeline autonome — projet-data-accidents
# Lance Claude Code (cc) et OpenCode (oc) sur les 17 questions dans l'ordre.
# Reprend depuis la dernière question complétée si interrompu.
# Usage : bash run_pipeline.sh
set -euo pipefail

PROJECT=/home/rayan/Documents/Projets/projet-data-accidents
STATE_FILE="$PROJECT/.pipeline-state"
LOG_FILE="$PROJECT/pipeline.log"

QUESTIONS=(Q11 Q12 Q13 Q21 Q22 Q23 Q24 Q31 Q41 Q51 Q52 Q53 Q61 Q62 Q63 Q64 Q65)
SCRIPTS=(question11 question12 question13 question21 question22 question23 question24 question31 question41 question51 question52 question53 question61 question62 question63 question64 question65)
AGENTS=(cc cc cc cc cc cc cc oc oc cc cc oc oc oc oc oc oc)

CURRENT_IDX=0
[ -f "$STATE_FILE" ] && CURRENT_IDX=$(cat "$STATE_FILE")

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILE"; }

# ─── Prompts ──────────────────────────────────────────────────────────────────

prompt_Q11() { cat <<'PROMPT'
Tu travailles sur le projet "Accidents de la route" — M2 MIMO Paris 1, Groupe 1 (2005–2015).
Le projet est dans le répertoire courant.

QUESTION 1.1 (extrait du sujet) :
Par précaution, à l'aide d'un programme Python, transformer le codage de tous les fichiers de
données au format utf-8 et s'assurer que le séparateur est bien `,`.

FICHIERS À CRÉER :
- python/question11.py : le script de conversion
- results/reponse11.txt : résumé des fichiers traités (encodage détecté → utf-8, nb fichiers)

CONTEXTE TECHNIQUE :
- Les fichiers source sont dans data/raw/ (4 types × 11 ans : caracteristiques, lieux, vehicules, usagers)
- Les fichiers convertis vont dans data/utf8/ (créer le dossier si nécessaire)
- Nommage des fichiers de sortie : {type}_{année}.csv (ex. caracteristiques_2005.csv)
- Utiliser chardet ou tester les encodages courants (latin-1, utf-8, cp1252) pour détecter l'encodage source
- Remplacer le séparateur par une virgule si c'est un point-virgule
- from common import RAW, UTF8, TYPES_FICHIERS, ANNEE_DEBUT, ANNEE_FIN
- Style : variables et commentaires en français, boucles explicites, prints de progression

APRÈS AVOIR CRÉÉ ET EXÉCUTÉ LE SCRIPT :
Mettre à jour report/dossier.md : remplacer "*(à compléter)*" sous "Question 1.1" par :
1. Rappel de la question
2. Travail avec l'agent (ce qui a été fait, encodages rencontrés)
3. Fichier Python : python/question11.py
4. Résultat : results/reponse11.txt
5. Vérifications et commentaires
PROMPT
}

prompt_Q12() { cat <<'PROMPT'
Tu travailles sur le projet "Accidents de la route" — M2 MIMO Paris 1, Groupe 1 (2005–2015).
Le projet est dans le répertoire courant.

QUESTION 1.2 (extrait du sujet) :
Vérifier par programme que pour chaque type de fichier (caractéristiques, lieux, véhicules et
usagers), les fichiers des différentes années ont une structure conforme à la documentation.
Faire 4 tableaux récapitulatifs avec le nombre de lignes par année présents dans chaque fichier
et le cumul pour chaque type.

FICHIERS À CRÉER :
- python/question12.py : le script de vérification
- results/reponse12.txt : les 4 tableaux (type, année, nb_lignes, nb_colonnes, cumul)

CONTEXTE TECHNIQUE :
- Lire depuis data/utf8/
- Schéma attendu par type (colonnes réelles 2005-2015) :
  * caracteristiques : Num_Acc, an, mois, jour, hrmn, lum, agg, int, atm, col, com, adr, gps, lat, long, dep
  * lieux : Num_Acc, catr, voie, v1, v2, circ, nbv, pr, pr1, vosp, prof, plan, lartpc, larrout, surf, infra, situ, env1
  * vehicules : Num_Acc, senc, catv, occutc, obs, obsm, choc, manv, num_veh
  * usagers : Num_Acc, place, catu, grav, sexe, trajet, secu, locp, actp, etatp, an_nais, num_veh
- Signaler toute colonne manquante ou inattendue
- from common import UTF8, TYPES_FICHIERS, ANNEE_DEBUT, ANNEE_FIN
- Style : variables et commentaires en français, tableaux formatés avec f-strings ou tabulate

APRÈS AVOIR CRÉÉ ET EXÉCUTÉ LE SCRIPT :
Mettre à jour report/dossier.md : remplacer "*(à compléter)*" sous "Question 1.2" par les 5 rubriques habituelles.
PROMPT
}

prompt_Q13() { cat <<'PROMPT'
Tu travailles sur le projet "Accidents de la route" — M2 MIMO Paris 1, Groupe 1 (2005–2015).
Le projet est dans le répertoire courant.

QUESTION 1.3 (extrait du sujet) :
Pour tous les fichiers obtenus en 1.1, générer une nouvelle version de chacun de ces fichiers
où toutes les valeurs de tous les domaines énumérés sont complétées avec le libellé correspondant.
Par exemple, la valeur 1 pour lum devient "1 - Plein jour", la valeur 2 devient "2 - Crépuscule ou aube", etc.
Vérifier que la transformation est correcte. Porter une attention particulière à catv de vehicule.

FICHIERS À CRÉER :
- python/question13.py : le script d'enrichissement
- results/reponse13.txt : vérification (nb fichiers créés, échantillon de valeurs enrichies)

CONTEXTE TECHNIQUE :
- Lire depuis data/utf8/, écrire dans data/enriched/ (même nommage : {type}_{année}.csv)
- from common import UTF8, ENRICHED, TYPES_FICHIERS, ANNEE_DEBUT, ANNEE_FIN
- Consulter docs/schema_baac.md pour la liste complète des colonnes énumérées et leurs libellés
- Colonnes à enrichir (référence schema_baac.md §4 Q1.3) :
  * caracteristiques : lum, agg, int, atm, col
  * lieux : catr, circ, vosp, prof, plan, surf, infra, situ
  * vehicules : senc, catv, obs, obsm, choc, manv
  * usagers : catu, grav, sexe, trajet, locp, actp, etatp
- Format des valeurs enrichies : "code - libellé" (ex. "1 - Plein jour")
- Conserver les colonnes non-énumérées telles quelles
- Attention catv : codes zero-paddés sur 2 chiffres ("07", "01"...) — normaliser avant lookup
- Style : dictionnaires de mapping explicites en français, boucles lisibles

APRÈS AVOIR CRÉÉ ET EXÉCUTÉ LE SCRIPT :
Mettre à jour report/dossier.md : remplacer "*(à compléter)*" sous "Question 1.3" par les 5 rubriques habituelles.
PROMPT
}

prompt_Q21() { cat <<'PROMPT'
Tu travailles sur le projet "Accidents de la route" — M2 MIMO Paris 1, Groupe 1 (2005–2015).
Le projet est dans le répertoire courant.

QUESTION 2.1 (extrait du sujet) :
Vérifier par programme que chaque usager fait référence à un véhicule présent dans les véhicules.
Si des données incohérentes existent, elles doivent être toutes listées dans un fichier dédié,
analysées et commentées.

FICHIERS À CRÉER :
- python/question21.py : le script de vérification
- results/reponse21.txt : résumé (nb violations / nb total usagers) + commentaires
- results/reponse21_violations.csv : liste des violations si elles existent (Num_Acc, num_veh, année)

CONTEXTE TECHNIQUE :
- Lire depuis data/enriched/
- Clé de jointure : (Num_Acc, num_veh) — usagers doit pointer vers vehicules
- from common import ENRICHED, ANNEE_DEBUT, ANNEE_FIN
- Traiter année par année, cumuler les violations
- Style : variables et commentaires en français, csv.reader pour la lecture

APRÈS AVOIR CRÉÉ ET EXÉCUTÉ LE SCRIPT :
Mettre à jour report/dossier.md : remplacer "*(à compléter)*" sous "Question 2.1" par les 5 rubriques.
PROMPT
}

prompt_Q22() { cat <<'PROMPT'
Tu travailles sur le projet "Accidents de la route" — M2 MIMO Paris 1, Groupe 1 (2005–2015).
Le projet est dans le répertoire courant.

QUESTION 2.2 (extrait du sujet) :
Vérifier par programme que chaque véhicule décrit dans les véhicules est associé à au moins un usager.
Si des données incohérentes existent, elles doivent être toutes listées dans un fichier dédié,
analysées et commentées.

FICHIERS À CRÉER :
- python/question22.py : le script de vérification
- results/reponse22.txt : résumé (nb véhicules sans usager / nb total) + commentaires
- results/reponse22_violations.csv : liste des violations (Num_Acc, num_veh, année)

CONTEXTE TECHNIQUE :
- Lire depuis data/enriched/
- Clé de jointure : (Num_Acc, num_veh) — chaque véhicule doit avoir ≥1 usager
- Note : des véhicules sans usager peuvent correspondre à des conducteurs en fuite (cas connu)
- from common import ENRICHED, ANNEE_DEBUT, ANNEE_FIN
- Style : variables et commentaires en français

APRÈS AVOIR CRÉÉ ET EXÉCUTÉ LE SCRIPT :
Mettre à jour report/dossier.md : remplacer "*(à compléter)*" sous "Question 2.2" par les 5 rubriques.
PROMPT
}

prompt_Q23() { cat <<'PROMPT'
Tu travailles sur le projet "Accidents de la route" — M2 MIMO Paris 1, Groupe 1 (2005–2015).
Le projet est dans le répertoire courant.

QUESTION 2.3 (facultative — extrait du sujet) :
Vérifier par programme que chaque lieu fait référence à un accident présent dans les caractéristiques.
Si des données incohérentes existent, elles doivent être toutes listées dans un fichier dédié,
analysées et commentées.

FICHIERS À CRÉER :
- python/question23.py : le script de vérification
- results/reponse23.txt : résumé (nb lieux sans accident correspondant) + commentaires
- results/reponse23_violations.csv : liste des violations (Num_Acc, année)

CONTEXTE TECHNIQUE :
- Lire depuis data/enriched/
- Clé : Num_Acc dans lieux doit exister dans caracteristiques
- from common import ENRICHED, ANNEE_DEBUT, ANNEE_FIN
- Style : variables et commentaires en français

APRÈS AVOIR CRÉÉ ET EXÉCUTÉ LE SCRIPT :
Mettre à jour report/dossier.md : remplacer "*(à compléter)*" sous "Question 2.3" par les 5 rubriques.
PROMPT
}

prompt_Q24() { cat <<'PROMPT'
Tu travailles sur le projet "Accidents de la route" — M2 MIMO Paris 1, Groupe 1 (2005–2015).
Le projet est dans le répertoire courant.

QUESTION 2.4 (facultative — extrait du sujet) :
Vérifier par programme que chaque accident décrit dans les caractéristiques se déroule bien
sur un et un seul lieu.
Si des données incohérentes existent, elles doivent être toutes listées dans un fichier dédié,
analysées et commentées.

FICHIERS À CRÉER :
- python/question24.py : le script de vérification
- results/reponse24.txt : résumé (nb accidents avec 0 ou 2+ lieux) + commentaires
- results/reponse24_violations.csv : liste des violations (Num_Acc, nb_lieux, année)

CONTEXTE TECHNIQUE :
- Lire depuis data/enriched/
- Pour chaque Num_Acc dans caracteristiques, compter ses occurrences dans lieux
- from common import ENRICHED, ANNEE_DEBUT, ANNEE_FIN
- Style : variables et commentaires en français

APRÈS AVOIR CRÉÉ ET EXÉCUTÉ LE SCRIPT :
Mettre à jour report/dossier.md : remplacer "*(à compléter)*" sous "Question 2.4" par les 5 rubriques.
PROMPT
}

prompt_Q31() { cat <<'PROMPT'
Tu travailles sur le projet "Accidents de la route" — M2 MIMO Paris 1, Groupe 1 (2005–2015).
Le projet est dans le répertoire courant.

QUESTION 3.1 (extrait du sujet) :
Faire un programme qui détaille la répartition en % des valeurs pour tous les attributs énumérés
du fichier des usagers. Commenter le résultat.

FICHIERS À CRÉER :
- python/question31.py : le script de répartition
- results/reponse31.txt : tableau par attribut avec % de chaque valeur + commentaires

CONTEXTE TECHNIQUE :
- Lire depuis data/enriched/ (valeurs déjà enrichies avec libellés)
- Attributs énumérés dans usagers : catu, grav, sexe, trajet, secu, locp, actp, etatp
- Attention secu : champ à 2 caractères (ex. "11", "12"), traiter comme chaîne
- Cumuler sur toutes les années 2005-2015
- Vérifier que les valeurs présentes correspondent à celles de la documentation
- from common import ENRICHED, ANNEE_DEBUT, ANNEE_FIN
- Style : variables et commentaires en français, affichage trié par % décroissant

APRÈS AVOIR CRÉÉ ET EXÉCUTÉ LE SCRIPT :
Mettre à jour report/dossier.md : remplacer "*(à compléter)*" sous "Question 3.1" par les 5 rubriques.
PROMPT
}

prompt_Q41() { cat <<'PROMPT'
Tu travailles sur le projet "Accidents de la route" — M2 MIMO Paris 1, Groupe 1 (2005–2015).
Le projet est dans le répertoire courant.

QUESTION 4.1 (extrait du sujet) :
Faire un programme qui mesure le taux de valeurs absentes pour chaque champ du fichier des
véhicules et interpréter les résultats.

FICHIERS À CRÉER :
- python/question41.py : le script d'analyse des valeurs manquantes
- results/reponse41.txt : tableau (colonne, nb_manquants, taux_%) + interprétation

CONTEXTE TECHNIQUE :
- Lire depuis data/enriched/
- Colonnes vehicules : Num_Acc, senc, catv, occutc, obs, obsm, choc, manv, num_veh
- Valeurs manquantes selon la documentation : cellule vide '', point '.', '-1', '0'/'00'/'000'
  Attention : '0' pour senc peut être une vraie valeur dans certaines années
- Interprétation des taux : <5% = bien renseigné, 5-15% = prudence, >15% = fragile
- Cumuler sur toutes les années 2005-2015
- from common import ENRICHED, ANNEE_DEBUT, ANNEE_FIN
- Style : variables et commentaires en français

APRÈS AVOIR CRÉÉ ET EXÉCUTÉ LE SCRIPT :
Mettre à jour report/dossier.md : remplacer "*(à compléter)*" sous "Question 4.1" par les 5 rubriques.
PROMPT
}

prompt_Q51() { cat <<'PROMPT'
Tu travailles sur le projet "Accidents de la route" — M2 MIMO Paris 1, Groupe 1 (2005–2015).
Le projet est dans le répertoire courant.

QUESTION 5.1 (extrait du sujet) :
Compter le nombre d'accidents pour lesquels il y a une incohérence entre les attributs lum et hrmn,
afficher les 10 premiers et générer le rapport complet dans un fichier. Commenter les résultats.

Contexte : si lum=1 (Plein jour) mais que l'heure est la nuit, ou inversement lum=3/4/5 (nuit)
mais que l'heure est en pleine journée, il y a incohérence.

FICHIERS À CRÉER :
- python/question51.py : le script de détection des incohérences
- results/reponse51.txt : nb total d'incohérences, les 10 premiers cas, commentaires
- results/reponse51_complet.csv : rapport complet de toutes les incohérences

CONTEXTE TECHNIQUE :
- Lire depuis data/enriched/
- Colonne hrmn : format HHMM (ex. "1900", "0200") — extraire l'heure avec int(hrmn[:2]) ou int(hrmn)//100
- Règle d'incohérence :
  * lum contient "1 - Plein jour" ET heure hors de [8, 19] → incohérent
  * lum contient "3 - Nuit" ou "4 - Nuit" ou "5 - Nuit" ET heure entre [10, 16] → incohérent
- Ne pas traiter les hrmn vides ou invalides
- from common import ENRICHED, ANNEE_DEBUT, ANNEE_FIN
- Style : variables et commentaires en français

APRÈS AVOIR CRÉÉ ET EXÉCUTÉ LE SCRIPT :
Mettre à jour report/dossier.md : remplacer "*(à compléter)*" sous "Question 5.1" par les 5 rubriques.
PROMPT
}

prompt_Q52() { cat <<'PROMPT'
Tu travailles sur le projet "Accidents de la route" — M2 MIMO Paris 1, Groupe 1 (2005–2015).
Le projet est dans le répertoire courant.

QUESTION 5.2 (extrait du sujet) :
Identifier une situation différente (autre que lum et hrmn) où il pourrait avoir des incohérences
inter-attributs. Calculer le nombre de lignes en incohérence, afficher les 10 premières lignes
et générer le rapport complet dans un fichier. Commenter les résultats.

Situation choisie : incohérence entre obsm (obstacle mobile heurté) et choc (point de choc initial).
Si obsm ≠ "0 - Aucun" (un obstacle mobile a été heurté) mais choc = "0 - Aucun" (aucun point de choc
enregistré), il y a contradiction : on ne peut pas heurter quelque chose sans point d'impact.

FICHIERS À CRÉER :
- python/question52.py : le script de détection
- results/reponse52.txt : nb total d'incohérences, 10 premiers cas, commentaires
- results/reponse52_complet.csv : rapport complet

CONTEXTE TECHNIQUE :
- Lire depuis data/enriched/ (table vehicules)
- obsm et choc sont des colonnes de vehicules (pas de caracteristiques)
- Les valeurs enrichies commencent par "0 - " pour la valeur "aucun"
- from common import ENRICHED, ANNEE_DEBUT, ANNEE_FIN
- Style : variables et commentaires en français

APRÈS AVOIR CRÉÉ ET EXÉCUTÉ LE SCRIPT :
Mettre à jour report/dossier.md : remplacer "*(à compléter)*" sous "Question 5.2" par les 5 rubriques.
PROMPT
}

prompt_Q53() { cat <<'PROMPT'
Tu travailles sur le projet "Accidents de la route" — M2 MIMO Paris 1, Groupe 1 (2005–2015).
Le projet est dans le répertoire courant.

QUESTION 5.3 (facultative — extrait du sujet) :
Identifier une autre situation différente des deux précédentes où il pourrait avoir des incohérences
inter-attributs. Calculer le nombre de lignes en incohérence, afficher les 10 premières lignes
et générer le rapport complet dans un fichier. Commenter les résultats.

Situation choisie : années de naissance impossibles dans usagers.
Si an_nais est renseigné (non vide, non "0") mais correspond à une naissance impossible
(an_nais < 1900 ou an_nais > 2015), il y a incohérence avec la période 2005-2015.
Un usager né après 2015 ne peut pas être victime d'un accident entre 2005 et 2015.
Un usager né avant 1900 aurait plus de 105 ans au moment de l'accident.

FICHIERS À CRÉER :
- python/question53.py : le script de détection
- results/reponse53.txt : nb total d'incohérences, 10 premiers cas, commentaires
- results/reponse53_complet.csv : rapport complet

CONTEXTE TECHNIQUE :
- Lire depuis data/enriched/ (table usagers)
- Colonne an_nais : peut être vide, "0", ou une année entre 1900 et 2015 en théorie
- Valeurs à ignorer : vide, "0", "00", "."
- Incohérence si int(an_nais) < 1900 ou int(an_nais) > 2015
- from common import ENRICHED, ANNEE_DEBUT, ANNEE_FIN
- Style : variables et commentaires en français

APRÈS AVOIR CRÉÉ ET EXÉCUTÉ LE SCRIPT :
Mettre à jour report/dossier.md : remplacer "*(à compléter)*" sous "Question 5.3" par les 5 rubriques.
PROMPT
}

prompt_Q61() { cat <<'PROMPT'
Tu travailles sur le projet "Accidents de la route" — M2 MIMO Paris 1, Groupe 1 (2005–2015).
Le projet est dans le répertoire courant.

QUESTION 6.1 (extrait du sujet) :
Afficher le nombre d'accidents par tranche horaire d'une heure.

FICHIERS À CRÉER :
- python/question61.py : le script de visualisation
- results/reponse61.png : graphique en barres (axe x = heure 0-23, axe y = nb accidents)

CONTEXTE TECHNIQUE :
- Lire depuis data/enriched/ (table caracteristiques)
- Colonne hrmn : format HHMM — extraire l'heure : int(hrmn[:2]) ou int(hrmn) // 100
- Ignorer les hrmn vides ou invalides
- Filtrer la France métropolitaine uniquement (utiliser normaliser_dep de common.py)
- Cumuler sur toutes les années 2005-2015
- Graphique : barres verticales, titre "Accidents par tranche horaire (2005-2015)",
  labels axes, grille, taille 12×6 pouces, couleur bleue
- from common import ENRICHED, ANNEE_DEBUT, ANNEE_FIN, normaliser_dep
- Style : variables et commentaires en français, matplotlib

APRÈS AVOIR CRÉÉ ET EXÉCUTÉ LE SCRIPT :
Mettre à jour report/dossier.md : remplacer "*(à compléter)*" sous "Question 6.1" par les 5 rubriques.
PROMPT
}

prompt_Q62() { cat <<'PROMPT'
Tu travailles sur le projet "Accidents de la route" — M2 MIMO Paris 1, Groupe 1 (2005–2015).
Le projet est dans le répertoire courant.

QUESTION 6.2 (extrait du sujet) :
Fournir un graphique qui présente le nombre de tués cumulé sur la période du projet par tranche
d'âge (de 5 années) et par sexe.

FICHIERS À CRÉER :
- python/question62.py : le script de visualisation
- results/reponse62.png : graphique en barres groupées (tranches d'âge × sexe)

CONTEXTE TECHNIQUE :
- Lire depuis data/enriched/ (table usagers + table caracteristiques pour filtrer métropole)
- Tués : grav contient "2 - Tué"
- Sexe : colonne sexe ("1 - Masculin", "2 - Féminin")
- Âge = année_fichier - an_nais (utiliser l'année dans le nom de fichier, ex. usagers_2005.csv → 2005)
  Attention : an du fichier BAAC est le dernier(s) chiffre(s) (5, 10, 15), pas l'année complète
- Ignorer les an_nais vides, "0", invalides, ou donnant un âge < 0 ou > 120
- Tranches de 5 ans : [0-4], [5-9], ..., [85-89], [90+]
- Filtrer la France métropolitaine (jointure avec caracteristiques via Num_Acc + normaliser_dep)
- Graphique : barres groupées par sexe, axe x = tranches d'âge, titre clair, légende
- from common import ENRICHED, ANNEE_DEBUT, ANNEE_FIN, normaliser_dep, charger_num_acc_metropole
- Style : variables et commentaires en français, matplotlib

APRÈS AVOIR CRÉÉ ET EXÉCUTÉ LE SCRIPT :
Mettre à jour report/dossier.md : remplacer "*(à compléter)*" sous "Question 6.2" par les 5 rubriques.
PROMPT
}

prompt_Q63() { cat <<'PROMPT'
Tu travailles sur le projet "Accidents de la route" — M2 MIMO Paris 1, Groupe 1 (2005–2015).
Le projet est dans le répertoire courant.

QUESTION 6.3 (extrait du sujet) :
Quels sont les 10 départements avec le plus d'accidents ? Il faut faire l'affichage sur une carte
de France en utilisant la bibliothèque folium.

FICHIERS À CRÉER :
- python/question63.py : le script de cartographie
- results/reponse63.html : carte folium interactive
- results/reponse63.txt : tableau des 10 départements (dept, nb_accidents)

CONTEXTE TECHNIQUE :
- Lire depuis data/enriched/ (table caracteristiques)
- Filtrer métropole : normaliser_dep(dep) non None → code INSEE 2 chiffres (+ 2A/2B Corse)
- Cumuler sur 2005-2015
- Utiliser CENTROIDES_DEPARTEMENTS de common.py pour les coordonnées
- Carte folium : centrer sur la France (46.5, 2.0), zoom 6
  * Cercles proportionnels au nb d'accidents pour les 10 premiers départements
  * Popup avec nom du département et nb d'accidents
  * Tous les autres départements : petits marqueurs discrets
- from common import ENRICHED, ANNEE_DEBUT, ANNEE_FIN, normaliser_dep, CENTROIDES_DEPARTEMENTS
- Style : variables et commentaires en français, folium

APRÈS AVOIR CRÉÉ ET EXÉCUTÉ LE SCRIPT :
Mettre à jour report/dossier.md : remplacer "*(à compléter)*" sous "Question 6.3" par les 5 rubriques.
PROMPT
}

prompt_Q64() { cat <<'PROMPT'
Tu travailles sur le projet "Accidents de la route" — M2 MIMO Paris 1, Groupe 1 (2005–2015).
Le projet est dans le répertoire courant.

QUESTION 6.4 (question libre — extrait du sujet) :
Question libre à définir, utiliser au moins 2 types de table (parmi caracteristiques, lieux,
vehicules et usagers) et un type d'affichage autre que les précédents (camembert exclu).

Question définie : Distribution des accidents selon les conditions atmosphériques (atm) croisées
avec l'état de la surface (surf). Tables utilisées : caracteristiques (atm) + lieux (surf).
Affichage : heatmap (carte de chaleur) avec matplotlib/seaborn.

FICHIERS À CRÉER :
- python/question64.py : le script de visualisation
- results/reponse64.png : heatmap atm × surf

CONTEXTE TECHNIQUE :
- Lire depuis data/enriched/
- Joindre caracteristiques et lieux via Num_Acc
- Filtrer métropole via normaliser_dep
- Cumuler sur 2005-2015
- Heatmap : colonnes = valeurs de surf, lignes = valeurs de atm, cellules = nb accidents
  Afficher les libellés abrégés (premiers mots) pour lisibilité
- from common import ENRICHED, ANNEE_DEBUT, ANNEE_FIN, normaliser_dep
- Style : variables et commentaires en français, matplotlib + seaborn si disponible

APRÈS AVOIR CRÉÉ ET EXÉCUTÉ LE SCRIPT :
Mettre à jour report/dossier.md : remplacer "*(à compléter)*" sous "Question 6.4" par les 5 rubriques.
PROMPT
}

prompt_Q65() { cat <<'PROMPT'
Tu travailles sur le projet "Accidents de la route" — M2 MIMO Paris 1, Groupe 1 (2005–2015).
Le projet est dans le répertoire courant.

QUESTION 6.5 (facultative — extrait du sujet) :
Reprendre la question 6.3 et faire un gif animé de la carte par année.

Note : faire une carte PNG par année (avec matplotlib, pas folium) puis assembler en GIF avec Pillow.

FICHIERS À CRÉER :
- python/question65.py : le script de génération du GIF
- results/reponse65.gif : carte animée (une frame par année 2005-2015)

CONTEXTE TECHNIQUE :
- Pour chaque année 2005-2015 :
  * Compter les accidents par département (filtrer métropole avec normaliser_dep)
  * Générer une carte matplotlib avec des cercles proportionnels au nb d'accidents
    Utiliser CENTROIDES_DEPARTEMENTS pour les positions
  * Sauvegarder en PNG temporaire dans results/
- Assembler les 11 PNG en GIF avec Pillow (PIL) :
  * from PIL import Image
  * images = [Image.open(f) for f in liste_png]
  * images[0].save('results/reponse65.gif', save_all=True, append_images=images[1:], duration=800, loop=0)
- Supprimer les PNG temporaires après création du GIF
- from common import ENRICHED, ANNEE_DEBUT, ANNEE_FIN, normaliser_dep, CENTROIDES_DEPARTEMENTS
- Style : variables et commentaires en français

APRÈS AVOIR CRÉÉ ET EXÉCUTÉ LE SCRIPT :
Mettre à jour report/dossier.md : remplacer "*(à compléter)*" sous "Question 6.5" par les 5 rubriques.
PROMPT
}

# ─── Sélection du prompt ──────────────────────────────────────────────────────

get_prompt() {
  case "$1" in
    Q11) prompt_Q11 ;; Q12) prompt_Q12 ;; Q13) prompt_Q13 ;;
    Q21) prompt_Q21 ;; Q22) prompt_Q22 ;; Q23) prompt_Q23 ;; Q24) prompt_Q24 ;;
    Q31) prompt_Q31 ;; Q41) prompt_Q41 ;;
    Q51) prompt_Q51 ;; Q52) prompt_Q52 ;; Q53) prompt_Q53 ;;
    Q61) prompt_Q61 ;; Q62) prompt_Q62 ;; Q63) prompt_Q63 ;;
    Q64) prompt_Q64 ;; Q65) prompt_Q65 ;;
  esac
}

# ─── Appel de l'agent ─────────────────────────────────────────────────────────

run_cc() {
  local prompt="$1"
  for attempt in 1 2 3 4 5; do
    if cd "$PROJECT" && claude -p --dangerously-skip-permissions "$prompt"; then
      return 0
    fi
    log "Claude — tentative $attempt échouée (limite API?), attente 5 min..."
    sleep 300
  done
  return 1
}

# ─── Boucle principale (questions cc uniquement — oc délégué à run_oc.sh) ────

total=${#QUESTIONS[@]}
log "Pipeline CC démarré — questions cc uniquement, depuis l'index $CURRENT_IDX"

for i in $(seq "$CURRENT_IDX" "$((total - 1))"); do
  Q="${QUESTIONS[$i]}"
  SCRIPT="${SCRIPTS[$i]}"
  AGENT="${AGENTS[$i]}"

  # Déléguer les questions oc à run_oc.sh
  if [ "$AGENT" = "oc" ]; then
    log "Skipping $Q (délégué à run_oc.sh)"
    echo "$((i+1))" > "$STATE_FILE"
    continue
  fi

  log "=== [$((i+1))/$total] $Q (claude) ==="

  PROMPT=$(get_prompt "$Q")
  run_cc "$PROMPT"

  # Exécuter le script s'il a été créé mais pas encore lancé
  SCRIPT_PATH="$PROJECT/python/${SCRIPT}.py"
  if [ -f "$SCRIPT_PATH" ]; then
    log "Exécution de $SCRIPT..."
    cd "$PROJECT" && python3 "python/${SCRIPT}.py" 2>&1 | tee -a "$LOG_FILE" || true
  else
    log "AVERTISSEMENT : $SCRIPT_PATH non trouvé après appel de l'agent"
  fi

  # Vérifier qu'un fichier résultat a été créé (reponse11, reponse12, etc.)
  QNUM="${Q:1}"  # Q11 → 11, Q65 → 65
  if ! ls "$PROJECT/results/reponse${QNUM}"* 2>/dev/null | grep -q .; then
    log "ERREUR : aucun fichier results/reponse${QNUM}* pour $Q"
    echo "$i" > "$STATE_FILE"
    exit 1
  fi

  # Commit
  cd "$PROJECT"
  git add python/ results/ report/dossier.md 2>/dev/null || true
  git commit -m "feat: ${Q} complété (agent: $AGENT)" || log "Rien à commiter pour $Q"

  # Avancer l'état
  echo "$((i+1))" > "$STATE_FILE"
  log "--- $Q TERMINÉ ---"
done

log "=== PIPELINE TERMINÉ ==="
rm -f "$STATE_FILE"
