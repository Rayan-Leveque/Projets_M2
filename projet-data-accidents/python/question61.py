"""Question 6.1 — Nombre d'accidents par tranche horaire d'une heure.

On compte, cumulé sur toute la période 2005-2015 (Groupe 1), le nombre
d'accidents survenus dans chacune des 24 tranches horaires d'une heure
(0h, 1h, …, 23h), puis on en fait un graphique en barres.

Source : data/enriched/caracteristiques_<annee>.csv (un accident par ligne).

Extraction de l'heure :
  La colonne hrmn est au format HHMM mais SANS zéro de tête : « 1900 » vaut
  19h00, mais « 300 » vaut 3h00 (et non 30h) et « 30 » vaut 0h30. On obtient
  donc l'heure de façon fiable par division entière : int(hrmn) // 100.
  (Faire int(hrmn[:2]) serait faux pour les valeurs à moins de 4 chiffres.)

Filtrage :
  - on ne garde que la France métropolitaine, via normaliser_dep (qui exclut
    les DOM et les départements non métropolitains) ;
  - les hrmn vides ou non numériques sont ignorées.

Sortie :
  - results/reponse61.png : graphique en barres (x = heure 0-23, y = nb accidents).
"""

import csv
import sys

import matplotlib

matplotlib.use("Agg")  # rendu hors écran : on écrit directement un fichier PNG
import matplotlib.pyplot as plt

from common import ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN, normaliser_dep


def compter_par_heure() -> list[int]:
    """Cumule, sur 2005-2015, le nombre d'accidents par tranche horaire.

    Renvoie une liste de 24 entiers : indice i = nombre d'accidents dont
    l'heure de survenue est i (0 ≤ i ≤ 23). France métropolitaine uniquement.
    """
    # accidents_par_heure[h] = nombre d'accidents survenus à l'heure h.
    accidents_par_heure = [0] * 24
    nb_ignores = 0  # hrmn vide ou invalide

    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        chemin = ENRICHED / f"caracteristiques_{annee}.csv"
        print(f"[..]   {annee}")
        with chemin.open("r", encoding="utf-8", newline="") as f:
            lecteur = csv.reader(f)
            entete = next(lecteur)
            idx_hrmn = entete.index("hrmn")
            idx_dep = entete.index("dep")
            for ligne in lecteur:
                # On ne garde que la France métropolitaine.
                if normaliser_dep(ligne[idx_dep]) is None:
                    continue
                hrmn = ligne[idx_hrmn].strip()
                # hrmn doit être numérique ; on ignore les valeurs vides/invalides.
                if not hrmn.isdigit():
                    nb_ignores += 1
                    continue
                heure = int(hrmn) // 100
                if 0 <= heure <= 23:
                    accidents_par_heure[heure] += 1
                else:
                    nb_ignores += 1
        total_cumule = sum(accidents_par_heure)
        print(f"  [OK] {annee} : {total_cumule} accidents cumulés")

    print(f"\nValeurs hrmn ignorées (vides/invalides) : {nb_ignores}")
    return accidents_par_heure


def tracer_graphique(accidents_par_heure: list[int]) -> None:
    """Trace et enregistre le graphique en barres dans results/reponse61.png."""
    heures = list(range(24))

    plt.figure(figsize=(12, 6))
    plt.bar(heures, accidents_par_heure, color="tab:blue")
    plt.title("Accidents par tranche horaire (2005-2015)")
    plt.xlabel("Heure de la journée")
    plt.ylabel("Nombre d'accidents")
    plt.xticks(heures)  # une graduation par heure (0 à 23)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()

    chemin = RESULTS / "reponse61.png"
    plt.savefig(chemin, dpi=150)
    plt.close()
    print(f"Graphique écrit dans {chemin}")


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    accidents_par_heure = compter_par_heure()

    total = sum(accidents_par_heure)
    heure_pic = accidents_par_heure.index(max(accidents_par_heure))
    print(f"\nTotal accidents (métropole, 2005-2015) : {total}")
    print(f"Heure la plus accidentogène : {heure_pic}h "
          f"({accidents_par_heure[heure_pic]} accidents)")

    tracer_graphique(accidents_par_heure)
    return 0


if __name__ == "__main__":
    sys.exit(main())
