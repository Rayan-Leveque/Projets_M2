"""Vérification Q2.3 — chaque lieu référence un accident existant (pandas).

Méthode indépendante de question23.py (csv + set) : pour chaque année on
fait lieux.merge(caracteristiques, how='left', indicator=True) sur Num_Acc.
Les lignes 'left_only' sont les lieux orphelins (Num_Acc absent côté
caractéristiques) — les violations. Comparaison à reponse23_violations.csv.

Trace : results/verification23.txt
"""

import sys

import pandas as pd

from common import ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN, Trace


def colonne_num_acc(annee: int, type_fichier: str) -> pd.DataFrame:
    chemin = ENRICHED / f"{type_fichier}_{annee}.csv"
    return pd.read_csv(
        chemin, usecols=["Num_Acc"], dtype=str, keep_default_na=False
    )


def main() -> int:
    trace = Trace("verification23.txt")
    trace("Vérification Q2.3 — lieux → caracteristiques (méthode pandas, anti-join)")
    trace("=" * 72)
    trace("Pour chaque année : lieux.merge(caracteristiques, how='left', indicator)")
    trace("sur Num_Acc. Les lignes 'left_only' sont des lieux sans accident parent.")
    trace("")
    trace(f"{'année':<8}{'lieux':>10}{'accidents':>12}{'violations':>13}")
    trace("-" * 72)

    violations: list[tuple[str, str]] = []
    total_lieux = 0
    total_viol = 0

    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        lieux = colonne_num_acc(annee, "lieux")
        carac = colonne_num_acc(annee, "caracteristiques").drop_duplicates(["Num_Acc"])

        fusion = lieux.merge(carac, on="Num_Acc", how="left", indicator=True)
        viol = fusion[fusion["_merge"] == "left_only"]

        total_lieux += len(lieux)
        total_viol += len(viol)
        for num_acc in viol["Num_Acc"]:
            violations.append((str(annee), num_acc))

        trace(f"{annee:<8}{len(lieux):>10}{len(carac):>12}{len(viol):>13}")

    trace("-" * 72)
    trace(f"{'TOTAL':<8}{total_lieux:>10}{'':>12}{total_viol:>13}")
    trace("")

    trace("Recoupement avec results/reponse23_violations.csv")
    trace("-" * 72)
    ref = pd.read_csv(
        RESULTS / "reponse23_violations.csv", dtype=str, keep_default_na=False
    )
    liste_pandas = sorted(violations)
    liste_ref = sorted(zip(ref["annee"], ref["Num_Acc"]))

    trace(f"Lignes de violation — pandas : {len(liste_pandas)} | réponse : {len(liste_ref)}")
    manquantes = sorted(set(liste_ref) - set(liste_pandas))
    en_trop = sorted(set(liste_pandas) - set(liste_ref))
    trace(f"Présentes dans la réponse, pas retrouvées par pandas : {len(manquantes)}")
    trace(f"Trouvées par pandas, absentes de la réponse          : {len(en_trop)}")
    trace("")

    ok = liste_pandas == liste_ref
    if ok:
        if total_viol == 0:
            trace("RÉSULTAT : ✓ VÉRIFIÉ — aucune violation par les deux méthodes :")
            trace("           tout lieu référence bien un accident existant.")
        else:
            trace(f"RÉSULTAT : ✓ VÉRIFIÉ — mêmes {len(liste_pandas)} violations.")
    else:
        trace("RÉSULTAT : ✗ DIVERGENCE — échantillons :")
        for cle in manquantes[:10]:
            trace(f"  manquant (réponse) : {cle}")
        for cle in en_trop[:10]:
            trace(f"  en trop (pandas)   : {cle}")

    trace.ecrire()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
