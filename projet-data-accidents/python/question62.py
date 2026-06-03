"""Question 6.2 — Tués cumulés par tranche d'âge (5 ans) et par sexe.

On compte, cumulé sur toute la période 2005-2015 (Groupe 1), le nombre
d'usagers TUÉS, ventilé par tranche d'âge de 5 ans et par sexe, puis on en
fait un graphique en barres groupées.

Source : data/enriched/usagers_<annee>.csv (un usager par ligne).
  - grav  : gravité — on ne garde que « 2 - Tué ».
  - sexe  : « 1 - Masculin » ou « 2 - Féminin ».
  - an_nais : année de naissance (millésime à 4 chiffres, ex. 1976).

Calcul de l'âge :
  L'âge est obtenu par différence entre l'année du fichier et l'année de
  naissance : age = annee_fichier - an_nais. L'année du fichier est lue
  directement dans le nom de fichier (usagers_2005.csv → 2005), qui est ici
  un millésime complet ; aucune reconstruction n'est nécessaire.

  an_nais ignorée si : vide, non numérique, égale à « 0 », ou donnant un âge
  hors de l'intervalle plausible [0, 120].

Tranches d'âge (5 ans) :
  [0-4], [5-9], …, [85-89], puis une dernière tranche ouverte [90+].
  Soit 18 tranches de 5 ans + 1 tranche « 90+ » = 19 tranches.

Filtrage :
  France métropolitaine uniquement. La table usagers ne porte pas le
  département : on récupère, pour chaque année, l'ensemble des Num_Acc
  métropolitains via charger_num_acc_metropole (jointure sur la table
  caractéristiques) et on ne garde que les usagers de ces accidents.

Sortie :
  - results/reponse62.png : barres groupées (x = tranche d'âge, 2 barres
    par tranche = hommes / femmes, y = nombre de tués cumulés).
"""

import csv
import sys

import matplotlib

matplotlib.use("Agg")  # rendu hors écran : on écrit directement un fichier PNG
import matplotlib.pyplot as plt

from common import (
    ENRICHED,
    RESULTS,
    ANNEE_DEBUT,
    ANNEE_FIN,
    charger_num_acc_metropole,
)

# Bornes des tranches : 19 tranches au total (18 de 5 ans + « 90+ »).
NB_TRANCHES = 19
LABELS_TRANCHES = [f"{5 * i}-{5 * i + 4}" for i in range(18)] + ["90+"]


def indice_tranche(age: int) -> int:
    """Renvoie l'indice (0 à 18) de la tranche de 5 ans contenant cet âge.

    Les âges de 90 ans et plus tombent tous dans la dernière tranche « 90+ ».
    """
    if age >= 90:
        return 18
    return age // 5


def compter_tues_par_age_sexe() -> tuple[list[int], list[int]]:
    """Cumule, sur 2005-2015, le nombre de tués par tranche d'âge et par sexe.

    Renvoie deux listes de 19 entiers (hommes, femmes) : indice i = nombre de
    tués de la tranche d'âge i. France métropolitaine uniquement.
    """
    tues_hommes = [0] * NB_TRANCHES
    tues_femmes = [0] * NB_TRANCHES
    nb_age_ignore = 0  # an_nais vide / invalide / âge hors [0, 120]
    nb_sexe_ignore = 0  # sexe non renseigné parmi les tués

    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        print(f"[..]   {annee}")
        # Num_Acc métropolitains de l'année (jointure avec caractéristiques).
        num_acc_metropole = charger_num_acc_metropole(annee)

        chemin = ENRICHED / f"usagers_{annee}.csv"
        with chemin.open("r", encoding="utf-8", newline="") as f:
            lecteur = csv.reader(f)
            entete = next(lecteur)
            idx_num = entete.index("Num_Acc")
            idx_grav = entete.index("grav")
            idx_sexe = entete.index("sexe")
            idx_nais = entete.index("an_nais")
            for ligne in lecteur:
                # On ne garde que les usagers TUÉS.
                if ligne[idx_grav] != "2 - Tué":
                    continue
                # … et seulement ceux d'accidents en France métropolitaine.
                if ligne[idx_num] not in num_acc_metropole:
                    continue

                # Âge = année du fichier - année de naissance.
                an_nais = ligne[idx_nais].strip()
                if not an_nais.isdigit() or an_nais == "0":
                    nb_age_ignore += 1
                    continue
                age = annee - int(an_nais)
                if age < 0 or age > 120:
                    nb_age_ignore += 1
                    continue

                tranche = indice_tranche(age)
                sexe = ligne[idx_sexe]
                if sexe == "1 - Masculin":
                    tues_hommes[tranche] += 1
                elif sexe == "2 - Féminin":
                    tues_femmes[tranche] += 1
                else:
                    nb_sexe_ignore += 1

        cumul = sum(tues_hommes) + sum(tues_femmes)
        print(f"  [OK] {annee} : {cumul} tués cumulés (métropole)")

    print(f"\nTués au sexe non renseigné (ignorés) : {nb_sexe_ignore}")
    print(f"Tués à l'âge non exploitable (ignorés) : {nb_age_ignore}")
    return tues_hommes, tues_femmes


def tracer_graphique(tues_hommes: list[int], tues_femmes: list[int]) -> None:
    """Trace et enregistre les barres groupées dans results/reponse62.png."""
    x = list(range(NB_TRANCHES))
    largeur = 0.4  # largeur d'une barre ; deux barres par tranche

    plt.figure(figsize=(14, 7))
    # Hommes décalés à gauche, femmes à droite, autour de la position centrale.
    plt.bar([i - largeur / 2 for i in x], tues_hommes, largeur,
            label="Masculin", color="tab:blue")
    plt.bar([i + largeur / 2 for i in x], tues_femmes, largeur,
            label="Féminin", color="tab:red")

    plt.title("Tués cumulés par tranche d'âge et par sexe (2005-2015)")
    plt.xlabel("Tranche d'âge (ans)")
    plt.ylabel("Nombre de tués cumulés")
    plt.xticks(x, LABELS_TRANCHES, rotation=45, ha="right")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()

    chemin = RESULTS / "reponse62.png"
    plt.savefig(chemin, dpi=150)
    plt.close()
    print(f"Graphique écrit dans {chemin}")


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    tues_hommes, tues_femmes = compter_tues_par_age_sexe()

    total_h = sum(tues_hommes)
    total_f = sum(tues_femmes)
    total = total_h + total_f
    print(f"\nTotal tués (métropole, 2005-2015) : {total}")
    print(f"  dont hommes : {total_h} ({100 * total_h / total:.1f} %)")
    print(f"  dont femmes : {total_f} ({100 * total_f / total:.1f} %)")

    # Tranche la plus meurtrière, tous sexes confondus.
    cumul_par_tranche = [h + f for h, f in zip(tues_hommes, tues_femmes)]
    i_max = cumul_par_tranche.index(max(cumul_par_tranche))
    print(f"Tranche la plus touchée : {LABELS_TRANCHES[i_max]} ans "
          f"({cumul_par_tranche[i_max]} tués)")

    tracer_graphique(tues_hommes, tues_femmes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
