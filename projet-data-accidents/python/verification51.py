"""Vérification Q5.1 — incohérence lum × hrmn (pandas).

Réimplémentation indépendante (pandas, vectorisée) du critère de question51.py
(csv.reader) : pour chaque accident testable on déduit la saison du mois, on
extrait l'heure de hrmn (HHMM non paddé → //100) et on applique les bornes
saisonnières. On compare ensuite l'ensemble des accidents signalés à
results/reponse51_complet.csv (clé : annee, Num_Acc).

Trace : results/verification51.txt
"""

import sys

import pandas as pd

from common import ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN, Trace

BORNES = {  # saison -> (jour_debut, jour_fin, coeur_debut, coeur_fin)
    "hiver": (8, 17, 10, 16),
    "printemps": (7, 20, 9, 17),
    "été": (6, 21, 8, 18),
    "automne": (7, 20, 9, 17),
}


def saison(mois: int) -> str:
    if mois in (12, 1, 2):
        return "hiver"
    if mois in (3, 4, 5):
        return "printemps"
    if mois in (6, 7, 8):
        return "été"
    return "automne"


def incoherences_pandas() -> set[tuple[str, str]]:
    flags: set[tuple[str, str]] = set()
    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        df = pd.read_csv(
            ENRICHED / f"caracteristiques_{annee}.csv",
            usecols=["Num_Acc", "mois", "hrmn", "lum"],
            dtype=str, keep_default_na=False,
        )
        valide = df["hrmn"].str.strip().str.isdigit() & df["mois"].str.strip().str.isdigit()
        w = df[valide].copy()
        w["heure"] = w["hrmn"].str.strip().astype(int) // 100
        w["mois_i"] = w["mois"].str.strip().astype(int)
        w["sais"] = w["mois_i"].map(saison)
        w["jd"] = w["sais"].map(lambda s: BORNES[s][0])
        w["jf"] = w["sais"].map(lambda s: BORNES[s][1])
        w["cd"] = w["sais"].map(lambda s: BORNES[s][2])
        w["cf"] = w["sais"].map(lambda s: BORNES[s][3])

        plein_jour = w["lum"].str.contains("1 - Plein jour", regex=False)
        nuit = w["lum"].str.contains("3 - Nuit|4 - Nuit|5 - Nuit", regex=True)
        cas1 = plein_jour & ~((w["heure"] >= w["jd"]) & (w["heure"] <= w["jf"]))
        cas2 = nuit & (w["heure"] >= w["cd"]) & (w["heure"] <= w["cf"])

        for num_acc in w[cas1 | cas2]["Num_Acc"]:
            flags.add((str(annee), num_acc))
    return flags


def main() -> int:
    trace = Trace("verification51.txt")
    trace("Vérification Q5.1 — incohérence lum × hrmn (pandas, bornes saisonnières)")
    trace("=" * 72)

    flags = incoherences_pandas()
    ref = pd.read_csv(
        RESULTS / "reponse51_complet.csv", dtype=str, keep_default_na=False
    )
    set_ref = {(a, n) for a, n in zip(ref["annee"], ref["Num_Acc"])}

    trace(f"Incohérences trouvées par pandas       : {len(flags)}")
    trace(f"Incohérences dans reponse51_complet.csv : {len(set_ref)}")
    manquantes = set_ref - flags
    en_trop = flags - set_ref
    trace(f"Présentes dans la réponse, pas retrouvées par pandas : {len(manquantes)}")
    trace(f"Trouvées par pandas, absentes de la réponse          : {len(en_trop)}")
    trace("")

    ok = flags == set_ref
    if ok:
        trace(f"RÉSULTAT : ✓ VÉRIFIÉ — mêmes {len(flags)} accidents incohérents par")
        trace("           les deux méthodes (csv.reader et pandas).")
    else:
        trace("RÉSULTAT : ✗ DIVERGENCE — échantillons :")
        for c in list(manquantes)[:10]:
            trace(f"  manquant (réponse) : {c}")
        for c in list(en_trop)[:10]:
            trace(f"  en trop (pandas)   : {c}")

    trace.ecrire()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
