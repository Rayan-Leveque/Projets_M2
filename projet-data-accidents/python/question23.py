"""Question 2.3 (facultative) — Intégrité référentielle : lieux → caracteristiques.

Vérifie par programme que chaque ligne de `lieux_{annee}.csv` fait référence à
un accident effectivement présent dans `caracteristiques_{annee}.csv`, via la
clé `Num_Acc`.

Méthode année par année (les Num_Acc sont préfixés par l'année dans BAAC, mais
on reste prudent et on traite chaque année isolément) :
  1. On charge l'ensemble des Num_Acc du fichier caracteristiques de l'année
     dans un `set` Python.
  2. On parcourt lieux_{annee}.csv ligne à ligne. Pour chaque lieu on teste
     l'appartenance de son Num_Acc au set. S'il n'y est pas → violation
     (lieu rattaché à un accident inexistant).

Sorties :
  - results/reponse23.txt              : résumé annuel + commentaires
  - results/reponse23_violations.csv   : liste des violations
    colonnes : annee, Num_Acc
"""

import csv
import sys

from common import ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN


def charger_num_acc_caracteristiques(annee: int) -> set[str]:
    """Renvoie l'ensemble des Num_Acc présents dans caracteristiques_{annee}.csv."""
    chemin = ENRICHED / f"caracteristiques_{annee}.csv"
    num_acc: set[str] = set()
    with chemin.open("r", encoding="utf-8", newline="") as f:
        lecteur = csv.reader(f)
        entete = next(lecteur)
        idx_acc = entete.index("Num_Acc")
        for ligne in lecteur:
            num_acc.add(ligne[idx_acc])
    return num_acc


def verifier_annee(
    annee: int, num_acc_caracteristiques: set[str]
) -> tuple[int, list[str]]:
    """Parcourt lieux_{annee}.csv. Renvoie (nb_total, violations).

    `violations` est la liste des Num_Acc trouvés côté lieux et absents de
    l'ensemble des Num_Acc côté caracteristiques — c.-à-d. des lieux rattachés
    à un accident qui n'existe pas dans les caractéristiques.
    """
    chemin = ENRICHED / f"lieux_{annee}.csv"
    violations: list[str] = []
    nb_total = 0
    with chemin.open("r", encoding="utf-8", newline="") as f:
        lecteur = csv.reader(f)
        entete = next(lecteur)
        idx_acc = entete.index("Num_Acc")
        for ligne in lecteur:
            nb_total += 1
            num = ligne[idx_acc]
            if num not in num_acc_caracteristiques:
                violations.append(num)
    return nb_total, violations


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)

    # On accumule pour chaque année : (annee, nb_lieux, nb_accidents,
    # nb_violations, nb_num_acc_vide).
    recap_par_annee: list[dict] = []
    toutes_violations: list[tuple[int, str]] = []  # (annee, Num_Acc)

    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        print(f"[..]   {annee}")
        num_acc_carac = charger_num_acc_caracteristiques(annee)
        nb_total, violations = verifier_annee(annee, num_acc_carac)

        # Sous-décompte : combien de violations sont dûes à un Num_Acc vide
        # côté lieux (cas distinct d'une "vraie" référence cassée).
        nb_num_acc_vide = sum(1 for n in violations if n.strip() == "")

        recap_par_annee.append({
            "annee": annee,
            "nb_lieux": nb_total,
            "nb_accidents": len(num_acc_carac),
            "nb_violations": len(violations),
            "nb_num_acc_vide": nb_num_acc_vide,
        })
        for num in violations:
            toutes_violations.append((annee, num))

        print(
            f"  [OK] {annee} : {nb_total} lieux, "
            f"{len(num_acc_carac)} accidents, "
            f"{len(violations)} violation(s)"
        )

    # --- Écriture du fichier de violations ---------------------------------
    chemin_violations = RESULTS / "reponse23_violations.csv"
    with chemin_violations.open("w", encoding="utf-8", newline="") as f:
        ecrivain = csv.writer(f)
        ecrivain.writerow(["annee", "Num_Acc"])
        for annee, num in toutes_violations:
            ecrivain.writerow([annee, num])

    # --- Écriture du résumé ------------------------------------------------
    nb_total_lieux = sum(r["nb_lieux"] for r in recap_par_annee)
    nb_total_violations = sum(r["nb_violations"] for r in recap_par_annee)
    nb_total_num_acc_vide = sum(r["nb_num_acc_vide"] for r in recap_par_annee)
    taux = (nb_total_violations / nb_total_lieux * 100) if nb_total_lieux else 0.0

    chemin_rapport = RESULTS / "reponse23.txt"
    with chemin_rapport.open("w", encoding="utf-8") as f:
        f.write("Question 2.3 (facultative) — Intégrité référentielle : "
                "lieux → caracteristiques\n")
        f.write("=" * 68 + "\n\n")
        f.write(f"Période : {ANNEE_DEBUT}-{ANNEE_FIN} (Groupe 1)\n")
        f.write(f"Source  : {ENRICHED}\n\n")

        f.write("Méthode : pour chaque année, on construit l'ensemble des Num_Acc\n")
        f.write("présents dans caracteristiques_{annee}.csv puis on parcourt\n")
        f.write("lieux_{annee}.csv en vérifiant que le Num_Acc de chaque lieu\n")
        f.write("existe bien dans cet ensemble. Tout lieu dont le Num_Acc n'est\n")
        f.write("pas trouvé est un lieu rattaché à un accident inexistant.\n\n")

        f.write("1. Récapitulatif par année\n")
        f.write("-" * 68 + "\n")
        f.write(f"{'année':<8} {'lieux':>10} {'accidents':>12} "
                f"{'violations':>12} {'dont Num_Acc vide':>20}\n")
        for r in recap_par_annee:
            f.write(
                f"{r['annee']:<8} {r['nb_lieux']:>10} "
                f"{r['nb_accidents']:>12} "
                f"{r['nb_violations']:>12} {r['nb_num_acc_vide']:>20}\n"
            )
        f.write("-" * 68 + "\n")
        f.write(
            f"{'TOTAL':<8} {nb_total_lieux:>10} "
            f"{sum(r['nb_accidents'] for r in recap_par_annee):>12} "
            f"{nb_total_violations:>12} {nb_total_num_acc_vide:>20}\n\n"
        )
        f.write(f"Taux global de violations : {taux:.4f} %\n\n")

        f.write("2. Fichier de violations\n")
        f.write("-" * 68 + "\n")
        if nb_total_violations == 0:
            f.write("Aucune violation détectée. Le fichier "
                    "reponse23_violations.csv est vide (en-tête seul).\n\n")
        else:
            f.write(f"{nb_total_violations} ligne(s) écrite(s) dans "
                    f"reponse23_violations.csv\n")
            f.write("Colonnes : annee, Num_Acc\n\n")

            # Échantillon des 20 premières violations.
            f.write("Échantillon (20 premières violations) :\n")
            for annee, num in toutes_violations[:20]:
                num_aff = repr(num) if num.strip() == "" else num
                f.write(f"  {annee}  Num_Acc={num_aff}\n")
            f.write("\n")

        f.write("3. Analyse / commentaires\n")
        f.write("-" * 68 + "\n")
        if nb_total_violations == 0:
            f.write(
                "Tout lieu enregistré référence un accident présent dans les\n"
                "caractéristiques, sur l'ensemble de la période 2005-2015.\n"
                "L'intégrité référentielle lieux → caracteristiques est\n"
                "parfaite. C'est le résultat attendu : dans le modèle BAAC, le\n"
                "fichier lieux décrit la voirie de l'accident à raison d'une\n"
                "ligne par Num_Acc (relation 1-à-1 avec caracteristiques),\n"
                "donc aucun lieu ne devrait exister sans son accident.\n"
            )
        else:
            f.write(
                f"{nb_total_violations} lieu(x) référencent un accident absent\n"
                f"des caractéristiques, sur {nb_total_lieux} lieux cumulés\n"
                f"({taux:.4f} %).\n\n"
                "Dans le modèle BAAC, le fichier lieux décrit la voirie de\n"
                "l'accident à raison d'une ligne par Num_Acc ; chaque lieu\n"
                "devrait donc avoir son accident correspondant dans\n"
                "caracteristiques. Une violation signale soit un Num_Acc mal\n"
                "saisi côté lieux, soit une ligne de caractéristiques\n"
                "manquante. La liste exhaustive est disponible dans\n"
                "reponse23_violations.csv.\n"
            )

    print(f"\nRapport écrit dans {chemin_rapport}")
    print(f"Violations écrites dans {chemin_violations}")
    print(
        f"Total : {nb_total_lieux} lieux, {nb_total_violations} violation(s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
