"""Question 3.1 — Répartition en % des valeurs des attributs énumérés (usagers).

Pour chacun des attributs énumérés du fichier des usagers, on calcule la
répartition en pourcentage de ses valeurs, cumulée sur toute la période
2005-2015 (Groupe 1).

Attributs traités (cf. schema_baac.md §3 et Q1.3) :
    catu, grav, sexe, trajet, secu, locp, actp, etatp

Remarque importante sur l'état des données :
  - catu, grav, sexe, trajet, locp, actp, etatp ont déjà été *enrichis* en
    Q1.3 : dans data/enriched/ leur valeur est de la forme « code - libellé »
    (ex. « 1 - Conducteur »). Les codes non documentés ou absents ("", ".",
    "-1") y figurent tels quels, sans libellé.
  - secu n'a PAS été enrichi (c'est un champ à 2 caractères, 1er = équipement,
    2e = utilisation). On le lit donc comme une chaîne brute (ex. "11", "12")
    et on lui adjoint un décodage lisible au moment de l'affichage.

Méthode : un simple comptage. Pour chaque attribut on tient un Counter des
valeurs rencontrées ligne à ligne ; le dénominateur du pourcentage est le
nombre total d'usagers (chaque ligne fournit exactement une valeur par
attribut). L'affichage est trié par pourcentage décroissant.

Sortie :
  - results/reponse31.txt : un tableau par attribut + commentaires.
"""

import csv
import sys
from collections import Counter

from common import ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN

# Attributs énumérés du fichier usagers, dans l'ordre de la documentation.
ATTRIBUTS = ["catu", "grav", "sexe", "trajet", "secu", "locp", "actp", "etatp"]

# Décodage de secu (2 caractères) — cf. schema_baac.md §3.
# 1er caractère = équipement de sécurité, 2e caractère = utilisation.
SECU_EQUIPEMENT = {
    "1": "Ceinture",
    "2": "Casque",
    "3": "Dispositif enfants",
    "4": "Équipement réfléchissant",
    "9": "Autre",
}
SECU_USAGE = {
    "1": "Oui",
    "2": "Non",
    "3": "Non déterminable",
}

# Marqueurs de valeur absente (mêmes conventions qu'en Q1.3).
MARQUEURS_ABSENTS = {"", ".", "-1"}


def decoder_secu(code: str) -> str:
    """Renvoie un libellé lisible pour un code secu à 2 caractères.

    Renvoie une mention explicite si le code est absent ou hors documentation.
    """
    s = code.strip()
    if s in MARQUEURS_ABSENTS:
        return "(valeur absente)"
    if len(s) == 2 and s[0] in SECU_EQUIPEMENT and s[1] in SECU_USAGE:
        return f"{SECU_EQUIPEMENT[s[0]]} - {SECU_USAGE[s[1]]}"
    return "(code hors documentation)"


def afficher_valeur(attribut: str, valeur: str) -> str:
    """Forme lisible d'une valeur pour le tableau.

    Pour secu (brut), on ajoute son décodage. Pour les autres attributs, la
    valeur enrichie est déjà lisible ; on signale juste les valeurs absentes.
    """
    if attribut == "secu":
        return f"{valeur!r:<6} → {decoder_secu(valeur)}"
    if valeur.strip() in MARQUEURS_ABSENTS:
        return f"{valeur!r} (valeur absente)"
    return valeur


def compter_attributs() -> tuple[dict[str, Counter], int]:
    """Cumule, sur 2005-2015, le décompte des valeurs de chaque attribut.

    Renvoie (compteurs, nb_usagers) où compteurs[attribut] est un Counter
    valeur → effectif, et nb_usagers le nombre total de lignes lues.
    """
    compteurs: dict[str, Counter] = {attr: Counter() for attr in ATTRIBUTS}
    nb_usagers = 0

    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        chemin = ENRICHED / f"usagers_{annee}.csv"
        print(f"[..]   {annee}")
        with chemin.open("r", encoding="utf-8", newline="") as f:
            lecteur = csv.reader(f)
            entete = next(lecteur)
            idx = {attr: entete.index(attr) for attr in ATTRIBUTS}
            for ligne in lecteur:
                nb_usagers += 1
                for attr in ATTRIBUTS:
                    compteurs[attr][ligne[idx[attr]]] += 1
        print(f"  [OK] {annee} : {nb_usagers} usagers cumulés")

    return compteurs, nb_usagers


def ecrire_rapport(compteurs: dict[str, Counter], nb_usagers: int) -> None:
    """Écrit results/reponse31.txt : un tableau trié par % décroissant."""
    chemin = RESULTS / "reponse31.txt"
    with chemin.open("w", encoding="utf-8") as f:
        f.write("Question 3.1 — Répartition en % des attributs énumérés "
                "(usagers)\n")
        f.write("=" * 68 + "\n\n")
        f.write(f"Période : {ANNEE_DEBUT}-{ANNEE_FIN} (Groupe 1)\n")
        f.write(f"Source  : {ENRICHED}\n")
        f.write(f"Total usagers cumulés : {nb_usagers}\n\n")
        f.write("Pour chaque attribut, le dénominateur du pourcentage est le\n")
        f.write("nombre total d'usagers ; les valeurs sont triées par effectif\n")
        f.write("décroissant. secu est un code brut à 2 caractères (1er =\n")
        f.write("équipement, 2e = utilisation), décodé pour la lisibilité.\n\n")

        for attr in ATTRIBUTS:
            compteur = compteurs[attr]
            nb_valeurs = len(compteur)
            f.write(f"Attribut « {attr} »  ({nb_valeurs} valeur(s) distincte(s))\n")
            f.write("-" * 68 + "\n")
            # Tri par effectif décroissant, puis par valeur pour stabilité.
            lignes_triees = sorted(
                compteur.items(), key=lambda kv: (-kv[1], kv[0])
            )
            for valeur, effectif in lignes_triees:
                pct = effectif / nb_usagers * 100
                f.write(
                    f"  {pct:6.2f} %  {effectif:>9}  "
                    f"{afficher_valeur(attr, valeur)}\n"
                )
            f.write("\n")

    print(f"\nRapport écrit dans {chemin}")


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    compteurs, nb_usagers = compter_attributs()
    ecrire_rapport(compteurs, nb_usagers)
    print(f"Total : {nb_usagers} usagers, {len(ATTRIBUTS)} attributs analysés")
    return 0


if __name__ == "__main__":
    sys.exit(main())
