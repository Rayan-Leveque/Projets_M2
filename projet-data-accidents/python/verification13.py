"""Vérification Q1.3 — enrichissement code → libellé (pandas).

question13.py a remplacé, dans data/enriched/, les codes énumérés par
"code - libellé". On vérifie ici, indépendamment :
  1. conservation : enriched et utf8 ont le même nombre de lignes (aucune
     ligne perdue ou ajoutée) ;
  2. enrichissement : dans chaque colonne énumérée, toute valeur est soit
     enrichie (contient " - "), soit un marqueur d'absence laissé brut
     ('', '.', '-1', '0'/'00'/'000') — aucune valeur "hors mapping" ne doit
     subsister (cohérence avec le « 0 hors mapping » de reponse13.txt) ;
  3. attention ciblée catv : on liste les libellés obtenus et on contrôle
     que les codes enrichis sont bien zero-paddés sur 2 chiffres.

Trace : results/verification13.txt
"""

import sys

import pandas as pd

from common import UTF8, ENRICHED, ANNEE_DEBUT, ANNEE_FIN, TYPES_FICHIERS, Trace

# Colonnes énumérées par type (cf. MAPPINGS de question13.py).
ENUM = {
    "caracteristiques": ["lum", "agg", "int", "atm", "col"],
    "lieux": ["catr", "circ", "vosp", "prof", "plan", "surf", "infra", "situ"],
    "vehicules": ["senc", "catv", "obs", "obsm", "choc", "manv"],
    "usagers": ["catu", "grav", "sexe", "trajet", "locp", "actp", "etatp"],
}
MARQUEURS_ABSENTS = {"", ".", "-1", "0", "00", "000"}


def est_acceptable(valeur: str) -> bool:
    """Une valeur de colonne énumérée est acceptable si elle est enrichie
    (contient ' - ') ou si c'est un marqueur d'absence laissé brut."""
    v = valeur.strip()
    return (" - " in v) or (v in MARQUEURS_ABSENTS)


def main() -> int:
    trace = Trace("verification13.txt")
    trace("Vérification Q1.3 — enrichissement code → libellé (pandas)")
    trace("=" * 72)

    total_anomalies = 0
    lignes_ok = True
    libelles_catv: set[str] = set()
    catv_codes_non_paddes = 0

    for type_fichier in TYPES_FICHIERS:
        trace(f"--- {type_fichier} ---")
        rows_utf8 = 0
        rows_enr = 0
        anomalies_type: dict[str, int] = {c: 0 for c in ENUM[type_fichier]}

        for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
            df_enr = pd.read_csv(
                ENRICHED / f"{type_fichier}_{annee}.csv",
                dtype=str, keep_default_na=False,
            )
            n_utf8 = len(pd.read_csv(
                UTF8 / f"{type_fichier}_{annee}.csv",
                usecols=["Num_Acc"], dtype=str, keep_default_na=False,
            ))
            rows_enr += len(df_enr)
            rows_utf8 += n_utf8
            if len(df_enr) != n_utf8:
                lignes_ok = False
                trace(f"  ✗ {annee} : {len(df_enr)} lignes enriched != {n_utf8} utf8")

            for col in ENUM[type_fichier]:
                serie = df_enr[col]
                masque_mauvais = ~serie.map(est_acceptable)
                anomalies_type[col] += int(masque_mauvais.sum())

            if type_fichier == "vehicules":
                enrichis = df_enr["catv"][df_enr["catv"].str.contains(" - ", regex=False)]
                libelles_catv.update(enrichis.unique())
                codes = enrichis.str.split(" - ", n=1).str[0]
                catv_codes_non_paddes += int((codes.str.len() != 2).sum())

        trace(f"  lignes : enriched={rows_enr}  utf8={rows_utf8}  "
              f"{'(=)' if rows_enr == rows_utf8 else '(DIFFÉRENT !)'}")
        for col, n in anomalies_type.items():
            total_anomalies += n
            etat = "✓" if n == 0 else f"✗ {n}"
            trace(f"    {col:<8} valeurs hors mapping : {etat}")
        trace("")

    # --- Focus catv --------------------------------------------------------
    trace("Focus catv (vehicules)")
    trace("-" * 72)
    trace(f"Nombre de libellés catv distincts obtenus : {len(libelles_catv)}")
    trace(f"Codes catv enrichis non zero-paddés sur 2 chiffres : {catv_codes_non_paddes}")
    for lib in sorted(libelles_catv)[:12]:
        trace(f"  · {lib}")
    if len(libelles_catv) > 12:
        trace(f"  … (+{len(libelles_catv) - 12} autres)")
    trace("")

    ok = (total_anomalies == 0) and lignes_ok and (catv_codes_non_paddes == 0)
    if ok:
        trace("RÉSULTAT : ✓ VÉRIFIÉ — aucune ligne perdue, aucune valeur énumérée")
        trace("           hors mapping, codes catv bien paddés sur 2 chiffres.")
    else:
        trace(f"RÉSULTAT : ✗ ANOMALIES — {total_anomalies} valeurs hors mapping, "
              f"lignes cohérentes={lignes_ok}, catv non paddés={catv_codes_non_paddes}.")

    trace.ecrire()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
