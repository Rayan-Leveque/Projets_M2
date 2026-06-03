"""Question 5.1 — Incohérence entre les attributs `lum` (luminosité) et `hrmn`.

On cherche les accidents pour lesquels la condition de luminosité déclarée
contredit l'heure de l'accident :

  - `lum` = « 1 - Plein jour » alors que l'heure est hors de la plage de jour
    [8 h ; 19 h] (donc avant 8 h ou à partir de 20 h) ;
  - `lum` = nuit (« 3 - Nuit … », « 4 - Nuit … » ou « 5 - Nuit … ») alors que
    l'heure tombe en pleine journée [10 h ; 16 h].

Le crépuscule/aube (« 2 - … ») est volontairement laissé de côté : par nature
il survient à des heures « intermédiaires » et ne constitue pas une incohérence
nette. Les bornes sont donc choisies prudemment (on ne signale que les cas
francs) pour éviter les faux positifs autour du lever/coucher du soleil, qui
varient selon la saison.

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

# Plages horaires de référence (heures pleines, bornes incluses).
JOUR_DEBUT, JOUR_FIN = 8, 19    # « plein jour » attendu entre 8 h et 19 h
PLEIN_JOUR_DEBUT, PLEIN_JOUR_FIN = 10, 16  # cœur de journée, où « nuit » détonne


def extraire_heure(hrmn: str) -> int | None:
    """Renvoie l'heure (0-23) à partir d'une valeur HHMM non zéro-paddée.

    Renvoie None si la cellule est vide ou non numérique.
    """
    v = hrmn.strip()
    if not v.isdigit():
        return None
    return int(v) // 100


def motif_incoherence(lum: str, heure: int) -> str | None:
    """Renvoie le motif d'incohérence entre `lum` et l'heure, ou None.

    `lum` est la valeur enrichie (« code - libellé »).
    """
    # Cas 1 : plein jour déclaré mais heure nocturne.
    if "1 - Plein jour" in lum and not (JOUR_DEBUT <= heure <= JOUR_FIN):
        return "Plein jour déclaré mais heure nocturne"
    # Cas 2 : nuit déclarée mais heure en pleine journée.
    nuit = ("3 - Nuit" in lum) or ("4 - Nuit" in lum) or ("5 - Nuit" in lum)
    if nuit and (PLEIN_JOUR_DEBUT <= heure <= PLEIN_JOUR_FIN):
        return "Nuit déclarée mais heure en pleine journée"
    return None


def detecter_incoherences() -> tuple[list[dict], int]:
    """Parcourt 2005-2015 et renvoie (incoherences, nb_accidents_testés).

    Chaque incohérence est un dict : annee, Num_Acc, hrmn, heure, lum, motif.
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
            idx_hrmn = entete.index("hrmn")
            idx_lum = entete.index("lum")
            for ligne in lecteur:
                heure = extraire_heure(ligne[idx_hrmn])
                if heure is None:
                    continue  # heure manquante → non testable
                nb_testes += 1
                lum = ligne[idx_lum]
                motif = motif_incoherence(lum, heure)
                if motif is not None:
                    incoherences.append({
                        "annee": annee,
                        "Num_Acc": ligne[idx_acc],
                        "hrmn": ligne[idx_hrmn].strip(),
                        "heure": heure,
                        "lum": lum,
                        "motif": motif,
                    })
        print(f"  [OK] {annee} : {len(incoherences)} incohérences cumulées")

    return incoherences, nb_testes


def ecrire_csv_complet(incoherences: list[dict]) -> None:
    """Écrit results/reponse51_complet.csv : toutes les incohérences."""
    chemin = RESULTS / "reponse51_complet.csv"
    colonnes = ["annee", "Num_Acc", "hrmn", "heure", "lum", "motif"]
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
        f.write("Règle d'incohérence appliquée :\n")
        f.write(f"  - « 1 - Plein jour » mais heure hors de "
                f"[{JOUR_DEBUT} h ; {JOUR_FIN} h]  → incohérent\n")
        f.write(f"  - « 3/4/5 - Nuit … » mais heure dans "
                f"[{PLEIN_JOUR_DEBUT} h ; {PLEIN_JOUR_FIN} h]  → incohérent\n")
        f.write("  (« 2 - Crépuscule ou aube » non testé : heures "
                "intermédiaires par nature.)\n")
        f.write("Heure extraite par int(hrmn)//100 (HHMM non zéro-paddé).\n\n")

        f.write(f"Accidents testés (hrmn renseignée) : {nb_testes}\n")
        f.write(f"Nombre total d'incohérences        : {nb}  "
                f"({taux:.3f} %)\n")
        f.write(f"  - plein jour déclaré la nuit      : {nb_jour}\n")
        f.write(f"  - nuit déclarée en pleine journée : {nb_nuit}\n\n")

        # Les 10 premiers cas.
        f.write("Les 10 premiers cas\n")
        f.write("-" * 68 + "\n")
        f.write(f"{'annee':<6}{'Num_Acc':<14}{'hrmn':>6}{'h':>4}   "
                f"lum / motif\n")
        f.write("-" * 68 + "\n")
        for inc in incoherences[:10]:
            f.write(f"{inc['annee']:<6}{inc['Num_Acc']:<14}"
                    f"{inc['hrmn']:>6}{inc['heure']:>4}   "
                    f"{inc['lum']}\n")
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
            "- Les bornes sont volontairement prudentes : la plage de jour "
            f"retenue\n  [{JOUR_DEBUT} h ; {JOUR_FIN} h] et le cœur de journée "
            f"[{PLEIN_JOUR_DEBUT} h ; {PLEIN_JOUR_FIN} h] laissent une marge "
            "autour\n  du lever et du coucher du soleil, qui varient fortement "
            "selon la saison\n  (en décembre il fait nuit dès 17 h, en juin "
            "encore jour à 21 h). On ne\n  signale ainsi que les cas nets et on "
            "évite les faux positifs saisonniers.\n"
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
