"""Question 5.3 — Incohérence sur l'année de naissance (`an_nais`).

Troisième situation d'incohérence inter-attributs, différente de Q5.1
(`lum` × `hrmn`) et Q5.2 (`obsm` × `choc`) : on confronte l'**année de
naissance** d'un usager (`an_nais`, table *usagers*) à la **période d'étude**
2005-2015 (Groupe 1), implicitement portée par l'année du fichier.

Règle d'incohérence :

  - `an_nais` est renseignée (cellule non vide et différente de « 0 ») ;
  - mais elle désigne une naissance **impossible** au regard de la période :
      * `an_nais > 2015` → l'usager naîtrait après l'accident le plus tardif
        de la fenêtre : impossible d'être victime avant d'être né ;
      * `an_nais < 1900` → l'usager aurait plus de 105 ans au moment des
        faits : valeur quasi certainement erronée (saisie, OCR, faute de
        frappe).

Les deux bornes (1900 et 2015) sont volontairement larges pour ne signaler
que des cas francs : on ne juge pas « suspect » un centenaire de 100 ans, on
ne retient que l'impossible (naissance future) et l'invraisemblable extrême
(> 105 ans).

Valeurs ignorées (information manquante, ligne non testable) : cellule vide,
« 0 », « 00 », « . » — codes de valeur manquante recensés dans l'inventaire des
données. Toute autre valeur non numérique est également ignorée.

Méthode : un simple parcours `csv.reader` année par année (2005-2015, Groupe 1),
sans pandas, pour rester lisible à la soutenance.

Sorties :
  - results/reponse53.txt          : nb total d'incohérences, les 10 premiers
                                     cas, commentaires.
  - results/reponse53_complet.csv  : rapport complet de toutes les incohérences
                                     (annee, Num_Acc, num_veh, an_nais, motif).
"""

import csv
import sys

from common import ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN

# Bornes de plausibilité pour l'année de naissance.
AN_NAIS_MIN = 1900          # en deçà : plus de 105 ans → invraisemblable
AN_NAIS_MAX = ANNEE_FIN     # au-delà de 2015 : naissance après l'accident

# Codes de valeur manquante pour an_nais (cf. inventaire des données).
VALEURS_MANQUANTES = {"", "0", "00", "."}


def annee_naissance(an_nais: str) -> int | None:
    """Renvoie l'année de naissance (int), ou None si non testable.

    Non testable = cellule manquante (vide, « 0 », « 00 », « . ») ou non
    numérique.
    """
    v = an_nais.strip()
    if v in VALEURS_MANQUANTES:
        return None
    if not v.isdigit():
        return None
    return int(v)


def motif_incoherence(an: int) -> str | None:
    """Renvoie le motif d'incohérence pour une année de naissance, ou None."""
    if an > AN_NAIS_MAX:
        return "Naissance postérieure à la période (an_nais > 2015)"
    if an < AN_NAIS_MIN:
        return "Naissance trop ancienne, > 105 ans (an_nais < 1900)"
    return None


def detecter_incoherences() -> tuple[list[dict], int]:
    """Parcourt 2005-2015 et renvoie (incoherences, nb_lignes_testées).

    Chaque incohérence est un dict : annee, Num_Acc, num_veh, an_nais, motif.
    Une ligne usager est « testée » dès lors que `an_nais` est renseignée.
    """
    incoherences: list[dict] = []
    nb_testes = 0

    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        chemin = ENRICHED / f"usagers_{annee}.csv"
        print(f"[..]   {annee}")
        with chemin.open("r", encoding="utf-8", newline="") as f:
            lecteur = csv.reader(f)
            entete = next(lecteur)
            idx_acc = entete.index("Num_Acc")
            idx_veh = entete.index("num_veh")
            idx_nais = entete.index("an_nais")
            for ligne in lecteur:
                an = annee_naissance(ligne[idx_nais])
                if an is None:
                    continue  # an_nais manquante ou non numérique → non testable
                nb_testes += 1
                motif = motif_incoherence(an)
                if motif is not None:
                    incoherences.append({
                        "annee": annee,
                        "Num_Acc": ligne[idx_acc],
                        "num_veh": ligne[idx_veh].strip(),
                        "an_nais": an,
                        "motif": motif,
                    })
        print(f"  [OK] {annee} : {len(incoherences)} incohérences cumulées")

    return incoherences, nb_testes


def ecrire_csv_complet(incoherences: list[dict]) -> None:
    """Écrit results/reponse53_complet.csv : toutes les incohérences."""
    chemin = RESULTS / "reponse53_complet.csv"
    colonnes = ["annee", "Num_Acc", "num_veh", "an_nais", "motif"]
    with chemin.open("w", encoding="utf-8", newline="") as f:
        ecrivain = csv.DictWriter(f, fieldnames=colonnes)
        ecrivain.writeheader()
        for inc in incoherences:
            ecrivain.writerow(inc)
    print(f"Rapport complet écrit dans {chemin}")


def ecrire_rapport(incoherences: list[dict], nb_testes: int) -> None:
    """Écrit results/reponse53.txt : total, 10 premiers cas, commentaires."""
    chemin = RESULTS / "reponse53.txt"
    nb = len(incoherences)
    taux = nb / nb_testes * 100 if nb_testes else 0.0

    # Répartition par motif, pour le commentaire.
    nb_futur = sum(1 for i in incoherences if i["an_nais"] > AN_NAIS_MAX)
    nb_ancien = nb - nb_futur

    # Phrase de commentaire adaptée à la répartition réellement observée.
    if nb_futur == 0:
        repartition = (
            "- Dans cette fenêtre, toutes les anomalies sont des années "
            "antérieures à 1900,\n  typiques d'erreurs de saisie ou de relevé "
            "(p. ex. 1789, 1066, ou une\n  inversion de chiffres) ; aucune "
            "naissance postérieure à 2015 n'apparaît.\n"
        )
    elif nb_ancien == 0:
        repartition = (
            "- Dans cette fenêtre, toutes les anomalies sont des naissances "
            "postérieures à\n  2015, c'est-à-dire après l'accident : "
            "impossibles, elles relèvent\n  d'erreurs de saisie ou de frappe.\n"
        )
    else:
        repartition = (
            f"- Les anomalies se répartissent entre {nb_ancien} naissances "
            f"trop anciennes\n  (< 1900) et {nb_futur} naissances postérieures "
            "à 2015 ; les deux relèvent\n  d'erreurs de saisie ou de frappe.\n"
        )

    with chemin.open("w", encoding="utf-8") as f:
        f.write("Question 5.3 — Incohérence sur an_nais (année de naissance)\n")
        f.write("=" * 68 + "\n\n")
        f.write(f"Période : {ANNEE_DEBUT}-{ANNEE_FIN} (Groupe 1)\n")
        f.write(f"Source  : {ENRICHED} (table usagers)\n\n")
        f.write("Règle d'incohérence appliquée :\n")
        f.write(f"  - an_nais > {AN_NAIS_MAX} (naissance après l'accident le plus "
                "tardif)  → incohérent\n")
        f.write(f"  - an_nais < {AN_NAIS_MIN} (plus de 105 ans à l'accident)      "
                "    → incohérent\n")
        f.write("Valeurs manquantes ignorées (vide, « 0 », « 00 », « . ») ainsi "
                "que toute\nvaleur non numérique.\n\n")

        f.write(f"Lignes usagers testées (an_nais renseignée) : {nb_testes}\n")
        f.write(f"Nombre total d'incohérences                 : {nb}  "
                f"({taux:.3f} %)\n")
        f.write(f"  - naissance postérieure à {AN_NAIS_MAX}        : {nb_futur}\n")
        f.write(f"  - naissance antérieure à {AN_NAIS_MIN}          : {nb_ancien}"
                "\n\n")

        # Les 10 premiers cas.
        f.write("Les 10 premiers cas\n")
        f.write("-" * 68 + "\n")
        f.write(f"{'annee':<6}{'Num_Acc':<14}{'num_veh':<8}"
                f"{'an_nais':>8}   motif\n")
        f.write("-" * 68 + "\n")
        for inc in incoherences[:10]:
            f.write(f"{inc['annee']:<6}{inc['Num_Acc']:<14}"
                    f"{inc['num_veh']:<8}{inc['an_nais']:>8}   "
                    f"{inc['motif']}\n")
        f.write("\n")

        # Commentaires.
        f.write("Commentaires\n")
        f.write("-" * 68 + "\n")
        f.write(
            f"- Sur {nb_testes} lignes usagers où an_nais est renseignée, seules "
            f"{nb}\n  présentent une incohérence ({taux:.3f} %) : l'année de "
            "naissance y est\n  matériellement impossible au regard de la période "
            f"{ANNEE_DEBUT}-{ANNEE_FIN}. La\n  qualité de remplissage de an_nais "
            "est donc excellente.\n"
            "- Les bornes sont volontairement larges (1900 et 2015) : on ne "
            "retient que\n  les cas francs — la naissance dans le futur "
            "(strictement impossible) et\n  l'âge supérieur à 105 ans (extrême et "
            "quasi certainement fautif). On évite\n  ainsi de qualifier "
            "d'« incohérent » un centenaire réel.\n"
        )
        f.write(repartition)
        f.write(
            "- Les valeurs manquantes (cellule vide, « 0 ») sont écartées du "
            "test : ce\n  sont des non-réponses, pas des incohérences. Les y "
            "inclure gonflerait\n  artificiellement le compte.\n"
            "- Le rapport complet (reponse53_complet.csv) liste chaque ligne "
            "fautive avec\n  son Num_Acc et son num_veh, ce qui permet de remonter "
            "à l'usager précis et\n  de croiser au besoin avec les autres tables.\n"
        )

    print(f"Rapport écrit dans {chemin}")


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    incoherences, nb_testes = detecter_incoherences()
    ecrire_csv_complet(incoherences)
    ecrire_rapport(incoherences, nb_testes)
    print(f"\nTotal : {len(incoherences)} incohérences sur {nb_testes} "
          f"lignes testées")
    return 0


if __name__ == "__main__":
    sys.exit(main())
