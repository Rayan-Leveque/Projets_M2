"""Vérification Q2.4 — chaque accident se déroule sur un et un seul lieu (pandas).

Méthode indépendante de question24.py (csv + Counter) : pour chaque année on
compte le nombre de lignes de lieux par Num_Acc (groupby.size), puis on
associe ce compte à chaque accident des caractéristiques. Un accident est en
violation si son nombre de lieux est différent de 1 (0 = aucun lieu, ≥ 2 =
plusieurs lieux). Comparaison à reponse24_violations.csv.

Trace : results/verification24.txt
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
    trace = Trace("verification24.txt")
    trace("Vérification Q2.4 — un et un seul lieu par accident (méthode pandas)")
    trace("=" * 72)
    trace("Pour chaque année : nb_lieux = lieux.groupby('Num_Acc').size(), reporté")
    trace("sur chaque accident. Violation si nb_lieux != 1 (0 = sans lieu, ≥2 = multi).")
    trace("")
    trace(f"{'année':<8}{'accidents':>11}{'sans lieu':>11}{'≥2 lieux':>11}{'violations':>13}")
    trace("-" * 72)

    violations: list[tuple[str, str, str]] = []  # (Num_Acc, nb_lieux, annee)
    total_acc = 0
    total_viol = 0

    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        lieux = colonne_num_acc(annee, "lieux")
        carac = colonne_num_acc(annee, "caracteristiques").drop_duplicates(["Num_Acc"])

        compte = lieux.groupby("Num_Acc").size()  # Num_Acc -> nb de lieux
        nb_lieux = carac["Num_Acc"].map(compte).fillna(0).astype(int)

        sans = int((nb_lieux == 0).sum())
        multi = int((nb_lieux >= 2).sum())
        masque = nb_lieux != 1
        viol = carac[masque]
        nb_viol = nb_lieux[masque]

        total_acc += len(carac)
        total_viol += int(masque.sum())
        for num_acc, n in zip(viol["Num_Acc"], nb_viol):
            violations.append((num_acc, str(int(n)), str(annee)))

        trace(f"{annee:<8}{len(carac):>11}{sans:>11}{multi:>11}{int(masque.sum()):>13}")

    trace("-" * 72)
    trace(f"{'TOTAL':<8}{total_acc:>11}{'':>11}{'':>11}{total_viol:>13}")
    trace("")

    trace("Recoupement avec results/reponse24_violations.csv")
    trace("-" * 72)
    ref = pd.read_csv(
        RESULTS / "reponse24_violations.csv", dtype=str, keep_default_na=False
    )
    liste_pandas = sorted(violations)
    liste_ref = sorted(zip(ref["Num_Acc"], ref["nb_lieux"], ref["annee"]))

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
            trace("           chaque accident a exactement un lieu.")
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
