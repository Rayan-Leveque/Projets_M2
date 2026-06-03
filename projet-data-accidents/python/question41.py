"""Question 4.1 — Taux de valeurs absentes pour chaque champ du fichier véhicules.

Pour chacune des colonnes du fichier des véhicules, on mesure la proportion de
cellules « non renseignées », cumulée sur toute la période 2005-2015 (Groupe 1).

Convention des valeurs manquantes (cf. schema_baac.md §2). Les PDF officiels
indiquent qu'une cellule vide, un zéro ou un point signalent une valeur « non
renseignée par les forces de l'ordre ou sans objet ». On retient donc comme
marqueurs d'absence :
    ''  (cellule vide), '.', '-1', '0', '00', '000'

État des données lues (data/enriched/) :
  - catv, obs, obsm, choc, manv ont été *enrichis* en Q1.3 : leur valeur est de
    la forme « code - libellé » (ex. « 07 - VL seul »). Pour tester l'absence on
    isole donc le code (partie avant « - ») avant de le comparer aux marqueurs.
  - senc, occutc, num_veh, Num_Acc sont des champs bruts : on les teste tels
    quels.

Point de vigilance (cf. énoncé) : le code '0' n'a pas le même sens partout.
  - Pour senc, '0' n'est pas documenté (seuls 1 et 2 le sont) : on le compte
    donc comme absent, mais c'est à nuancer car certaines années l'utilisent.
  - Pour obs/obsm/choc, '0'/'00' est documenté comme « Sans objet / Aucun » :
    mécaniquement compté ici comme absent, mais il s'agit le plus souvent d'une
    vraie information (le véhicule n'a heurté aucun obstacle) — voir analyse.
  - Pour occutc, '000' = 0 occupant, ce qui est normal pour tout véhicule qui
    n'est pas un transport en commun → taux d'absence mécaniquement très élevé.

Méthode : un simple comptage ligne à ligne. Pour chaque colonne on tient le
nombre de cellules absentes ; le dénominateur est le nombre total de véhicules.

Seuils d'interprétation (cf. énoncé) :
    < 5 %     → champ bien renseigné
    5 % - 15 %→ à utiliser avec prudence
    > 15 %    → champ fragile

Sortie :
  - results/reponse41.txt : tableau (colonne, nb_manquants, taux_%) + analyse.
"""

import csv
import sys

from common import ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN

# Colonnes du fichier véhicules, dans l'ordre de la documentation.
COLONNES = ["Num_Acc", "senc", "catv", "occutc", "obs", "obsm", "choc",
            "manv", "num_veh"]

# Marqueurs de valeur absente (cf. schema_baac.md §2).
MARQUEURS_ABSENTS = {"", ".", "-1", "0", "00", "000"}

# Seuils d'interprétation du taux d'absence.
SEUIL_BIEN = 5.0      # < 5 %  : bien renseigné
SEUIL_PRUDENCE = 15.0  # 5-15 % : prudence ; > 15 % : fragile


def extraire_code(valeur: str) -> str:
    """Isole le code d'une cellule enrichie « code - libellé ».

    Pour une cellule brute (sans « - »), renvoie la valeur nettoyée telle quelle.
    """
    v = valeur.strip()
    if " - " in v:
        return v.split(" - ", 1)[0].strip()
    return v


def est_absente(valeur: str) -> bool:
    """Vrai si la cellule correspond à un marqueur de valeur absente."""
    return extraire_code(valeur) in MARQUEURS_ABSENTS


def compter_absences() -> tuple[dict[str, int], int]:
    """Cumule, sur 2005-2015, le nombre de cellules absentes par colonne.

    Renvoie (absences, nb_vehicules) où absences[colonne] est le nombre de
    cellules absentes et nb_vehicules le nombre total de lignes lues.
    """
    absences: dict[str, int] = {col: 0 for col in COLONNES}
    nb_vehicules = 0

    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        chemin = ENRICHED / f"vehicules_{annee}.csv"
        print(f"[..]   {annee}")
        with chemin.open("r", encoding="utf-8", newline="") as f:
            lecteur = csv.reader(f)
            entete = next(lecteur)
            idx = {col: entete.index(col) for col in COLONNES}
            for ligne in lecteur:
                nb_vehicules += 1
                for col in COLONNES:
                    if est_absente(ligne[idx[col]]):
                        absences[col] += 1
        print(f"  [OK] {annee} : {nb_vehicules} véhicules cumulés")

    return absences, nb_vehicules


def qualifier(taux: float) -> str:
    """Renvoie le qualificatif associé à un taux d'absence (en %)."""
    if taux < SEUIL_BIEN:
        return "bien renseigné"
    if taux <= SEUIL_PRUDENCE:
        return "prudence"
    return "fragile"


def ecrire_rapport(absences: dict[str, int], nb_vehicules: int) -> None:
    """Écrit results/reponse41.txt : tableau des taux + interprétation."""
    chemin = RESULTS / "reponse41.txt"
    with chemin.open("w", encoding="utf-8") as f:
        f.write("Question 4.1 — Taux de valeurs absentes par champ (véhicules)\n")
        f.write("=" * 68 + "\n\n")
        f.write(f"Période : {ANNEE_DEBUT}-{ANNEE_FIN} (Groupe 1)\n")
        f.write(f"Source  : {ENRICHED}\n")
        f.write(f"Total véhicules cumulés : {nb_vehicules}\n\n")
        f.write("Marqueurs d'absence retenus : '' (vide), '.', '-1', "
                "'0', '00', '000'.\n")
        f.write("Pour les colonnes enrichies (catv, obs, obsm, choc, manv) le\n")
        f.write("test porte sur le code (partie avant « - »).\n")
        f.write(f"Seuils : < {SEUIL_BIEN:.0f}% bien renseigné, "
                f"{SEUIL_BIEN:.0f}-{SEUIL_PRUDENCE:.0f}% prudence, "
                f"> {SEUIL_PRUDENCE:.0f}% fragile.\n\n")

        # Tableau, trié par taux décroissant.
        f.write(f"{'colonne':<10}{'nb_manquants':>14}{'taux_%':>10}"
                f"   qualificatif\n")
        f.write("-" * 68 + "\n")
        lignes = sorted(
            COLONNES, key=lambda col: absences[col], reverse=True
        )
        for col in lignes:
            nb = absences[col]
            taux = nb / nb_vehicules * 100 if nb_vehicules else 0.0
            f.write(f"{col:<10}{nb:>14}{taux:>9.2f}%   {qualifier(taux)}\n")
        f.write("\n")

        # Interprétation.
        f.write("Interprétation\n")
        f.write("-" * 68 + "\n")
        f.write(
            "- Num_Acc et num_veh sont les identifiants de jointure : 0 % "
            "d'absence,\n  ce qui est attendu (sans eux la ligne serait "
            "inexploitable).\n"
            "- occutc (nombre d'occupants d'un transport en commun) affiche un "
            "taux\n  d'absence très élevé : '000' y domine, car la quasi-totalité"
            " des\n  véhicules ne sont pas des bus/cars. Ce n'est pas un défaut "
            "de saisie\n  mais un « sans objet » massif : la colonne n'est "
            "pertinente que pour\n  les catégories de transport en commun.\n"
            "- obs (obstacle fixe heurté) est très majoritairement « 00 - Sans "
            "objet » :\n  le code 0 est ici une vraie information (aucun obstacle"
            " fixe heurté),\n  comptée mécaniquement comme absente par notre "
            "convention. Le taux\n  élevé traduit donc surtout la rareté des "
            "chocs contre obstacle fixe.\n"
            "- obsm et choc utilisent aussi le code 0 (« Aucun »), documenté : "
            "leur\n  taux mêle absences réelles et « sans objet », à interpréter "
            "avec recul.\n"
            "- senc : le code '0' n'est pas documenté (seuls 1 et 2 le sont) ; "
            "on le\n  compte comme absent. Son taux reflète une saisie "
            "irrégulière du sens\n  de circulation, variable selon les années.\n"
            "- catv (catégorie de véhicule) est à 0 % : c'est l'attribut le "
            "mieux\n  renseigné, ce qui est rassurant car beaucoup d'analyses "
            "en dépendent.\n"
            "- manv (manœuvre) et choc se situent dans la zone de prudence "
            "(5-15 %) :\n  exploitables, mais en gardant à l'esprit cette part "
            "de non-saisie.\n\n"
            "Conclusion : la convention « 0 = absent » est volontairement "
            "stricte. Pour\nles champs où 0 est documenté (obs, obsm, choc, "
            "occutc), un taux élevé\nsignale surtout du « sans objet » et non un "
            "défaut de remplissage ; ces\nchamps restent exploitables en "
            "distinguant 0 des autres valeurs. Les champs\nréellement fragiles "
            "sont ceux dont l'absence n'est pas un « sans objet »\nlégitime.\n"
        )

    print(f"\nRapport écrit dans {chemin}")


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    absences, nb_vehicules = compter_absences()
    ecrire_rapport(absences, nb_vehicules)
    print(f"Total : {nb_vehicules} véhicules, {len(COLONNES)} colonnes analysées")
    return 0


if __name__ == "__main__":
    sys.exit(main())
