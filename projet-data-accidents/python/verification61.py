"""Vérification Q6.1 — accidents par tranche horaire d'1h (pandas).

On recompte avec pandas le nombre d'accidents métropolitains par heure
(0-23) et on le recoupe avec la fonction d'agrégation de question61.py
(compter_par_heure, basée sur csv.reader). Accord des deux méthodes = trace
chiffrée de l'histogramme reponse61.png.

Trace : results/verification61.txt
"""

import sys

import pandas as pd

import question61
from common import ENRICHED, ANNEE_DEBUT, ANNEE_FIN, normaliser_dep, Trace


def par_heure_pandas() -> list[int]:
    compte = [0] * 24
    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        df = pd.read_csv(
            ENRICHED / f"caracteristiques_{annee}.csv",
            usecols=["hrmn", "dep"], dtype=str, keep_default_na=False,
        )
        metropole = df["dep"].map(normaliser_dep).notna()
        valide = metropole & df["hrmn"].str.strip().str.isdigit()
        heures = df[valide]["hrmn"].str.strip().astype(int) // 100
        for h, n in heures.value_counts().items():
            if 0 <= int(h) <= 23:
                compte[int(h)] += int(n)
    return compte


def main() -> int:
    trace = Trace("verification61.txt")
    trace("Vérification Q6.1 — accidents par tranche horaire (pandas vs csv)")
    trace("=" * 72)

    pandas_compte = par_heure_pandas()
    ref = question61.compter_par_heure()

    trace(f"{'heure':<8}{'pandas':>10}{'question61':>12}{'==?':>6}")
    trace("-" * 72)
    ok = True
    for h in range(24):
        egal = pandas_compte[h] == ref[h]
        ok = ok and egal
        trace(f"{h:<8}{pandas_compte[h]:>10}{ref[h]:>12}{('✓' if egal else '✗'):>6}")
    trace("-" * 72)
    trace(f"{'TOTAL':<8}{sum(pandas_compte):>10}{sum(ref):>12}")
    trace("")

    if ok:
        trace("RÉSULTAT : ✓ VÉRIFIÉ — pandas et question61.py donnent le même nombre")
        trace(f"           d'accidents pour chacune des 24 heures (total {sum(ref)}).")
    else:
        trace("RÉSULTAT : ✗ DIVERGENCE sur au moins une tranche horaire.")

    trace.ecrire()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
