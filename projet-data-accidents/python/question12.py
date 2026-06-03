"""Question 1.2 — Vérification de la structure et tableaux récapitulatifs.

Pour chaque type de fichier (caracteristiques, lieux, vehicules, usagers)
et chaque année du groupe (ANNEE_DEBUT..ANNEE_FIN) :

  1. on lit la ligne d'en-tête et on la compare au schéma attendu
     (colonnes manquantes, colonnes inattendues, ordre) ;
  2. on compte le nombre de lignes de données (hors en-tête) ;
  3. on note le nombre de colonnes effectivement présentes.

Le rapport (4 tableaux + synthèse des écarts de schéma) est écrit dans
results/reponse12.txt.
"""

import csv
import sys
from pathlib import Path

from common import UTF8, RESULTS, TYPES_FICHIERS, ANNEE_DEBUT, ANNEE_FIN


# Schémas attendus (colonnes réelles 2005-2015), dans l'ordre de la doc BAAC.
SCHEMAS_ATTENDUS: dict[str, list[str]] = {
    "caracteristiques": [
        "Num_Acc", "an", "mois", "jour", "hrmn", "lum", "agg", "int",
        "atm", "col", "com", "adr", "gps", "lat", "long", "dep",
    ],
    "lieux": [
        "Num_Acc", "catr", "voie", "v1", "v2", "circ", "nbv", "pr", "pr1",
        "vosp", "prof", "plan", "lartpc", "larrout", "surf", "infra",
        "situ", "env1",
    ],
    "vehicules": [
        "Num_Acc", "senc", "catv", "occutc", "obs", "obsm", "choc", "manv",
        "num_veh",
    ],
    "usagers": [
        "Num_Acc", "place", "catu", "grav", "sexe", "trajet", "secu",
        "locp", "actp", "etatp", "an_nais", "num_veh",
    ],
}


def analyser_fichier(chemin: Path, schema_attendu: list[str]) -> dict:
    """Lit l'en-tête + compte les lignes ; renvoie un récap détaillé."""
    with chemin.open("r", encoding="utf-8", newline="") as f:
        lecteur = csv.reader(f)
        try:
            entete = next(lecteur)
        except StopIteration:
            return {
                "existe": True,
                "vide": True,
                "entete": [],
                "nb_lignes": 0,
                "nb_colonnes": 0,
                "manquantes": list(schema_attendu),
                "inattendues": [],
                "ordre_ok": False,
            }
        nb_lignes = sum(1 for _ in lecteur)

    ensemble_attendu = set(schema_attendu)
    ensemble_present = set(entete)
    manquantes = [c for c in schema_attendu if c not in ensemble_present]
    inattendues = [c for c in entete if c not in ensemble_attendu]
    ordre_ok = entete == schema_attendu

    return {
        "existe": True,
        "vide": False,
        "entete": entete,
        "nb_lignes": nb_lignes,
        "nb_colonnes": len(entete),
        "manquantes": manquantes,
        "inattendues": inattendues,
        "ordre_ok": ordre_ok,
    }


def formater_tableau(type_fichier: str, lignes: list[dict], nb_col_attendu: int) -> str:
    """Construit un tableau ASCII pour un type donné."""
    titre = f"Tableau — {type_fichier} ({nb_col_attendu} colonnes attendues)"
    sortie = [titre, "=" * len(titre), ""]
    sortie.append(f"{'Année':<8} {'Nb lignes':>12} {'Nb colonnes':>13} {'Cumul lignes':>15}")
    sortie.append("-" * 52)
    cumul = 0
    for ligne in lignes:
        cumul += ligne["nb_lignes"]
        sortie.append(
            f"{ligne['annee']:<8} {ligne['nb_lignes']:>12} "
            f"{ligne['nb_colonnes']:>13} {cumul:>15}"
        )
    sortie.append("-" * 52)
    sortie.append(f"{'TOTAL':<8} {cumul:>12}")
    sortie.append("")
    return "\n".join(sortie)


def main() -> int:
    if not UTF8.is_dir():
        print(f"Dossier source introuvable : {UTF8}", file=sys.stderr)
        return 1
    RESULTS.mkdir(parents=True, exist_ok=True)

    # Collecte des résultats par type.
    resultats: dict[str, list[dict]] = {t: [] for t in TYPES_FICHIERS}
    anomalies: list[str] = []  # écarts de schéma rencontrés

    for type_fichier in TYPES_FICHIERS:
        schema_attendu = SCHEMAS_ATTENDUS[type_fichier]
        nb_col_attendu = len(schema_attendu)
        print(f"\n=== {type_fichier} ===")
        for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
            chemin = UTF8 / f"{type_fichier}_{annee}.csv"
            if not chemin.exists():
                print(f"  [MANQUANT] {chemin.name}")
                anomalies.append(f"{chemin.name} : fichier absent de data/utf8/")
                resultats[type_fichier].append({
                    "annee": annee,
                    "nb_lignes": 0,
                    "nb_colonnes": 0,
                })
                continue

            recap = analyser_fichier(chemin, schema_attendu)
            resultats[type_fichier].append({
                "annee": annee,
                "nb_lignes": recap["nb_lignes"],
                "nb_colonnes": recap["nb_colonnes"],
            })

            statut = "OK" if recap["ordre_ok"] else "ÉCART"
            print(
                f"  [{statut}] {chemin.name} : "
                f"{recap['nb_lignes']} lignes, {recap['nb_colonnes']} colonnes"
            )

            # Détail des écarts.
            if recap["nb_colonnes"] != nb_col_attendu:
                anomalies.append(
                    f"{chemin.name} : {recap['nb_colonnes']} colonnes "
                    f"vs {nb_col_attendu} attendues"
                )
            if recap["manquantes"]:
                anomalies.append(
                    f"{chemin.name} : colonnes manquantes "
                    f"{recap['manquantes']}"
                )
            if recap["inattendues"]:
                anomalies.append(
                    f"{chemin.name} : colonnes inattendues "
                    f"{recap['inattendues']}"
                )
            if (not recap["manquantes"] and not recap["inattendues"]
                    and not recap["ordre_ok"]):
                anomalies.append(
                    f"{chemin.name} : ordre des colonnes différent du schéma\n"
                    f"    présent  : {recap['entete']}\n"
                    f"    attendu  : {schema_attendu}"
                )

    # Écriture du rapport.
    chemin_rapport = RESULTS / "reponse12.txt"
    with chemin_rapport.open("w", encoding="utf-8") as f:
        f.write("Question 1.2 — Vérification de la structure des fichiers BAAC\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Période traitée : {ANNEE_DEBUT}-{ANNEE_FIN} (Groupe 1)\n")
        f.write(f"Source : {UTF8}\n\n")

        # Schémas attendus.
        f.write("Schémas attendus (colonnes réelles 2005-2015) :\n")
        for type_fichier in TYPES_FICHIERS:
            cols = SCHEMAS_ATTENDUS[type_fichier]
            f.write(f"  - {type_fichier} ({len(cols)} colonnes) : "
                    f"{', '.join(cols)}\n")
        f.write("\n")

        # Les 4 tableaux récapitulatifs.
        for type_fichier in TYPES_FICHIERS:
            nb_col_attendu = len(SCHEMAS_ATTENDUS[type_fichier])
            f.write(formater_tableau(
                type_fichier, resultats[type_fichier], nb_col_attendu
            ))
            f.write("\n")

        # Cumul global tous types confondus.
        cumul_global = sum(
            r["nb_lignes"]
            for type_fichier in TYPES_FICHIERS
            for r in resultats[type_fichier]
        )
        f.write(f"Cumul global (tous types, toutes années) : "
                f"{cumul_global} lignes de données\n\n")

        # Synthèse des anomalies de schéma.
        f.write("Synthèse des écarts de schéma\n")
        f.write("-" * 30 + "\n")
        if not anomalies:
            f.write("Aucun écart : tous les fichiers ont la structure attendue, "
                    "dans le bon ordre.\n")
        else:
            for ligne in anomalies:
                f.write(f"  - {ligne}\n")

    print(f"\nRapport écrit dans {chemin_rapport}")
    print(f"Anomalies de schéma : {len(anomalies)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
