"""Vérification Q2.2 — chaque véhicule a ≥ 1 usager (pandas, anti-join).

Méthode indépendante de question22.py (csv + set) : pour chaque année on
fait vehicules.merge(usagers, how='left', indicator=True) sur (Num_Acc,
num_veh). Les lignes 'left_only' sont les véhicules SANS aucun usager
rattaché — les violations. On compare le multiset obtenu à
results/reponse22_violations.csv.

Trace : results/verification22.txt
"""

import sys

import pandas as pd

from common import ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN, Trace


def charger(annee: int, type_fichier: str) -> pd.DataFrame:
    chemin = ENRICHED / f"{type_fichier}_{annee}.csv"
    return pd.read_csv(
        chemin, usecols=["Num_Acc", "num_veh"], dtype=str, keep_default_na=False
    )


def main() -> int:
    trace = Trace("verification22.txt")
    trace("Vérification Q2.2 — vehicules → ≥ 1 usager (méthode pandas, anti-join)")
    trace("=" * 72)
    trace("Pour chaque année : vehicules.merge(usagers, how='left', indicator).")
    trace("Les lignes 'left_only' sont les véhicules sans usager rattaché.")
    trace("")
    trace(f"{'année':<8}{'véhicules':>11}{'couples usagers':>17}{'violations':>13}")
    trace("-" * 72)

    violations: list[tuple[str, str, str]] = []
    total_veh = 0
    total_viol = 0

    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        veh = charger(annee, "vehicules")
        usa = charger(annee, "usagers").drop_duplicates(["Num_Acc", "num_veh"])

        fusion = veh.merge(
            usa, on=["Num_Acc", "num_veh"], how="left", indicator=True
        )
        viol = fusion[fusion["_merge"] == "left_only"]

        total_veh += len(veh)
        total_viol += len(viol)
        for num_acc, num_veh in zip(viol["Num_Acc"], viol["num_veh"]):
            violations.append((str(annee), num_acc, num_veh))

        trace(f"{annee:<8}{len(veh):>11}{len(usa):>17}{len(viol):>13}")

    trace("-" * 72)
    trace(f"{'TOTAL':<8}{total_veh:>11}{'':>17}{total_viol:>13}")
    trace("")

    trace("Recoupement avec results/reponse22_violations.csv")
    trace("-" * 72)
    ref = pd.read_csv(
        RESULTS / "reponse22_violations.csv", dtype=str, keep_default_na=False
    )
    liste_pandas = sorted(violations)
    liste_ref = sorted(zip(ref["annee"], ref["Num_Acc"], ref["num_veh"]))

    trace(f"Lignes de violation — pandas : {len(liste_pandas)} | réponse : {len(liste_ref)}")
    manquantes = sorted(set(liste_ref) - set(liste_pandas))
    en_trop = sorted(set(liste_pandas) - set(liste_ref))
    trace(f"Présentes dans la réponse, pas retrouvées par pandas : {len(manquantes)}")
    trace(f"Trouvées par pandas, absentes de la réponse          : {len(en_trop)}")
    trace("")

    ok = liste_pandas == liste_ref
    if ok:
        trace(f"RÉSULTAT : ✓ VÉRIFIÉ — mêmes {len(liste_pandas)} violations par les deux méthodes.")
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
