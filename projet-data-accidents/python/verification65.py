"""Vérification Q6.5 — comptes annuels par département du GIF (pandas).

Le GIF de question65.py empile une image par année, chacune construite à
partir du nombre d'accidents métropolitains par département de l'année. On
recompte ces comptes annuels avec pandas et on les recoupe, année par année,
avec la fonction compter_accidents_par_departement de question65.py.

Trace : results/verification65.txt
"""

import sys

import pandas as pd

import question65
from common import ENRICHED, ANNEE_DEBUT, ANNEE_FIN, normaliser_dep, Trace


def comptes_pandas(annee: int) -> dict[str, int]:
    df = pd.read_csv(
        ENRICHED / f"caracteristiques_{annee}.csv",
        usecols=["dep"], dtype=str, keep_default_na=False,
    )
    deps = df["dep"].map(normaliser_dep).dropna()
    return {d: int(n) for d, n in deps.value_counts().items()}


def main() -> int:
    trace = Trace("verification65.txt")
    trace("Vérification Q6.5 — comptes annuels par département (pandas vs csv)")
    trace("=" * 72)
    trace(f"{'année':<8}{'départements':>14}{'total métropole':>18}{'== question65 ?':>18}")
    trace("-" * 72)

    tout_ok = True
    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        pandas_compte = comptes_pandas(annee)
        ref = dict(question65.compter_accidents_par_departement(annee))
        egal = pandas_compte == ref
        tout_ok = tout_ok and egal
        trace(f"{annee:<8}{len(pandas_compte):>14}{sum(pandas_compte.values()):>18}"
              f"{('✓' if egal else '✗'):>18}")
        if not egal:
            deps = set(pandas_compte) | set(ref)
            for d in sorted(deps):
                if pandas_compte.get(d) != ref.get(d):
                    trace(f"    {annee} dép {d} : pandas={pandas_compte.get(d)} "
                          f"vs q65={ref.get(d)}")

    trace("-" * 72)
    trace("")
    if tout_ok:
        trace("RÉSULTAT : ✓ VÉRIFIÉ — pour chaque année, pandas et question65.py")
        trace("           donnent les mêmes comptes par département.")
    else:
        trace("RÉSULTAT : ✗ DIVERGENCE sur au moins une année (voir détails).")

    trace.ecrire()
    return 0 if tout_ok else 1


if __name__ == "__main__":
    sys.exit(main())
