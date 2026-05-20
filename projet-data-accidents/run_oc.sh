#!/usr/bin/env bash
# Pipeline OpenCode — questions Q31, Q41, Q53, Q61-Q65
# Attend que data/enriched/ soit prêt (Q13 doit finir d'abord), puis lance en parallèle du CC.
set -euo pipefail

PROJECT=/home/rayan/Documents/Projets/projet-data-accidents
STATE_FILE="$PROJECT/.state-oc"
LOG_FILE="$PROJECT/pipeline-oc.log"

QUESTIONS=(Q31 Q41 Q53 Q61 Q62 Q63 Q64 Q65)
SCRIPTS=(question31 question41 question53 question61 question62 question63 question64 question65)

CURRENT_IDX=0
[ -f "$STATE_FILE" ] && CURRENT_IDX=$(cat "$STATE_FILE")

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILE"; }

# ─── Attendre les données enrichies ──────────────────────────────────────────

log "Pipeline OC démarré — attente des données enrichies (Q13)..."
until [ -f "$PROJECT/data/enriched/caracteristiques_2005.csv" ]; do
  sleep 30
done
log "Données enrichies disponibles — démarrage des questions oc."

# ─── Prompts ─────────────────────────────────────────────────────────────────

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
Question libre à définir, utiliser au moins 2 types de table et un type d'affichage autre que
les précédents (camembert exclu).

Question définie : Distribution des accidents selon les conditions atmosphériques (atm) croisées
avec l'état de la surface (surf). Tables : caracteristiques (atm) + lieux (surf). Heatmap.

FICHIERS À CRÉER :
- python/question64.py : le script de visualisation
- results/reponse64.png : heatmap atm × surf

CONTEXTE TECHNIQUE :
- Lire depuis data/enriched/
- Joindre caracteristiques et lieux via Num_Acc
- Filtrer métropole via normaliser_dep
- Cumuler sur 2005-2015
- Heatmap : lignes = valeurs de atm, colonnes = valeurs de surf, cellules = nb accidents
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

Note : faire une carte PNG par année (avec matplotlib) puis assembler en GIF avec Pillow.

FICHIERS À CRÉER :
- python/question65.py : le script de génération du GIF
- results/reponse65.gif : carte animée (une frame par année 2005-2015)

CONTEXTE TECHNIQUE :
- Pour chaque année 2005-2015 :
  * Compter les accidents par département (filtrer métropole avec normaliser_dep)
  * Générer une carte matplotlib avec des cercles proportionnels au nb d'accidents
    Utiliser CENTROIDES_DEPARTEMENTS pour les positions
  * Sauvegarder en PNG temporaire dans results/
- Assembler les 11 PNG en GIF avec Pillow :
  from PIL import Image
  images = [Image.open(f) for f in liste_png]
  images[0].save('results/reponse65.gif', save_all=True, append_images=images[1:], duration=800, loop=0)
- Supprimer les PNG temporaires après création du GIF
- from common import ENRICHED, ANNEE_DEBUT, ANNEE_FIN, normaliser_dep, CENTROIDES_DEPARTEMENTS
- Style : variables et commentaires en français

APRÈS AVOIR CRÉÉ ET EXÉCUTÉ LE SCRIPT :
Mettre à jour report/dossier.md : remplacer "*(à compléter)*" sous "Question 6.5" par les 5 rubriques.
PROMPT
}

get_prompt() {
  case "$1" in
    Q31) prompt_Q31 ;; Q41) prompt_Q41 ;; Q53) prompt_Q53 ;;
    Q61) prompt_Q61 ;; Q62) prompt_Q62 ;; Q63) prompt_Q63 ;;
    Q64) prompt_Q64 ;; Q65) prompt_Q65 ;;
  esac
}

# ─── Boucle principale ────────────────────────────────────────────────────────

total=${#QUESTIONS[@]}
log "Lancement — $total questions oc, depuis l'index $CURRENT_IDX"

for i in $(seq "$CURRENT_IDX" "$((total - 1))"); do
  Q="${QUESTIONS[$i]}"
  SCRIPT="${SCRIPTS[$i]}"

  log "=== [$((i+1))/$total] $Q (opencode) ==="

  PROMPT=$(get_prompt "$Q")

  # Appel opencode avec retry
  for attempt in 1 2 3; do
    if cd "$PROJECT" && opencode run --dangerously-skip-permissions "$PROMPT"; then
      break
    fi
    log "OpenCode — tentative $attempt échouée, attente 2 min..."
    sleep 120
  done

  # Exécuter le script si créé
  if [ -f "$PROJECT/python/${SCRIPT}.py" ]; then
    log "Exécution de $SCRIPT..."
    cd "$PROJECT" && python3 "python/${SCRIPT}.py" 2>&1 | tee -a "$LOG_FILE" || true
  else
    log "AVERTISSEMENT : python/${SCRIPT}.py non trouvé"
  fi

  # Vérifier le résultat
  QNUM="${Q:1}"
  if ! ls "$PROJECT/results/reponse${QNUM}"* 2>/dev/null | grep -q .; then
    log "ERREUR : aucun fichier results/reponse${QNUM}* pour $Q"
    echo "$i" > "$STATE_FILE"
    exit 1
  fi

  # Commit (avec lock basique pour éviter conflit avec run_pipeline.sh)
  cd "$PROJECT"
  sleep 2
  git add python/ results/ report/dossier.md 2>/dev/null || true
  git commit -m "feat: $Q complété (opencode)" || log "Rien à commiter pour $Q"

  echo "$((i+1))" > "$STATE_FILE"
  log "--- $Q TERMINÉ ---"
done

log "=== PIPELINE OC TERMINÉ ==="
rm -f "$STATE_FILE"
