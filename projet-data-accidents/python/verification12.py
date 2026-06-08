"""Vérification Q1.2 — structure des fichiers + nb de lignes par année (pandas).

question12.py a vérifié la conformité de structure via csv.reader. On la
recoupe ici avec pandas : pour chaque fichier on contrôle que l'en-tête est
EXACTEMENT le schéma BAAC attendu (mêmes colonnes, même ordre) et on
recompte le nombre de lignes de données par année + le cumul par type.

Trace : results/verification12.txt
"""

import sys

import pandas as pd

from common import UTF8, ANNEE_DEBUT, ANNEE_FIN, TYPES_FICHIERS, Trace

# Schémas attendus (colonnes réelles 2005-2015), dans l'ordre de la doc BAAC.
SCHEMAS = {
    "caracteristiques": ["Num_Acc", "an", "mois", "jour", "hrmn", "lum", "agg",
                         "int", "atm", "col", "com", "adr", "gps", "lat", "long", "dep"],
    "lieux": ["Num_Acc", "catr", "voie", "v1", "v2", "circ", "nbv", "pr", "pr1",
              "vosp", "prof", "plan", "lartpc", "larrout", "surf", "infra", "situ", "env1"],
    "vehicules": ["Num_Acc", "senc", "catv", "occutc", "obs", "obsm", "choc",
                  "manv", "num_veh"],
    "usagers": ["Num_Acc", "place", "catu", "grav", "sexe", "trajet", "secu",
                "locp", "actp", "etatp", "an_nais", "num_veh"],
}


def main() -> int:
    trace = Trace("verification12.txt")
    trace("Vérification Q1.2 — structure conforme + nb de lignes par année (pandas)")
    trace("=" * 72)
    trace("Pour chaque fichier : en-tête comparé au schéma attendu (colonnes +")
    trace("ordre), puis recomptage des lignes de données et du cumul par type.")
    trace("")

    schemas_ok = 0
    schemas_total = 0
    anomalies: list[str] = []

    for type_fichier in TYPES_FICHIERS:
        schema = SCHEMAS[type_fichier]
        trace(f"Tableau — {type_fichier} ({len(schema)} colonnes attendues)")
        trace(f"{'Année':<8}{'Nb lignes':>12}{'Nb colonnes':>14}{'Cumul':>14}{'Schéma':>10}")
        trace("-" * 72)
        cumul = 0
        for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
            chemin = UTF8 / f"{type_fichier}_{annee}.csv"
            df = pd.read_csv(chemin, dtype=str, keep_default_na=False)
            schemas_total += 1
            conforme = list(df.columns) == schema
            if conforme:
                schemas_ok += 1
                etat = "✓"
            else:
                etat = "✗"
                anomalies.append(
                    f"{chemin.name} : en-tête {list(df.columns)} != schéma attendu"
                )
            cumul += len(df)
            trace(f"{annee:<8}{len(df):>12}{df.shape[1]:>14}{cumul:>14}{etat:>10}")
        trace("-" * 72)
        trace(f"{'TOTAL':<8}{cumul:>12}")
        trace("")

    trace(f"Fichiers au schéma conforme : {schemas_ok} / {schemas_total}")
    trace("")
    ok = schemas_ok == schemas_total
    if ok:
        trace("RÉSULTAT : ✓ VÉRIFIÉ — les 44 fichiers ont l'en-tête exact attendu")
        trace("           (colonnes et ordre), conforme à la documentation BAAC.")
    else:
        trace("RÉSULTAT : ✗ ANOMALIES DE STRUCTURE :")
        for a in anomalies[:20]:
            trace(f"  - {a}")

    trace.ecrire()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
