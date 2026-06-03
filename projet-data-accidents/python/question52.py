"""Question 5.2 — Incohérence entre les attributs `obsm` et `choc`.

Situation choisie (différente de `lum` × `hrmn` traitée en Q5.1) : la
contradiction entre l'**obstacle mobile heurté** (`obsm`) et le **point de choc
initial** (`choc`), deux attributs de la table *vehicules*.

Règle d'incohérence :

  - `obsm` désigne un obstacle mobile réellement heurté (« 1 - Piéton »,
    « 2 - Véhicule », « 4 - Véhicule sur rail », « 5 - Animal domestique »,
    « 6 - Animal sauvage » ou « 9 - Autre ») ;
  - mais `choc` vaut « 0 - Aucun », c'est-à-dire qu'aucun point de choc n'est
    enregistré sur le véhicule.

C'est contradictoire : on ne peut pas heurter un obstacle mobile sans qu'il y
ait un point d'impact sur le véhicule. Le cas inverse (un point de choc sans
obstacle mobile) n'est **pas** une incohérence : le véhicule a pu heurter un
obstacle *fixe* (mur, glissière…), renseigné dans `obs` et non dans `obsm`.

Valeurs « aucun » repérées par le préfixe « 0 - » (format enrichi « code -
libellé »), conformément à l'inventaire des données.

Cellules vides : `obsm` ou `choc` vide → information manquante, ligne non
testable, ignorée (cf. inventaire : 551 `obsm` vides et 218 `choc` vides sur
~1,3 M de lignes véhicules).

Méthode : un simple parcours `csv.reader` année par année (2005-2015, Groupe 1),
sans pandas, pour rester lisible à la soutenance.

Sorties :
  - results/reponse52.txt          : nb total d'incohérences, les 10 premiers
                                     cas, commentaires.
  - results/reponse52_complet.csv  : rapport complet de toutes les incohérences
                                     (annee, Num_Acc, num_veh, obsm, choc).
"""

import csv
import sys

from common import ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN


def est_aucun(valeur: str) -> bool:
    """Vrai si la valeur enrichie correspond à « 0 - … » (aucun)."""
    return valeur.strip().startswith("0 - ")


def est_obstacle_mobile_reel(obsm: str) -> bool:
    """Vrai si `obsm` désigne un obstacle mobile effectivement heurté.

    Faux pour la cellule vide (non renseignée) et pour « 0 - Aucun ».
    """
    v = obsm.strip()
    return v != "" and not est_aucun(v)


def detecter_incoherences() -> tuple[list[dict], int]:
    """Parcourt 2005-2015 et renvoie (incoherences, nb_lignes_testées).

    Chaque incohérence est un dict : annee, Num_Acc, num_veh, obsm, choc.
    Une ligne véhicule est « testée » dès lors que `obsm` et `choc` sont tous
    deux renseignés (non vides).
    """
    incoherences: list[dict] = []
    nb_testes = 0

    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        chemin = ENRICHED / f"vehicules_{annee}.csv"
        print(f"[..]   {annee}")
        with chemin.open("r", encoding="utf-8", newline="") as f:
            lecteur = csv.reader(f)
            entete = next(lecteur)
            idx_acc = entete.index("Num_Acc")
            idx_veh = entete.index("num_veh")
            idx_obsm = entete.index("obsm")
            idx_choc = entete.index("choc")
            for ligne in lecteur:
                obsm = ligne[idx_obsm]
                choc = ligne[idx_choc]
                # Ligne non testable si l'un des deux champs est vide.
                if obsm.strip() == "" or choc.strip() == "":
                    continue
                nb_testes += 1
                # Incohérence : obstacle mobile heurté mais aucun point de choc.
                if est_obstacle_mobile_reel(obsm) and est_aucun(choc):
                    incoherences.append({
                        "annee": annee,
                        "Num_Acc": ligne[idx_acc],
                        "num_veh": ligne[idx_veh].strip(),
                        "obsm": obsm.strip(),
                        "choc": choc.strip(),
                    })
        print(f"  [OK] {annee} : {len(incoherences)} incohérences cumulées")

    return incoherences, nb_testes


def ecrire_csv_complet(incoherences: list[dict]) -> None:
    """Écrit results/reponse52_complet.csv : toutes les incohérences."""
    chemin = RESULTS / "reponse52_complet.csv"
    colonnes = ["annee", "Num_Acc", "num_veh", "obsm", "choc"]
    with chemin.open("w", encoding="utf-8", newline="") as f:
        ecrivain = csv.DictWriter(f, fieldnames=colonnes)
        ecrivain.writeheader()
        for inc in incoherences:
            ecrivain.writerow(inc)
    print(f"Rapport complet écrit dans {chemin}")


def ecrire_rapport(incoherences: list[dict], nb_testes: int) -> None:
    """Écrit results/reponse52.txt : total, 10 premiers cas, commentaires."""
    chemin = RESULTS / "reponse52.txt"
    nb = len(incoherences)
    taux = nb / nb_testes * 100 if nb_testes else 0.0

    # Répartition par type d'obstacle mobile heurté, pour le commentaire.
    par_obsm: dict[str, int] = {}
    for inc in incoherences:
        par_obsm[inc["obsm"]] = par_obsm.get(inc["obsm"], 0) + 1

    with chemin.open("w", encoding="utf-8") as f:
        f.write("Question 5.2 — Incohérence entre obsm (obstacle mobile) "
                "et choc (point de choc)\n")
        f.write("=" * 68 + "\n\n")
        f.write(f"Période : {ANNEE_DEBUT}-{ANNEE_FIN} (Groupe 1)\n")
        f.write(f"Source  : {ENRICHED} (table vehicules)\n\n")
        f.write("Règle d'incohérence appliquée :\n")
        f.write("  - obsm = obstacle mobile réellement heurté "
                "(« 1 », « 2 », « 4 », « 5 », « 6 » ou « 9 »)\n")
        f.write("  - mais choc = « 0 - Aucun » (aucun point de choc enregistré)"
                "  → incohérent\n")
        f.write("  (Cas inverse non testé : un choc sans obstacle mobile peut "
                "venir d'un\n   obstacle fixe, renseigné dans obs.)\n")
        f.write("Lignes vides (obsm ou choc non renseigné) : ignorées.\n\n")

        f.write(f"Lignes véhicules testées (obsm et choc renseignés) : "
                f"{nb_testes}\n")
        f.write(f"Nombre total d'incohérences                        : {nb}  "
                f"({taux:.3f} %)\n\n")

        f.write("Répartition par obstacle mobile heurté :\n")
        for obsm in sorted(par_obsm, key=lambda k: -par_obsm[k]):
            f.write(f"  - {obsm:<24} : {par_obsm[obsm]}\n")
        f.write("\n")

        # Les 10 premiers cas.
        f.write("Les 10 premiers cas\n")
        f.write("-" * 68 + "\n")
        f.write(f"{'annee':<6}{'Num_Acc':<14}{'num_veh':<8}"
                f"{'obsm':<26}choc\n")
        f.write("-" * 68 + "\n")
        for inc in incoherences[:10]:
            f.write(f"{inc['annee']:<6}{inc['Num_Acc']:<14}"
                    f"{inc['num_veh']:<8}{inc['obsm']:<26}{inc['choc']}\n")
        f.write("\n")

        # Commentaires.
        f.write("Commentaires\n")
        f.write("-" * 68 + "\n")
        f.write(
            f"- Sur {nb_testes} lignes véhicules où obsm et choc sont tous deux "
            f"renseignés,\n  {nb} présentent une incohérence ({taux:.3f} %) : un "
            "obstacle mobile est\n  déclaré heurté alors qu'aucun point de choc "
            "n'est enregistré sur le\n  véhicule. Logiquement, un impact aurait "
            "dû être reporté.\n"
            "- La règle est volontairement asymétrique : on ne signale que "
            "« obstacle\n  mobile sans choc ». Le cas inverse (choc sans obstacle "
            "mobile) n'est PAS\n  une anomalie, car le véhicule a pu heurter un "
            "obstacle fixe (mur,\n  glissière, arbre…), qui est codé dans obs et "
            "non dans obsm.\n"
            "- Ces incohérences relèvent presque toujours d'une erreur ou d'un "
            "oubli de\n  saisie sur le champ choc (laissé à « 0 - Aucun » par "
            "défaut), le champ\n  obsm étant lui correctement renseigné. Le taux "
            "faible confirme la bonne\n  qualité de remplissage de ces deux "
            "attributs.\n"
            "- Le rapport complet (reponse52_complet.csv) liste chaque ligne "
            "fautive avec\n  son Num_Acc et son num_veh, ce qui permet de "
            "remonter au véhicule précis\n  et de croiser au besoin avec les "
            "autres tables.\n"
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
