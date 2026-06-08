"""Vérification Q4.1 — taux de valeurs absentes par champ véhicules (pandas).

question41.py compte les absences avec csv.reader. On recompte ici avec
pandas, sur les ~1,33 M véhicules cumulés, en appliquant la même convention
d'absence puis on recoupe colonne par colonne avec results/reponse41.txt.

Convention (identique à question41.py) :
  - marqueurs d'absence : '', '.', '-1', '0', '00', '000' ;
  - pour les colonnes enrichies (catv, obs, obsm, choc, manv) le test porte
    sur le code (partie avant « - »), sinon sur la valeur brute.

Trace : results/verification41.txt
"""

import re
import sys

import pandas as pd

from common import ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN, Trace

COLONNES = ["Num_Acc", "senc", "catv", "occutc", "obs", "obsm", "choc", "manv", "num_veh"]
COLONNES_ENRICHIES = {"catv", "obs", "obsm", "choc", "manv"}
MARQUEURS_ABSENTS = {"", ".", "-1", "0", "00", "000"}


def code(colonne: str, valeur: str) -> str:
    """Code testé pour l'absence : avant « - » si colonne enrichie, sinon brut."""
    v = valeur.strip()
    if colonne in COLONNES_ENRICHIES and " - " in v:
        return v.split(" - ", 1)[0].strip()
    return v


def absences_pandas() -> tuple[dict[str, int], int]:
    manquants = {c: 0 for c in COLONNES}
    total = 0
    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        df = pd.read_csv(
            ENRICHED / f"vehicules_{annee}.csv",
            usecols=COLONNES, dtype=str, keep_default_na=False,
        )
        total += len(df)
        for c in COLONNES:
            codes = df[c].map(lambda v, col=c: code(col, v))
            manquants[c] += int(codes.isin(MARQUEURS_ABSENTS).sum())
    return manquants, total


def absences_reponse() -> dict[str, int]:
    """Parse reponse41.txt : (colonne -> nb_manquants)."""
    texte = (RESULTS / "reponse41.txt").read_text(encoding="utf-8")
    ref: dict[str, int] = {}
    ligne = re.compile(r"^(\w+)\s+(\d+)\s+[\d.]+%")
    for l in texte.splitlines():
        m = ligne.match(l)
        if m:
            ref[m.group(1)] = int(m.group(2))
    return ref


def main() -> int:
    trace = Trace("verification41.txt")
    trace("Vérification Q4.1 — taux de valeurs absentes véhicules (pandas)")
    trace("=" * 72)

    manquants, total = absences_pandas()
    ref = absences_reponse()

    trace(f"Total véhicules (pandas) : {total}")
    trace("")
    trace(f"{'colonne':<10}{'manquants (pandas)':>20}{'taux_%':>10}{'réponse':>12}{'==?':>6}")
    trace("-" * 72)

    tout_ok = True
    for c in COLONNES:
        nb = manquants[c]
        taux = nb / total * 100 if total else 0.0
        nb_ref = ref.get(c)
        egal = nb_ref is not None and nb == nb_ref
        tout_ok = tout_ok and egal
        trace(f"{c:<10}{nb:>20}{taux:>9.2f}%{(nb_ref if nb_ref is not None else '—'):>12}"
              f"{('✓' if egal else '✗'):>6}")

    trace("-" * 72)
    trace("")
    if tout_ok:
        trace("RÉSULTAT : ✓ VÉRIFIÉ — pandas retrouve exactement les nb_manquants")
        trace(f"           de reponse41.txt sur les {len(COLONNES)} colonnes (total {total}).")
    else:
        trace("RÉSULTAT : ✗ DIVERGENCE sur au moins une colonne (voir ✗).")

    trace.ecrire()
    return 0 if tout_ok else 1


if __name__ == "__main__":
    sys.exit(main())
