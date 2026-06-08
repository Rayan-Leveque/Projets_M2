"""Vérification Q6.2 — tués par tranche d'âge (5 ans) et sexe (pandas).

On recompte avec pandas le nombre d'usagers tués (grav = « 2 - Tué »),
métropolitains, ventilés par tranche d'âge (19 tranches) et par sexe, et on
recoupe avec question62.py (compter_tues_par_age_sexe, csv.reader).

Trace : results/verification62.txt
"""

import sys

import pandas as pd

import question62
from common import ENRICHED, ANNEE_DEBUT, ANNEE_FIN, normaliser_dep, Trace

NB_TRANCHES = 19


def indice_tranche(age: int) -> int:
    return 18 if age >= 90 else age // 5


def num_acc_metropole_pandas(annee: int) -> set[str]:
    df = pd.read_csv(
        ENRICHED / f"caracteristiques_{annee}.csv",
        usecols=["Num_Acc", "dep"], dtype=str, keep_default_na=False,
    )
    return set(df[df["dep"].map(normaliser_dep).notna()]["Num_Acc"])


def tues_pandas() -> tuple[list[int], list[int]]:
    hommes = [0] * NB_TRANCHES
    femmes = [0] * NB_TRANCHES
    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        metropole = num_acc_metropole_pandas(annee)
        df = pd.read_csv(
            ENRICHED / f"usagers_{annee}.csv",
            usecols=["Num_Acc", "grav", "sexe", "an_nais"],
            dtype=str, keep_default_na=False,
        )
        tues = df[(df["grav"] == "2 - Tué") & df["Num_Acc"].isin(metropole)].copy()
        an = tues["an_nais"].str.strip()
        valide = an.str.isdigit() & (an != "0")
        tues = tues[valide]
        age = annee - tues["an_nais"].str.strip().astype(int)
        tues = tues.assign(age=age)
        tues = tues[(tues["age"] >= 0) & (tues["age"] <= 120)]
        for a, s in zip(tues["age"], tues["sexe"]):
            t = indice_tranche(int(a))
            if s == "1 - Masculin":
                hommes[t] += 1
            elif s == "2 - Féminin":
                femmes[t] += 1
    return hommes, femmes


def main() -> int:
    trace = Trace("verification62.txt")
    trace("Vérification Q6.2 — tués par tranche d'âge et sexe (pandas vs csv)")
    trace("=" * 72)

    h_pandas, f_pandas = tues_pandas()
    h_ref, f_ref = question62.compter_tues_par_age_sexe()

    trace(f"{'tranche':<10}{'H pandas':>10}{'H q62':>8}{'F pandas':>10}{'F q62':>8}{'==?':>6}")
    trace("-" * 72)
    ok = True
    for i in range(NB_TRANCHES):
        libelle = "90+" if i == 18 else f"{i*5}-{i*5+4}"
        egal = (h_pandas[i] == h_ref[i]) and (f_pandas[i] == f_ref[i])
        ok = ok and egal
        trace(f"{libelle:<10}{h_pandas[i]:>10}{h_ref[i]:>8}{f_pandas[i]:>10}{f_ref[i]:>8}"
              f"{('✓' if egal else '✗'):>6}")
    trace("-" * 72)
    trace(f"{'TOTAL':<10}{sum(h_pandas):>10}{sum(h_ref):>8}{sum(f_pandas):>10}{sum(f_ref):>8}")
    trace("")

    if ok:
        trace("RÉSULTAT : ✓ VÉRIFIÉ — pandas et question62.py donnent les mêmes")
        trace(f"           effectifs (total tués = {sum(h_ref)+sum(f_ref)}).")
    else:
        trace("RÉSULTAT : ✗ DIVERGENCE sur au moins une tranche.")

    trace.ecrire()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
