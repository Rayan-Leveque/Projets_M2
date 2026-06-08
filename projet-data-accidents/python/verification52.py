"""Vérification Q5.2 — incohérence obsm × choc (pandas).

Réimplémentation indépendante (pandas) du critère de question52.py : un
véhicule a heurté un obstacle mobile (obsm ∈ {1,2,4,5,6,9}) alors qu'aucun
point de choc n'est enregistré (choc = « 0 - Aucun »). Comparaison à
results/reponse52_complet.csv (clé : annee, Num_Acc, num_veh).

Trace : results/verification52.txt
"""

import sys

import pandas as pd

from common import ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN, Trace

CODES_OBSTACLE_MOBILE = {"1", "2", "4", "5", "6", "9"}


def incoherences_pandas() -> list[tuple[str, str, str]]:
    flags: list[tuple[str, str, str]] = []
    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        df = pd.read_csv(
            ENRICHED / f"vehicules_{annee}.csv",
            usecols=["Num_Acc", "num_veh", "obsm", "choc"],
            dtype=str, keep_default_na=False,
        )
        code_obsm = df["obsm"].str.split(" - ", n=1).str[0].str.strip()
        obstacle = code_obsm.isin(CODES_OBSTACLE_MOBILE)
        choc_aucun = df["choc"].str.startswith("0 - ")
        viol = df[obstacle & choc_aucun]
        for num_acc, num_veh in zip(viol["Num_Acc"], viol["num_veh"]):
            flags.append((str(annee), num_acc, num_veh))
    return flags


def main() -> int:
    trace = Trace("verification52.txt")
    trace("Vérification Q5.2 — incohérence obsm × choc (pandas)")
    trace("=" * 72)
    trace("Critère : obsm ∈ {1,2,4,5,6,9} (obstacle mobile heurté) ET choc = « 0 - Aucun ».")
    trace("")

    flags = incoherences_pandas()
    ref = pd.read_csv(
        RESULTS / "reponse52_complet.csv", dtype=str, keep_default_na=False
    )
    liste_pandas = sorted(flags)
    liste_ref = sorted(zip(ref["annee"], ref["Num_Acc"], ref["num_veh"]))

    trace(f"Incohérences pandas : {len(liste_pandas)} | réponse : {len(liste_ref)}")
    manquantes = sorted(set(liste_ref) - set(liste_pandas))
    en_trop = sorted(set(liste_pandas) - set(liste_ref))
    trace(f"Présentes dans la réponse, pas retrouvées par pandas : {len(manquantes)}")
    trace(f"Trouvées par pandas, absentes de la réponse          : {len(en_trop)}")
    trace("")

    ok = liste_pandas == liste_ref
    if ok:
        trace(f"RÉSULTAT : ✓ VÉRIFIÉ — mêmes {len(liste_pandas)} incohérences par les deux méthodes.")
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
