"""Vérification Q5.3 — année de naissance impossible (pandas).

Réimplémentation indépendante (pandas) du critère de question53.py : an_nais
renseignée (≠ '', '0', '00', '.', et numérique) mais > 2015 (naissance après
l'accident) ou < 1900 (> 105 ans). Comparaison à reponse53_complet.csv
(clé : annee, Num_Acc, num_veh, an_nais, motif).

Trace : results/verification53.txt
"""

import sys

import pandas as pd

from common import ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN, Trace

IGNORES = {"", "0", "00", "."}


def incoherences_pandas() -> list[tuple[str, str, str, str, str]]:
    flags: list[tuple[str, str, str, str, str]] = []
    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        df = pd.read_csv(
            ENRICHED / f"usagers_{annee}.csv",
            usecols=["Num_Acc", "num_veh", "an_nais"],
            dtype=str, keep_default_na=False,
        )
        v = df["an_nais"].str.strip()
        testable = (~v.isin(IGNORES)) & v.str.isdigit()
        w = df[testable].copy()
        an = w["an_nais"].str.strip().astype(int)
        futur = an > 2015
        trop_vieux = an < 1900
        w = w[futur | trop_vieux]
        motifs = []
        for valeur in w["an_nais"].str.strip().astype(int):
            motifs.append("Naissance future (> 2015)" if valeur > 2015
                          else "Âge invraisemblable (< 1900)")
        for (num_acc, num_veh, an_nais), motif in zip(
            zip(w["Num_Acc"], w["num_veh"], w["an_nais"]), motifs
        ):
            flags.append((str(annee), num_acc, num_veh, an_nais, motif))
    return flags


def main() -> int:
    trace = Trace("verification53.txt")
    trace("Vérification Q5.3 — année de naissance impossible (pandas)")
    trace("=" * 72)
    trace("Critère : an_nais renseignée et numérique, mais > 2015 ou < 1900.")
    trace("")

    flags = incoherences_pandas()
    ref = pd.read_csv(
        RESULTS / "reponse53_complet.csv", dtype=str, keep_default_na=False
    )
    # Recoupement sur (annee, Num_Acc, num_veh, an_nais) — le motif dépend du
    # libellé exact, on le compare à part pour rester robuste.
    cle_pandas = sorted((a, n, v, an) for a, n, v, an, _ in flags)
    cle_ref = sorted(zip(ref["annee"], ref["Num_Acc"], ref["num_veh"], ref["an_nais"]))

    trace(f"Incohérences pandas : {len(cle_pandas)} | réponse : {len(cle_ref)}")
    manquantes = sorted(set(cle_ref) - set(cle_pandas))
    en_trop = sorted(set(cle_pandas) - set(cle_ref))
    trace(f"Présentes dans la réponse, pas retrouvées par pandas : {len(manquantes)}")
    trace(f"Trouvées par pandas, absentes de la réponse          : {len(en_trop)}")
    trace("")
    trace("Échantillon des cas trouvés par pandas :")
    for a, n, v, an, motif in flags[:10]:
        trace(f"  {a}  Num_Acc={n}  num_veh={v}  an_nais={an}  ({motif})")
    trace("")

    ok = cle_pandas == cle_ref
    if ok:
        trace(f"RÉSULTAT : ✓ VÉRIFIÉ — mêmes {len(cle_pandas)} incohérences par les deux méthodes.")
    else:
        trace("RÉSULTAT : ✗ DIVERGENCE — échantillons :")
        for c in manquantes[:10]:
            trace(f"  manquant (réponse) : {c}")
        for c in en_trop[:10]:
            trace(f"  en trop (pandas)   : {c}")

    trace.ecrire()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
