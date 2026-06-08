"""Vérification Q6.3 — top 10 des départements (pandas).

On recompte avec pandas le nombre d'accidents par département (France
métropolitaine, via normaliser_dep) sur 2005-2015, puis on compare le top 10
à results/reponse63.txt.

Trace : results/verification63.txt
"""

import re
import sys
from collections import Counter

import pandas as pd

from common import ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN, normaliser_dep, Trace


def comptes_pandas() -> Counter:
    total = Counter()
    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        df = pd.read_csv(
            ENRICHED / f"caracteristiques_{annee}.csv",
            usecols=["dep"], dtype=str, keep_default_na=False,
        )
        deps = df["dep"].map(normaliser_dep).dropna()
        total.update(deps.tolist())
    return total


def top10_reponse() -> list[tuple[str, int]]:
    texte = (RESULTS / "reponse63.txt").read_text(encoding="utf-8")
    ligne = re.compile(r"^\s*\d+\s+(\S+)\s+.+?\s+(\d+)\s*$")
    res = []
    for l in texte.splitlines():
        m = ligne.match(l)
        if m:
            res.append((m.group(1), int(m.group(2))))
    return res[:10]


def main() -> int:
    trace = Trace("verification63.txt")
    trace("Vérification Q6.3 — top 10 départements (pandas)")
    trace("=" * 72)

    comptes = comptes_pandas()
    top_pandas = comptes.most_common(10)
    top_ref = top10_reponse()

    trace(f"{'rang':<6}{'dép. pandas':>14}{'nb pandas':>12}{'dép. réponse':>15}{'nb réponse':>12}{'==?':>6}")
    trace("-" * 72)
    ok = True
    for i in range(10):
        dp, np_ = top_pandas[i]
        dr, nr = top_ref[i] if i < len(top_ref) else ("—", -1)
        egal = (dp == dr) and (np_ == nr)
        ok = ok and egal
        trace(f"{i+1:<6}{dp:>14}{np_:>12}{dr:>15}{nr:>12}{('✓' if egal else '✗'):>6}")
    trace("-" * 72)
    trace("")

    if ok:
        trace("RÉSULTAT : ✓ VÉRIFIÉ — même top 10 (département et effectif) que reponse63.txt.")
    else:
        trace("RÉSULTAT : ✗ DIVERGENCE dans le top 10.")

    trace.ecrire()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
