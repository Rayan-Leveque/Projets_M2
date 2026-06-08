"""Vérification Q1.1 — sortie UTF-8 + séparateur ',' (pandas).

question11.py a produit data/utf8/. On vérifie ici, indépendamment, que les
44 fichiers produits respectent bien les deux garanties attendues :
  1. ils se décodent intégralement en UTF-8 (lecture binaire puis .decode) ;
  2. leur séparateur est bien ',' : lus par pandas avec sep=',', ils
     présentent EXACTEMENT le nombre de colonnes attendu pour leur type
     (un mauvais séparateur donnerait une seule colonne).

Trace : results/verification11.txt
"""

import sys

import pandas as pd

from common import UTF8, ANNEE_DEBUT, ANNEE_FIN, TYPES_FICHIERS, Trace

# Nombre de colonnes attendu par type (schéma BAAC 2005-2015).
NB_COLONNES = {
    "caracteristiques": 16,
    "lieux": 18,
    "vehicules": 9,
    "usagers": 12,
}


def main() -> int:
    trace = Trace("verification11.txt")
    trace("Vérification Q1.1 — fichiers utf8/ : encodage UTF-8 + séparateur ','")
    trace("=" * 72)
    trace("Pour chaque fichier : (1) décodage UTF-8 complet, (2) lecture pandas")
    trace("sep=',' et contrôle du nombre de colonnes attendu par type.")
    trace("")

    total = 0
    ok_total = 0
    erreurs: list[str] = []

    for type_fichier in TYPES_FICHIERS:
        attendu = NB_COLONNES[type_fichier]
        trace(f"--- {type_fichier} ({attendu} colonnes attendues) ---")
        for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
            chemin = UTF8 / f"{type_fichier}_{annee}.csv"
            total += 1
            nom = chemin.name

            # 1. décodage UTF-8
            try:
                chemin.read_bytes().decode("utf-8")
                utf8_ok = True
            except UnicodeDecodeError as e:
                utf8_ok = False
                erreurs.append(f"{nom} : décodage UTF-8 échoué ({e})")

            # 2. séparateur ',' -> nombre de colonnes
            entete = pd.read_csv(chemin, sep=",", nrows=0, dtype=str)
            ncols = entete.shape[1]
            sep_ok = ncols == attendu
            if not sep_ok:
                erreurs.append(
                    f"{nom} : {ncols} colonnes lues avec sep=',' (attendu {attendu})"
                )

            if utf8_ok and sep_ok:
                ok_total += 1
            else:
                trace(f"  ✗ {nom} : utf8={utf8_ok}, colonnes={ncols}/{attendu}")

    trace("")
    trace(f"Fichiers conformes : {ok_total} / {total}")
    trace("")
    ok = ok_total == total
    if ok:
        trace("RÉSULTAT : ✓ VÉRIFIÉ — les 44 fichiers utf8/ sont en UTF-8 et")
        trace("           séparés par ',' avec le bon nombre de colonnes.")
    else:
        trace("RÉSULTAT : ✗ ANOMALIES :")
        for e in erreurs[:20]:
            trace(f"  - {e}")

    trace.ecrire()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
