"""Vérification Q3.1 — répartition en % des attributs énumérés usagers (pandas).

question31.py compte les modalités avec csv.reader + Counter. On recompte
ici avec pandas (value_counts) sur les ~1,74 M usagers cumulés, puis on
recoupe avec results/reponse31.txt.

Stratégie de recoupement robuste : pour chaque attribut, on compare le
MULTISET des effectifs (triés) calculé par pandas à celui lu dans la trace
de réponse. Les effectifs identifient la distribution sans dépendre du
libellé affiché (utile pour secu, affiché sous forme décodée).

Trace : results/verification31.txt
"""

import re
import sys
from collections import Counter

import pandas as pd

from common import ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN, Trace

ATTRS = ["catu", "grav", "sexe", "trajet", "secu", "locp", "actp", "etatp"]


def effectifs_pandas() -> tuple[dict[str, Counter], int]:
    compteurs = {a: Counter() for a in ATTRS}
    total = 0
    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        df = pd.read_csv(
            ENRICHED / f"usagers_{annee}.csv",
            usecols=ATTRS, dtype=str, keep_default_na=False,
        )
        total += len(df)
        for a in ATTRS:
            compteurs[a].update(df[a].tolist())
    return compteurs, total


def effectifs_reponse() -> dict[str, list[int]]:
    """Parse reponse31.txt : effectifs (1er entier après le « % ») par attribut."""
    texte = (RESULTS / "reponse31.txt").read_text(encoding="utf-8")
    par_attribut: dict[str, list[int]] = {}
    courant = None
    en_tete = re.compile(r"Attribut « (\w+) »")
    ligne_data = re.compile(r"^\s*\d+\.\d+ %\s+(\d+)\b")
    for ligne in texte.splitlines():
        m = en_tete.search(ligne)
        if m:
            courant = m.group(1)
            par_attribut[courant] = []
            continue
        if courant:
            md = ligne_data.match(ligne)
            if md:
                par_attribut[courant].append(int(md.group(1)))
    return par_attribut


def main() -> int:
    trace = Trace("verification31.txt")
    trace("Vérification Q3.1 — répartition % attributs usagers (pandas)")
    trace("=" * 72)

    compteurs, total = effectifs_pandas()
    ref = effectifs_reponse()

    trace(f"Total usagers (pandas) : {total}")
    trace("")
    trace(f"{'attribut':<10}{'modalités':>11}{'somme eff.':>13}{'= total ?':>11}{'eff. == réponse ?':>20}")
    trace("-" * 72)

    tout_ok = True
    for a in ATTRS:
        eff_pandas = sorted(compteurs[a].values(), reverse=True)
        somme = sum(eff_pandas)
        eff_ref = sorted(ref.get(a, []), reverse=True)
        total_ok = somme == total
        eff_ok = eff_pandas == eff_ref
        tout_ok = tout_ok and total_ok and eff_ok
        trace(f"{a:<10}{len(eff_pandas):>11}{somme:>13}"
              f"{('✓' if total_ok else '✗'):>11}{('✓' if eff_ok else '✗'):>20}")

    trace("-" * 72)
    trace("")
    trace("Lecture : « somme eff. = total » confirme que chaque usager compte pour")
    trace("exactement une modalité (bon dénominateur) ; « eff. == réponse » confirme")
    trace("que pandas retrouve exactement les mêmes effectifs que question31.py.")
    trace("")

    if tout_ok:
        trace("RÉSULTAT : ✓ VÉRIFIÉ — distributions pandas identiques à reponse31.txt")
        trace(f"           sur les {len(ATTRS)} attributs, dénominateur = {total}.")
    else:
        trace("RÉSULTAT : ✗ DIVERGENCE sur au moins un attribut (voir colonnes ✗).")
        for a in ATTRS:
            ep = sorted(compteurs[a].values(), reverse=True)
            er = sorted(ref.get(a, []), reverse=True)
            if ep != er:
                trace(f"  {a} : pandas={ep[:5]}… ({len(ep)}) vs réponse={er[:5]}… ({len(er)})")

    trace.ecrire()
    return 0 if tout_ok else 1


if __name__ == "__main__":
    sys.exit(main())
