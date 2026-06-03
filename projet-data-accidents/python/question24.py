"""Question 2.4 (facultative) — Cardinalité : chaque accident sur un seul lieu.

Vérifie par programme que chaque accident décrit dans
`caracteristiques_{annee}.csv` se déroule sur **un et un seul** lieu, c.-à-d.
qu'il possède exactement une ligne correspondante dans `lieux_{annee}.csv`
(via la clé `Num_Acc`).

C'est le pendant « cardinalité » de Q2.3 : Q2.3 vérifiait que tout lieu
référence un accident existant (sens lieux → caracteristiques) ; ici on
vérifie le sens inverse et le *nombre* de lieux par accident.

Méthode année par année :
  1. On parcourt lieux_{annee}.csv et on compte, pour chaque Num_Acc, son
     nombre d'occurrences (un `Counter`).
  2. On parcourt caracteristiques_{annee}.csv. Pour chaque accident on lit
     son nombre de lieux dans le compteur :
       - nb_lieux == 1  → cas normal (un et un seul lieu).
       - nb_lieux == 0  → accident sans aucun lieu (violation).
       - nb_lieux >= 2  → accident décrit sur plusieurs lieux (violation).

Sorties :
  - results/reponse24.txt              : résumé annuel + commentaires
  - results/reponse24_violations.csv   : liste des violations
    colonnes : Num_Acc, nb_lieux, annee
"""

import csv
import sys
from collections import Counter

from common import ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN


def compter_lieux_par_accident(annee: int) -> Counter:
    """Renvoie un Counter {Num_Acc: nb de lignes dans lieux_{annee}.csv}."""
    chemin = ENRICHED / f"lieux_{annee}.csv"
    compteur: Counter = Counter()
    with chemin.open("r", encoding="utf-8", newline="") as f:
        lecteur = csv.reader(f)
        entete = next(lecteur)
        idx_acc = entete.index("Num_Acc")
        for ligne in lecteur:
            compteur[ligne[idx_acc]] += 1
    return compteur


def verifier_annee(
    annee: int, nb_lieux_par_acc: Counter
) -> tuple[int, list[tuple[str, int]]]:
    """Parcourt caracteristiques_{annee}.csv. Renvoie (nb_total, violations).

    `violations` est la liste des couples (Num_Acc, nb_lieux) pour lesquels
    nb_lieux != 1 — c.-à-d. un accident sans lieu (0) ou décrit sur plusieurs
    lieux (>= 2).
    """
    chemin = ENRICHED / f"caracteristiques_{annee}.csv"
    violations: list[tuple[str, int]] = []
    nb_total = 0
    with chemin.open("r", encoding="utf-8", newline="") as f:
        lecteur = csv.reader(f)
        entete = next(lecteur)
        idx_acc = entete.index("Num_Acc")
        for ligne in lecteur:
            nb_total += 1
            num = ligne[idx_acc]
            nb_lieux = nb_lieux_par_acc[num]
            if nb_lieux != 1:
                violations.append((num, nb_lieux))
    return nb_total, violations


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)

    # On accumule pour chaque année : (annee, nb_accidents, nb_violations,
    # nb_sans_lieu, nb_multi_lieux).
    recap_par_annee: list[dict] = []
    toutes_violations: list[tuple[str, int, int]] = []  # (Num_Acc, nb_lieux, annee)

    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        print(f"[..]   {annee}")
        nb_lieux_par_acc = compter_lieux_par_accident(annee)
        nb_total, violations = verifier_annee(annee, nb_lieux_par_acc)

        # Sous-décompte : accidents sans aucun lieu (0) vs sur plusieurs lieux (>=2).
        nb_sans_lieu = sum(1 for _, n in violations if n == 0)
        nb_multi_lieux = sum(1 for _, n in violations if n >= 2)

        recap_par_annee.append({
            "annee": annee,
            "nb_accidents": nb_total,
            "nb_violations": len(violations),
            "nb_sans_lieu": nb_sans_lieu,
            "nb_multi_lieux": nb_multi_lieux,
        })
        for num, nb_lieux in violations:
            toutes_violations.append((num, nb_lieux, annee))

        print(
            f"  [OK] {annee} : {nb_total} accidents, "
            f"{len(violations)} violation(s) "
            f"({nb_sans_lieu} sans lieu, {nb_multi_lieux} multi-lieux)"
        )

    # --- Écriture du fichier de violations ---------------------------------
    chemin_violations = RESULTS / "reponse24_violations.csv"
    with chemin_violations.open("w", encoding="utf-8", newline="") as f:
        ecrivain = csv.writer(f)
        ecrivain.writerow(["Num_Acc", "nb_lieux", "annee"])
        for num, nb_lieux, annee in toutes_violations:
            ecrivain.writerow([num, nb_lieux, annee])

    # --- Écriture du résumé ------------------------------------------------
    nb_total_accidents = sum(r["nb_accidents"] for r in recap_par_annee)
    nb_total_violations = sum(r["nb_violations"] for r in recap_par_annee)
    nb_total_sans_lieu = sum(r["nb_sans_lieu"] for r in recap_par_annee)
    nb_total_multi_lieux = sum(r["nb_multi_lieux"] for r in recap_par_annee)
    taux = (nb_total_violations / nb_total_accidents * 100) if nb_total_accidents else 0.0

    chemin_rapport = RESULTS / "reponse24.txt"
    with chemin_rapport.open("w", encoding="utf-8") as f:
        f.write("Question 2.4 (facultative) — Cardinalité : chaque accident sur "
                "un seul lieu\n")
        f.write("=" * 68 + "\n\n")
        f.write(f"Période : {ANNEE_DEBUT}-{ANNEE_FIN} (Groupe 1)\n")
        f.write(f"Source  : {ENRICHED}\n\n")

        f.write("Méthode : pour chaque année, on compte le nombre de lignes de\n")
        f.write("lieux_{annee}.csv pour chaque Num_Acc (un Counter), puis on\n")
        f.write("parcourt caracteristiques_{annee}.csv en vérifiant que chaque\n")
        f.write("accident possède exactement un lieu. Un accident dont le nombre\n")
        f.write("de lieux vaut 0 (aucun lieu) ou >= 2 (plusieurs lieux) est une\n")
        f.write("violation de la cardinalité « un et un seul lieu ».\n\n")

        f.write("1. Récapitulatif par année\n")
        f.write("-" * 68 + "\n")
        f.write(f"{'année':<8} {'accidents':>12} {'violations':>12} "
                f"{'dont sans lieu':>16} {'dont multi-lieux':>18}\n")
        for r in recap_par_annee:
            f.write(
                f"{r['annee']:<8} {r['nb_accidents']:>12} "
                f"{r['nb_violations']:>12} "
                f"{r['nb_sans_lieu']:>16} {r['nb_multi_lieux']:>18}\n"
            )
        f.write("-" * 68 + "\n")
        f.write(
            f"{'TOTAL':<8} {nb_total_accidents:>12} "
            f"{nb_total_violations:>12} "
            f"{nb_total_sans_lieu:>16} {nb_total_multi_lieux:>18}\n\n"
        )
        f.write(f"Taux global de violations : {taux:.4f} %\n\n")

        f.write("2. Fichier de violations\n")
        f.write("-" * 68 + "\n")
        if nb_total_violations == 0:
            f.write("Aucune violation détectée. Le fichier "
                    "reponse24_violations.csv est vide (en-tête seul).\n\n")
        else:
            f.write(f"{nb_total_violations} ligne(s) écrite(s) dans "
                    f"reponse24_violations.csv\n")
            f.write("Colonnes : Num_Acc, nb_lieux, annee\n\n")

            # Échantillon des 20 premières violations.
            f.write("Échantillon (20 premières violations) :\n")
            for num, nb_lieux, annee in toutes_violations[:20]:
                f.write(f"  {annee}  Num_Acc={num}  nb_lieux={nb_lieux}\n")
            f.write("\n")

        f.write("3. Analyse / commentaires\n")
        f.write("-" * 68 + "\n")
        if nb_total_violations == 0:
            f.write(
                "Chaque accident des caractéristiques se déroule sur un et un\n"
                "seul lieu, sur l'ensemble de la période 2005-2015. La relation\n"
                "caracteristiques → lieux est donc une vraie relation 1-à-1.\n\n"
                "C'est le résultat attendu et il complète Q2.3 : Q2.3 montrait\n"
                "que tout lieu référence un accident existant (aucun lieu\n"
                "orphelin), et que chaque année nb_lieux == nb_accidents ; la\n"
                "présente question confirme le sens manquant — aucun accident\n"
                "n'est sans lieu (0) ni dupliqué sur plusieurs lieux (>= 2).\n"
                "Les deux contrôles réunis établissent la bijection\n"
                "accident ⟷ lieu.\n\n"
                "Conséquence pour la suite : une jointure caracteristiques ⋈\n"
                "lieux sur Num_Acc ne crée ni perte ni duplication de lignes ;\n"
                "les analyses spatiales (Q6) et de voirie (Q3) peuvent\n"
                "fusionner les deux fichiers en toute sûreté.\n"
            )
        else:
            f.write(
                f"{nb_total_violations} accident(s) ne respectent pas la\n"
                f"cardinalité « un seul lieu », sur {nb_total_accidents} "
                f"accidents cumulés ({taux:.4f} %).\n\n"
                f"  - {nb_total_sans_lieu} accident(s) sans aucun lieu "
                f"(nb_lieux = 0) :\n"
                "    une ligne de caractéristiques existe mais aucune ligne de\n"
                "    voirie ne lui correspond — soit une ligne lieux manquante,\n"
                "    soit un Num_Acc mal saisi côté lieux.\n"
                f"  - {nb_total_multi_lieux} accident(s) sur plusieurs lieux "
                f"(nb_lieux >= 2) :\n"
                "    le même Num_Acc apparaît en double dans lieux — doublon de\n"
                "    saisie ou collision de clé.\n\n"
                "La liste exhaustive (Num_Acc, nb_lieux, annee) est disponible\n"
                "dans reponse24_violations.csv pour analyse au cas par cas.\n"
            )

    print(f"\nRapport écrit dans {chemin_rapport}")
    print(f"Violations écrites dans {chemin_violations}")
    print(
        f"Total : {nb_total_accidents} accidents, "
        f"{nb_total_violations} violation(s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
