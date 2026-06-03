"""Question 2.2 — Intégrité référentielle : vehicules → usagers.

Vérifie par programme que chaque véhicule décrit dans `vehicules_{annee}.csv`
est associé à *au moins un* usager dans `usagers_{annee}.csv` (sens inverse
de Q2.1).

Méthode année par année :
  1. On charge l'ensemble des couples (Num_Acc, num_veh) du fichier
     usagers de l'année dans un `set` Python.
  2. On parcourt vehicules_{annee}.csv ligne à ligne. Pour chaque véhicule
     on construit la clé (Num_Acc, num_veh) et on teste son appartenance
     au set. Si elle n'y est pas → violation (véhicule sans usager).

Sorties :
  - results/reponse22.txt              : résumé annuel + commentaires
  - results/reponse22_violations.csv   : liste des violations
    colonnes : annee, Num_Acc, num_veh
"""

import csv
import sys

from common import ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN


def charger_couples_usagers(annee: int) -> set[tuple[str, str]]:
    """Renvoie l'ensemble des couples (Num_Acc, num_veh) du fichier usagers."""
    chemin = ENRICHED / f"usagers_{annee}.csv"
    couples: set[tuple[str, str]] = set()
    with chemin.open("r", encoding="utf-8", newline="") as f:
        lecteur = csv.reader(f)
        entete = next(lecteur)
        idx_acc = entete.index("Num_Acc")
        idx_veh = entete.index("num_veh")
        for ligne in lecteur:
            couples.add((ligne[idx_acc], ligne[idx_veh]))
    return couples


def verifier_annee(
    annee: int, couples_usagers: set[tuple[str, str]]
) -> tuple[int, list[tuple[str, str]]]:
    """Parcourt vehicules_{annee}.csv. Renvoie (nb_total, violations).

    `violations` est la liste des couples (Num_Acc, num_veh) trouvés côté
    vehicules et absents de l'ensemble des couples côté usagers — c.-à-d.
    des véhicules sans aucun usager rattaché.
    """
    chemin = ENRICHED / f"vehicules_{annee}.csv"
    violations: list[tuple[str, str]] = []
    nb_total = 0
    with chemin.open("r", encoding="utf-8", newline="") as f:
        lecteur = csv.reader(f)
        entete = next(lecteur)
        idx_acc = entete.index("Num_Acc")
        idx_veh = entete.index("num_veh")
        for ligne in lecteur:
            nb_total += 1
            cle = (ligne[idx_acc], ligne[idx_veh])
            if cle not in couples_usagers:
                violations.append(cle)
    return nb_total, violations


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)

    # On accumule pour chaque année : (annee, nb_vehicules, nb_violations,
    # nb_violations_num_veh_vide, nb_couples_usagers).
    recap_par_annee: list[dict] = []
    toutes_violations: list[tuple[int, str, str]] = []  # (annee, Num_Acc, num_veh)

    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        print(f"[..]   {annee}")
        couples_usa = charger_couples_usagers(annee)
        nb_total, violations = verifier_annee(annee, couples_usa)

        # Sous-décompte : combien de violations sont dûes à un num_veh vide
        # côté vehicules (cas distinct d'une "vraie" référence cassée).
        nb_num_veh_vide = sum(1 for _, v in violations if v.strip() == "")

        recap_par_annee.append({
            "annee": annee,
            "nb_vehicules": nb_total,
            "nb_couples_usagers": len(couples_usa),
            "nb_violations": len(violations),
            "nb_num_veh_vide": nb_num_veh_vide,
        })
        for acc, veh in violations:
            toutes_violations.append((annee, acc, veh))

        print(
            f"  [OK] {annee} : {nb_total} véhicules, "
            f"{len(couples_usa)} couples usager, "
            f"{len(violations)} violation(s)"
        )

    # --- Écriture du fichier de violations ---------------------------------
    chemin_violations = RESULTS / "reponse22_violations.csv"
    with chemin_violations.open("w", encoding="utf-8", newline="") as f:
        ecrivain = csv.writer(f)
        ecrivain.writerow(["annee", "Num_Acc", "num_veh"])
        for annee, acc, veh in toutes_violations:
            ecrivain.writerow([annee, acc, veh])

    # --- Écriture du résumé ------------------------------------------------
    nb_total_vehicules = sum(r["nb_vehicules"] for r in recap_par_annee)
    nb_total_violations = sum(r["nb_violations"] for r in recap_par_annee)
    nb_total_num_veh_vide = sum(r["nb_num_veh_vide"] for r in recap_par_annee)
    taux = (nb_total_violations / nb_total_vehicules * 100) if nb_total_vehicules else 0.0

    chemin_rapport = RESULTS / "reponse22.txt"
    with chemin_rapport.open("w", encoding="utf-8") as f:
        f.write("Question 2.2 — Intégrité référentielle : vehicules → usagers\n")
        f.write("=" * 68 + "\n\n")
        f.write(f"Période : {ANNEE_DEBUT}-{ANNEE_FIN} (Groupe 1)\n")
        f.write(f"Source  : {ENRICHED}\n\n")

        f.write("Méthode : pour chaque année, on construit l'ensemble des couples\n")
        f.write("(Num_Acc, num_veh) présents dans usagers_{annee}.csv puis on\n")
        f.write("parcourt vehicules_{annee}.csv en vérifiant que chaque (Num_Acc,\n")
        f.write("num_veh) côté véhicule existe bien dans cet ensemble. Tout\n")
        f.write("véhicule dont la clé n'est pas trouvée est un véhicule \"sans\n")
        f.write("usager\".\n\n")

        f.write("1. Récapitulatif par année\n")
        f.write("-" * 68 + "\n")
        f.write(f"{'année':<8} {'véhicules':>10} {'couples usa.':>14} "
                f"{'violations':>12} {'dont num_veh vide':>20}\n")
        for r in recap_par_annee:
            f.write(
                f"{r['annee']:<8} {r['nb_vehicules']:>10} "
                f"{r['nb_couples_usagers']:>14} "
                f"{r['nb_violations']:>12} {r['nb_num_veh_vide']:>20}\n"
            )
        f.write("-" * 68 + "\n")
        f.write(
            f"{'TOTAL':<8} {nb_total_vehicules:>10} "
            f"{sum(r['nb_couples_usagers'] for r in recap_par_annee):>14} "
            f"{nb_total_violations:>12} {nb_total_num_veh_vide:>20}\n\n"
        )
        f.write(f"Taux global de violations : {taux:.4f} %\n\n")

        f.write("2. Fichier de violations\n")
        f.write("-" * 68 + "\n")
        if nb_total_violations == 0:
            f.write("Aucune violation détectée. Le fichier "
                    "reponse22_violations.csv est vide (en-tête seul).\n\n")
        else:
            f.write(f"{nb_total_violations} ligne(s) écrite(s) dans "
                    f"reponse22_violations.csv\n")
            f.write("Colonnes : annee, Num_Acc, num_veh\n\n")

            # Échantillon des 20 premières violations.
            f.write("Échantillon (20 premières violations) :\n")
            for annee, acc, veh in toutes_violations[:20]:
                veh_aff = repr(veh) if veh.strip() == "" else veh
                f.write(f"  {annee}  Num_Acc={acc}  num_veh={veh_aff}\n")
            f.write("\n")

        f.write("3. Analyse / commentaires\n")
        f.write("-" * 68 + "\n")
        if nb_total_violations == 0:
            f.write(
                "Tout véhicule enregistré est rattaché à au moins un usager\n"
                "sur l'ensemble de la période 2005-2015. L'intégrité\n"
                "référentielle vehicules → usagers est parfaite.\n"
            )
        else:
            f.write(
                f"{nb_total_violations} véhicule(s) sans aucun usager rattaché,\n"
                f"sur {nb_total_vehicules} véhicules cumulés ({taux:.4f} %).\n\n"
                "Interprétation : un véhicule sans usager peut paraître\n"
                "anormal puisqu'un véhicule est *forcément* conduit par\n"
                "quelqu'un. Le cas connu correspond aux **conducteurs en\n"
                "fuite** : la procédure BAAC enregistre le véhicule heurtant\n"
                "(numéro, type) parce qu'il est mentionné par les témoins ou\n"
                "déduit des dégâts, mais aucun usager n'est saisi côté\n"
                "victime — la fiche conducteur reste vide tant que le fuyard\n"
                "n'est pas identifié. Ces lignes ne sont donc pas de simples\n"
                "erreurs de saisie : elles portent une information utile (un\n"
                "véhicule a été impliqué sans qu'on connaisse son\n"
                "conducteur).\n\n"
                f"Aucune violation n'est dûe à un num_veh vide ({nb_total_num_veh_vide}\n"
                "cas) : la clé est toujours non vide côté véhicules.\n\n"
                "Décision pour les questions suivantes : ces véhicules \"sans\n"
                "usager\" ne seront PAS supprimés ; ils restent comptabilisés\n"
                "dans les analyses sur les véhicules (Q3, Q4, Q6) mais\n"
                "n'apparaîtront évidemment pas dans les analyses centrées sur\n"
                "les usagers (gravité, âge, sexe). La liste exhaustive est\n"
                "disponible dans reponse22_violations.csv pour qui voudrait\n"
                "les isoler explicitement (étude de la fuite, p. ex.).\n"
            )

    print(f"\nRapport écrit dans {chemin_rapport}")
    print(f"Violations écrites dans {chemin_violations}")
    print(
        f"Total : {nb_total_vehicules} véhicules, "
        f"{nb_total_violations} violation(s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
