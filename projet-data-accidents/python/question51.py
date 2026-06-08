"""Question 5.1 — Incohérence entre les attributs `lum` (luminosité) et `hrmn`.

On cherche les accidents pour lesquels la condition de luminosité déclarée
contredit l'heure de l'accident :

  - `lum` = « 1 - Plein jour » alors que l'heure est hors de la plage de jour ;
  - `lum` = nuit (« 3 - Nuit … », « 4 - Nuit … » ou « 5 - Nuit … ») alors que
    l'heure tombe en pleine journée.

Les bornes ne sont **pas fixes toute l'année** : le lever et le coucher du
soleil varient fortement selon la saison (en décembre il fait nuit dès 17 h, en
juin il fait encore jour à 21 h). Des bornes fixes généreraient donc de faux
positifs : un accident « plein jour » à 6 h 45 est nocturne en hiver mais en
plein jour en été. On définit donc des **plages par saison** (mois de l'accident
→ saison), volontairement prudentes (marge autour du lever/coucher réel) afin de
ne signaler que les cas francs :

  Saison          Plein jour plausible   Cœur de journée (nuit impossible)
  Hiver  (12-2)        8 h – 17 h                 10 h – 16 h
  Printemps (3-5)      7 h – 20 h                  9 h – 17 h
  Été    (6-8)         6 h – 21 h                  8 h – 18 h
  Automne (9-11)       7 h – 20 h                  9 h – 17 h

Le crépuscule/aube (« 2 - … ») est volontairement laissé de côté : par nature
il survient à des heures « intermédiaires » et ne constitue pas une incohérence
nette, qu'aucune borne fixe ne peut qualifier sans la date précise.

Format de `hrmn` (cf. inspection des données) : entier HHMM **non** zéro-paddé,
donc « 1900 » = 19 h 00 mais « 230 » = 02 h 30 et « 800 » = 08 h 00. On extrait
l'heure par division entière `int(hrmn) // 100`, ce qui est correct pour toutes
les largeurs ; `int(hrmn[:2])` serait faux sur les heures < 10 h.

Les cellules `hrmn` vides ou non numériques sont ignorées (pas d'heure → pas de
test possible). Sur les données du projet il n'y en a aucune, mais la garde
reste pour la robustesse.

Méthode : un simple parcours `csv.reader` année par année (2005-2015, Groupe 1),
sans pandas, pour rester lisible à la soutenance.

Sorties :
  - results/reponse51.txt          : nb total d'incohérences, les 10 premiers
                                     cas, commentaires.
  - results/reponse51_complet.csv  : rapport complet de toutes les incohérences
                                     (annee, Num_Acc, hrmn, heure, lum, motif).
"""

import csv
import sys

from common import ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN

# Plages horaires de référence PAR SAISON (heures pleines, bornes incluses).
#   "jour"  : plage où « plein jour » est plausible (hors plage → incohérent).
#   "coeur" : cœur de journée où il fait forcément jour (« nuit » → incohérent).
# Les marges autour du lever/coucher du soleil sont volontairement larges pour
# n'attraper que les cas francs (cf. docstring du module).
BORNES_SAISON = {
    "hiver":     {"jour": (8, 17), "coeur": (10, 16)},
    "printemps": {"jour": (7, 20), "coeur": (9, 17)},
    "été":       {"jour": (6, 21), "coeur": (8, 18)},
    "automne":   {"jour": (7, 20), "coeur": (9, 17)},
}


def saison(mois: int) -> str:
    """Renvoie la saison (« hiver », « printemps », « été », « automne »).

    Découpage trimestriel calendaire simple, suffisant pour borner le jour.
    """
    if mois in (12, 1, 2):
        return "hiver"
    if mois in (3, 4, 5):
        return "printemps"
    if mois in (6, 7, 8):
        return "été"
    return "automne"  # 9, 10, 11


def extraire_heure(hrmn: str) -> int | None:
    """Renvoie l'heure (0-23) à partir d'une valeur HHMM non zéro-paddée.

    Renvoie None si la cellule est vide ou non numérique.
    """
    v = hrmn.strip()
    if not v.isdigit():
        return None
    return int(v) // 100


def motif_incoherence(lum: str, heure: int, mois: int) -> str | None:
    """Renvoie le motif d'incohérence entre `lum` et l'heure, ou None.

    `lum` est la valeur enrichie (« code - libellé »). Les bornes appliquées
    dépendent de la saison déduite de `mois`.
    """
    bornes = BORNES_SAISON[saison(mois)]
    jour_debut, jour_fin = bornes["jour"]
    coeur_debut, coeur_fin = bornes["coeur"]
    # Cas 1 : plein jour déclaré mais heure nocturne.
    if "1 - Plein jour" in lum and not (jour_debut <= heure <= jour_fin):
        return "Plein jour déclaré mais heure nocturne"
    # Cas 2 : nuit déclarée mais heure en pleine journée.
    nuit = ("3 - Nuit" in lum) or ("4 - Nuit" in lum) or ("5 - Nuit" in lum)
    if nuit and (coeur_debut <= heure <= coeur_fin):
        return "Nuit déclarée mais heure en pleine journée"
    return None


def detecter_incoherences() -> tuple[list[dict], int]:
    """Parcourt 2005-2015 et renvoie (incoherences, nb_accidents_testés).

    Chaque incohérence est un dict : annee, Num_Acc, hrmn, heure, saison, lum,
    motif.
    """
    incoherences: list[dict] = []
    nb_testes = 0

    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        chemin = ENRICHED / f"caracteristiques_{annee}.csv"
        print(f"[..]   {annee}")
        with chemin.open("r", encoding="utf-8", newline="") as f:
            lecteur = csv.reader(f)
            entete = next(lecteur)
            idx_acc = entete.index("Num_Acc")
            idx_mois = entete.index("mois")
            idx_hrmn = entete.index("hrmn")
            idx_lum = entete.index("lum")
            for ligne in lecteur:
                heure = extraire_heure(ligne[idx_hrmn])
                if heure is None:
                    continue  # heure manquante → non testable
                mois_txt = ligne[idx_mois].strip()
                if not mois_txt.isdigit():
                    continue  # mois manquant → saison inconnue, non testable
                mois = int(mois_txt)
                nb_testes += 1
                lum = ligne[idx_lum]
                motif = motif_incoherence(lum, heure, mois)
                if motif is not None:
                    incoherences.append({
                        "annee": annee,
                        "Num_Acc": ligne[idx_acc],
                        "hrmn": ligne[idx_hrmn].strip(),
                        "heure": heure,
                        "saison": saison(mois),
                        "lum": lum,
                        "motif": motif,
                    })
        print(f"  [OK] {annee} : {len(incoherences)} incohérences cumulées")

    return incoherences, nb_testes


def ecrire_csv_complet(incoherences: list[dict]) -> None:
    """Écrit results/reponse51_complet.csv : toutes les incohérences."""
    chemin = RESULTS / "reponse51_complet.csv"
    colonnes = ["annee", "Num_Acc", "hrmn", "heure", "saison", "lum", "motif"]
    with chemin.open("w", encoding="utf-8", newline="") as f:
        ecrivain = csv.DictWriter(f, fieldnames=colonnes)
        ecrivain.writeheader()
        for inc in incoherences:
            ecrivain.writerow(inc)
    print(f"Rapport complet écrit dans {chemin}")


def ecrire_rapport(incoherences: list[dict], nb_testes: int) -> None:
    """Écrit results/reponse51.txt : total, 10 premiers cas, commentaires."""
    chemin = RESULTS / "reponse51.txt"
    nb = len(incoherences)
    taux = nb / nb_testes * 100 if nb_testes else 0.0

    # Répartition par motif, pour le commentaire.
    nb_jour = sum(1 for i in incoherences
                  if i["motif"].startswith("Plein jour"))
    nb_nuit = nb - nb_jour

    with chemin.open("w", encoding="utf-8") as f:
        f.write("Question 5.1 — Incohérence entre lum (luminosité) et hrmn\n")
        f.write("=" * 68 + "\n\n")
        f.write(f"Période : {ANNEE_DEBUT}-{ANNEE_FIN} (Groupe 1)\n")
        f.write(f"Source  : {ENRICHED}\n\n")
        f.write("Règle d'incohérence appliquée (bornes par saison) :\n")
        f.write("  - « 1 - Plein jour » mais heure hors de la plage de jour "
                "→ incohérent\n")
        f.write("  - « 3/4/5 - Nuit … » mais heure dans le cœur de journée "
                "→ incohérent\n")
        f.write("  (« 2 - Crépuscule ou aube » non testé : heures "
                "intermédiaires par nature.)\n\n")
        f.write("  Saison          Plein jour plausible   Cœur de journée\n")
        for nom in ("hiver", "printemps", "été", "automne"):
            jd, jf = BORNES_SAISON[nom]["jour"]
            cd, cf = BORNES_SAISON[nom]["coeur"]
            f.write(f"  {nom:<14}  {jd:>2} h – {jf:>2} h              "
                    f"{cd:>2} h – {cf:>2} h\n")
        f.write("\nHeure extraite par int(hrmn)//100 (HHMM non zéro-paddé).\n\n")

        f.write(f"Accidents testés (hrmn renseignée) : {nb_testes}\n")
        f.write(f"Nombre total d'incohérences        : {nb}  "
                f"({taux:.3f} %)\n")
        f.write(f"  - plein jour déclaré la nuit      : {nb_jour}\n")
        f.write(f"  - nuit déclarée en pleine journée : {nb_nuit}\n\n")

        # Les 10 premiers cas.
        f.write("Les 10 premiers cas\n")
        f.write("-" * 68 + "\n")
        f.write(f"{'annee':<6}{'Num_Acc':<14}{'hrmn':>6}{'h':>4}  "
                f"{'saison':<10}lum / motif\n")
        f.write("-" * 68 + "\n")
        for inc in incoherences[:10]:
            f.write(f"{inc['annee']:<6}{inc['Num_Acc']:<14}"
                    f"{inc['hrmn']:>6}{inc['heure']:>4}  "
                    f"{inc['saison']:<10}{inc['lum']}\n")
            f.write(f"{'':>30}→ {inc['motif']}\n")
        f.write("\n")

        # Commentaires.
        f.write("Commentaires\n")
        f.write("-" * 68 + "\n")
        f.write(
            f"- Sur {nb_testes} accidents datés, seuls {nb} présentent une "
            f"incohérence\n  franche entre la luminosité déclarée et l'heure, "
            f"soit {taux:.3f} %. La\n  cohérence lum × hrmn est donc globalement "
            "très bonne : les forces de\n  l'ordre renseignent ces deux champs "
            "de façon concordante.\n"
            "- Les bornes varient selon la saison (plages ci-dessus) afin "
            "d'éviter les\n  faux positifs liés au lever/coucher du soleil : "
            "un accident « plein jour »\n  à 6 h 45 est nocturne en hiver mais "
            "en plein jour en été, et n'est donc\n  signalé qu'en hiver. Chaque "
            "plage garde en outre une marge autour des\n  heures réelles de "
            "lever/coucher, pour ne retenir que les cas francs.\n"
            "- Le crépuscule/aube (« 2 - … ») est exclu du test : c'est par "
            "construction\n  une luminosité d'heure intermédiaire, qu'aucune "
            "borne fixe ne peut\n  qualifier d'incohérente sans connaître la "
            "date précise.\n"
            "- Interprétation des cas restants : ils relèvent soit d'une "
            "erreur de\n  saisie (luminosité ou heure mal reportée), soit d'une "
            "situation réelle\n  mais rare (p. ex. tunnel, brouillard très "
            "dense, éclipse) — non\n  distinguables à partir des seuls champs "
            "lum et hrmn. Le rapport complet\n  (reponse51_complet.csv) permet "
            "de les inspecter un par un.\n"
        )

    print(f"Rapport écrit dans {chemin}")


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    incoherences, nb_testes = detecter_incoherences()
    ecrire_csv_complet(incoherences)
    ecrire_rapport(incoherences, nb_testes)
    print(f"\nTotal : {len(incoherences)} incohérences sur {nb_testes} "
          f"accidents testés")
    return 0


if __name__ == "__main__":
    sys.exit(main())
