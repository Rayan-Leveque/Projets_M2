"""Vérification Q2.1 — intégrité référentielle usagers → vehicules (pandas).

Le script-réponse question21.py utilise csv.reader + un `set` de couples.
Ici on RE-CALCULE le même résultat par une méthode indépendante : DataFrames
pandas + anti-join (merge avec indicator='left_only'). Une divergence entre
les deux méthodes révélerait un bug ; leur accord constitue la vérification.

Recoupements effectués :
  1. nb de violations pandas par année et au total ;
  2. l'ENSEMBLE des couples en violation (annee, Num_Acc, num_veh) trouvé par
     pandas est-il exactement celui de results/reponse21_violations.csv ?

Trace : results/verification21.txt
"""

import sys

import pandas as pd

from common import ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN, Trace


def charger(annee: int, type_fichier: str) -> pd.DataFrame:
    """Charge (Num_Acc, num_veh) en chaînes, cellules vides = '' (comme csv.reader)."""
    chemin = ENRICHED / f"{type_fichier}_{annee}.csv"
    return pd.read_csv(
        chemin,
        usecols=["Num_Acc", "num_veh"],
        dtype=str,
        keep_default_na=False,  # une cellule vide reste "" et non NaN
    )


def main() -> int:
    trace = Trace("verification21.txt")
    trace("Vérification Q2.1 — usagers → vehicules (méthode pandas, anti-join)")
    trace("=" * 70)
    trace("Méthode indépendante de question21.py (csv + set) : pour chaque année,")
    trace("usagers.merge(vehicules, how='left', indicator=True) ; les lignes")
    trace("'left_only' sont les usagers sans véhicule correspondant.")
    trace("")
    trace(f"{'année':<8}{'usagers':>10}{'couples véh.':>15}{'violations':>13}")
    trace("-" * 70)

    violations_pandas: list[tuple[str, str, str]] = []  # (annee, Num_Acc, num_veh)
    total_usagers = 0
    total_violations = 0

    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        usa = charger(annee, "usagers")
        veh = charger(annee, "vehicules")
        couples_veh = veh.drop_duplicates(["Num_Acc", "num_veh"])

        fusion = usa.merge(
            couples_veh, on=["Num_Acc", "num_veh"], how="left", indicator=True
        )
        viol = fusion[fusion["_merge"] == "left_only"]

        total_usagers += len(usa)
        total_violations += len(viol)
        for num_acc, num_veh in zip(viol["Num_Acc"], viol["num_veh"]):
            violations_pandas.append((str(annee), num_acc, num_veh))

        trace(f"{annee:<8}{len(usa):>10}{len(couples_veh):>15}{len(viol):>13}")

    trace("-" * 70)
    trace(f"{'TOTAL':<8}{total_usagers:>10}{'':>15}{total_violations:>13}")
    trace("")

    # --- Recoupement avec le fichier de violations du script-réponse ---------
    trace("Recoupement avec results/reponse21_violations.csv")
    trace("-" * 70)
    ref = pd.read_csv(
        RESULTS / "reponse21_violations.csv", dtype=str, keep_default_na=False
    )
    # On compare le multiset complet (une ligne par usager, doublons de couple
    # conservés) ET, à titre indicatif, le nombre de couples distincts.
    liste_pandas = sorted(violations_pandas)
    liste_ref = sorted(zip(ref["annee"], ref["Num_Acc"], ref["num_veh"]))

    trace(f"Lignes de violation — pandas : {len(liste_pandas)} | réponse : {len(liste_ref)}")
    trace(f"Couples (Num_Acc, num_veh) distincts — pandas : {len(set(liste_pandas))} "
          f"| réponse : {len(set(liste_ref))}")
    manquantes = sorted(set(liste_ref) - set(liste_pandas))
    en_trop = sorted(set(liste_pandas) - set(liste_ref))
    trace(f"Couples présents dans la réponse mais pas retrouvés par pandas : {len(manquantes)}")
    trace(f"Couples trouvés par pandas mais absents de la réponse          : {len(en_trop)}")
    trace("")

    ok = liste_pandas == liste_ref
    if ok:
        trace("RÉSULTAT : ✓ VÉRIFIÉ — les deux méthodes (csv/set et pandas/merge)")
        trace("           produisent exactement les mêmes lignes de violation")
        trace(f"           ({len(liste_pandas)} lignes, {len(set(liste_pandas))} couples distincts).")
    else:
        trace("RÉSULTAT : ✗ DIVERGENCE — voir échantillons ci-dessous.")
        for cle in manquantes[:10]:
            trace(f"  manquant (réponse) : {cle}")
        for cle in en_trop[:10]:
            trace(f"  en trop (pandas)   : {cle}")

    trace.ecrire()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
