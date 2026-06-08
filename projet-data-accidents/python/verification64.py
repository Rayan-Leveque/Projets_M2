"""Vérification Q6.4 — heatmap atm × surf (pandas).

On reconstruit avec pandas (jointure caracteristiques↔lieux sur Num_Acc,
France métropolitaine) le nombre d'accidents exploités, les accidents
ignorés (atm/surf hors référentiel) et le couple le plus fréquent, puis on
recoupe avec results/reponse64.txt. Les listes de référence VALEURS_ATM /
VALEURS_SURF sont importées de question64.py.

Trace : results/verification64.txt
"""

import re
import sys
from collections import Counter

import pandas as pd

import question64
from common import ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN, normaliser_dep, Trace

ATM = set(question64.VALEURS_ATM)
SURF = set(question64.VALEURS_SURF)


def calcul_pandas():
    couples = Counter()
    atm_ignore = 0
    surf_ignore = 0
    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        carac = pd.read_csv(
            ENRICHED / f"caracteristiques_{annee}.csv",
            usecols=["Num_Acc", "dep", "atm"], dtype=str, keep_default_na=False,
        )
        carac = carac[carac["dep"].map(normaliser_dep).notna()][["Num_Acc", "atm"]]
        lieux = pd.read_csv(
            ENRICHED / f"lieux_{annee}.csv",
            usecols=["Num_Acc", "surf"], dtype=str, keep_default_na=False,
        )
        fusion = lieux.merge(carac, on="Num_Acc", how="inner")
        atm_ok = fusion["atm"].isin(ATM)
        surf_ok = fusion["surf"].isin(SURF)
        atm_ignore += int((~atm_ok).sum())
        surf_ignore += int((atm_ok & ~surf_ok).sum())
        bons = fusion[atm_ok & surf_ok]
        couples.update(zip(bons["atm"], bons["surf"]))
    return couples, atm_ignore, surf_ignore


def reference():
    texte = (RESULTS / "reponse64.txt").read_text(encoding="utf-8")

    def entier(motif):
        m = re.search(motif, texte)
        return int(m.group(1).replace(" ", "").replace(" ", "")) if m else None

    return {
        "exploites": entier(r"Total accidents exploités.*?:\s*([\d   ]+)"),
        "atm_ignore": entier(r"atm non exploitable \(ignorés\)\s*:\s*([\d   ]+)"),
        "surf_ignore": entier(r"surf non exploitable \(ignorés\)\s*:\s*([\d   ]+)"),
        "top": entier(r"Couple le plus fréquent.*?\(([\d   ]+) accidents"),
    }


def main() -> int:
    trace = Trace("verification64.txt")
    trace("Vérification Q6.4 — heatmap atm × surf (pandas)")
    trace("=" * 72)

    couples, atm_ignore, surf_ignore = calcul_pandas()
    exploites = sum(couples.values())
    (top_couple, top_nb), = couples.most_common(1)
    ref = reference()

    controles = [
        ("accidents exploités", exploites, ref["exploites"]),
        ("atm ignorés", atm_ignore, ref["atm_ignore"]),
        ("surf ignorés", surf_ignore, ref["surf_ignore"]),
        ("couple le plus fréquent (effectif)", top_nb, ref["top"]),
    ]
    trace(f"{'contrôle':<38}{'pandas':>12}{'réponse':>12}{'==?':>6}")
    trace("-" * 72)
    ok = True
    for libelle, val, val_ref in controles:
        egal = val == val_ref
        ok = ok and egal
        trace(f"{libelle:<38}{val:>12}{(val_ref if val_ref is not None else '—'):>12}"
              f"{('✓' if egal else '✗'):>6}")
    trace("-" * 72)
    trace(f"Couple le plus fréquent (pandas) : {top_couple[0]} × {top_couple[1]}")
    trace("")

    if ok:
        trace("RÉSULTAT : ✓ VÉRIFIÉ — totaux exploités/ignorés et couple dominant")
        trace("           identiques à reponse64.txt.")
    else:
        trace("RÉSULTAT : ✗ DIVERGENCE (voir ✗).")

    trace.ecrire()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
