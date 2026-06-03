"""Question 1.3 — Enrichissement des codes énumérés avec leur libellé.

Pour chaque fichier de data/utf8/ on produit dans data/enriched/ une copie
identique sauf que les colonnes appartenant à un domaine énuméré (lum, agg,
catv, manv, etc.) voient leur valeur remplacée par "code - libellé"
(ex. "1" → "1 - Plein jour", "07" → "07 - VL seul").

Les valeurs absentes ('', '.', '-1') et les codes non répertoriés sont
laissés à l'identique : on ne fabrique pas de libellé pour une valeur que
l'on ne sait pas interpréter — cela sera traité au cas par cas en Q4
(valeurs absentes) et Q5 (incohérences).

Cas particuliers de format (cf. docs/schema_baac.md §5) :
- catv, obs, manv sont stockés zero-paddés sur 2 chiffres ("07", "01"...).
  On normalise donc la valeur via zfill(2) avant lookup.
- senc et trajet peuvent contenir "0" (non documenté dans la doc PDF mais
  présent dans les données). On ne l'enrichit pas et on le laisse passer.

Le rapport (results/reponse13.txt) liste pour chaque fichier le nombre
de lignes et, pour chaque colonne énumérée, le nombre de cellules
enrichies / non répertoriées, plus quelques échantillons avant/après.
"""

import csv
import sys

from common import UTF8, ENRICHED, RESULTS, TYPES_FICHIERS, ANNEE_DEBUT, ANNEE_FIN


# ---------------------------------------------------------------------------
# Dictionnaires de libellés (codes BAAC 2005-2015, source : doc ONISR + spec)
# ---------------------------------------------------------------------------

# caracteristiques
LUM = {
    "1": "Plein jour",
    "2": "Crépuscule ou aube",
    "3": "Nuit sans éclairage public",
    "4": "Nuit avec éclairage public non allumé",
    "5": "Nuit avec éclairage public allumé",
}
AGG = {
    "1": "Hors agglomération",
    "2": "En agglomération",
}
INTERSECTION = {
    "1": "Hors intersection",
    "2": "Intersection en X",
    "3": "Intersection en T",
    "4": "Intersection en Y",
    "5": "Intersection à plus de 4 branches",
    "6": "Giratoire",
    "7": "Place",
    "8": "Passage à niveau",
    "9": "Autre intersection",
}
ATM = {
    "1": "Normale",
    "2": "Pluie légère",
    "3": "Pluie forte",
    "4": "Neige - grêle",
    "5": "Brouillard - fumée",
    "6": "Vent fort - tempête",
    "7": "Temps éblouissant",
    "8": "Temps couvert",
    "9": "Autre",
}
COL = {
    "1": "Deux véhicules - frontale",
    "2": "Deux véhicules - par l'arrière",
    "3": "Deux véhicules - par le côté",
    "4": "Trois véhicules et plus - en chaîne",
    "5": "Trois véhicules et plus - collisions multiples",
    "6": "Autre collision",
    "7": "Sans collision",
}

# lieux
CATR = {
    "1": "Autoroute",
    "2": "Route nationale",
    "3": "Route départementale",
    "4": "Voie communale",
    "5": "Hors réseau public",
    "6": "Parc de stationnement ouvert à la circulation publique",
    "9": "Autre",
}
CIRC = {
    "1": "À sens unique",
    "2": "Bidirectionnelle",
    "3": "À chaussées séparées",
    "4": "Avec voies d'affectation variable",
}
VOSP = {
    "0": "Sans objet",
    "1": "Piste cyclable",
    "2": "Bande cyclable",
    "3": "Voie réservée",
}
PROF = {
    "1": "Plat",
    "2": "Pente",
    "3": "Sommet de côte",
    "4": "Bas de côte",
}
PLAN = {
    "1": "Partie rectiligne",
    "2": "Courbe à gauche",
    "3": "Courbe à droite",
    "4": "En S",
}
SURF = {
    "1": "Normale",
    "2": "Mouillée",
    "3": "Flaques",
    "4": "Inondée",
    "5": "Enneigée",
    "6": "Boue",
    "7": "Verglacée",
    "8": "Corps gras - huile",
    "9": "Autre",
}
INFRA = {
    "0": "Aucun",
    "1": "Souterrain - tunnel",
    "2": "Pont - autopont",
    "3": "Bretelle d'échangeur ou de raccordement",
    "4": "Voie ferrée",
    "5": "Carrefour aménagé",
    "6": "Zone piétonne",
    "7": "Zone de péage",
}
SITU = {
    "1": "Sur chaussée",
    "2": "Sur bande d'arrêt d'urgence",
    "3": "Sur accotement",
    "4": "Sur trottoir",
    "5": "Sur piste cyclable",
}

# vehicules
SENC = {
    "1": "PK ou PR croissant",
    "2": "PK ou PR décroissant",
}
CATV = {  # zero-paddé sur 2 chiffres dans les fichiers
    "01": "Bicyclette",
    "02": "Cyclomoteur < 50 cm³",
    "03": "Voiturette",
    "04": "Référence plus utilisée (scooter immatriculé)",
    "05": "Référence plus utilisée (motocyclette)",
    "06": "Référence plus utilisée (side-car)",
    "07": "VL seul",
    "08": "VL + caravane",
    "09": "VL + remorque",
    "10": "VU seul (1,5T < PTAC ≤ 3,5T)",
    "11": "VU + caravane",
    "12": "VU + remorque",
    "13": "PL seul (3,5T < PTAC ≤ 7,5T)",
    "14": "PL seul > 7,5T",
    "15": "PL > 3,5T + remorque",
    "16": "Tracteur routier seul",
    "17": "Tracteur routier + semi-remorque",
    "18": "Référence plus utilisée (transport en commun)",
    "19": "Référence plus utilisée (tramway)",
    "20": "Engin spécial",
    "21": "Tracteur agricole",
    "30": "Scooter ≤ 50 cm³",
    "31": "Motocyclette > 50 cm³ et ≤ 125 cm³",
    "32": "Scooter > 50 cm³ et ≤ 125 cm³",
    "33": "Motocyclette > 125 cm³",
    "34": "Scooter > 125 cm³",
    "35": "Quad léger ≤ 50 cm³",
    "36": "Quad lourd > 50 cm³",
    "37": "Autobus",
    "38": "Autocar",
    "39": "Train",
    "40": "Tramway",
    "99": "Autre véhicule",
}
OBS = {  # zero-paddé sur 2 chiffres dans les fichiers
    "00": "Sans objet",
    "01": "Véhicule en stationnement",
    "02": "Arbre",
    "03": "Glissière métallique",
    "04": "Glissière béton",
    "05": "Autre glissière",
    "06": "Bâtiment, mur, pile de pont",
    "07": "Support de signalisation verticale ou poste d'appel d'urgence",
    "08": "Poteau",
    "09": "Mobilier urbain",
    "10": "Parapet",
    "11": "Îlot, refuge, borne haute",
    "12": "Bordure de trottoir",
    "13": "Fossé, talus, paroi rocheuse",
    "14": "Autre obstacle fixe sur chaussée",
    "15": "Autre obstacle fixe sur trottoir ou accotement",
    "16": "Sortie de chaussée sans obstacle",
}
OBSM = {
    "0": "Aucun",
    "1": "Piéton",
    "2": "Véhicule",
    "4": "Véhicule sur rail",
    "5": "Animal domestique",
    "6": "Animal sauvage",
    "9": "Autre",
}
CHOC = {
    "0": "Aucun",
    "1": "Avant",
    "2": "Avant droit",
    "3": "Avant gauche",
    "4": "Arrière",
    "5": "Arrière droit",
    "6": "Arrière gauche",
    "7": "Côté droit",
    "8": "Côté gauche",
    "9": "Chocs multiples (tonneaux)",
}
MANV = {  # zero-paddé sur 2 chiffres dans les fichiers
    "01": "Sans changement de direction",
    "02": "Même sens, même file",
    "03": "Entre 2 files",
    "04": "En marche arrière",
    "05": "À contresens",
    "06": "En franchissant le terre-plein central",
    "07": "Dans le couloir bus, dans le même sens",
    "08": "Dans le couloir bus, dans le sens inverse",
    "09": "En s'insérant",
    "10": "En faisant demi-tour sur la chaussée",
    "11": "Changement de file à gauche",
    "12": "Changement de file à droite",
    "13": "Déporté à gauche",
    "14": "Déporté à droite",
    "15": "Tournant à gauche",
    "16": "Tournant à droite",
    "17": "Dépassant à gauche",
    "18": "Dépassant à droite",
    "19": "Traversant la chaussée",
    "20": "Manœuvre de stationnement",
    "21": "Manœuvre d'évitement",
    "22": "Ouverture de porte",
    "23": "Arrêté (hors stationnement)",
    "24": "En stationnement (avec occupants)",
}

# usagers
CATU = {
    "1": "Conducteur",
    "2": "Passager",
    "3": "Piéton",
    "4": "Piéton en roller ou trottinette",
}
GRAV = {
    "1": "Indemne",
    "2": "Tué",
    "3": "Blessé hospitalisé",
    "4": "Blessé léger",
}
SEXE = {
    "1": "Masculin",
    "2": "Féminin",
}
TRAJET = {
    "0": "Non renseigné",
    "1": "Domicile - travail",
    "2": "Domicile - école",
    "3": "Courses - achats",
    "4": "Utilisation professionnelle",
    "5": "Promenade - loisirs",
    "9": "Autre",
}
LOCP = {
    "0": "Sans objet",
    "1": "À +50 m du passage piéton",
    "2": "À -50 m du passage piéton",
    "3": "Sur passage piéton sans signalisation lumineuse",
    "4": "Sur passage piéton avec signalisation lumineuse",
    "5": "Sur trottoir",
    "6": "Sur accotement",
    "7": "Sur refuge ou BAU",
    "8": "Sur contre-allée",
}
ACTP = {
    "0": "Non renseigné ou sans objet",
    "1": "Sens du véhicule heurtant",
    "2": "Sens inverse du véhicule heurtant",
    "3": "Traversant",
    "4": "Masqué",
    "5": "Jouant - courant",
    "6": "Avec animal",
    "9": "Autre",
}
ETATP = {
    "0": "Non renseigné",
    "1": "Seul",
    "2": "Accompagné",
    "3": "En groupe",
}


# Pour chaque type de fichier : colonne → dictionnaire de libellés.
MAPPINGS: dict[str, dict[str, dict[str, str]]] = {
    "caracteristiques": {
        "lum": LUM, "agg": AGG, "int": INTERSECTION, "atm": ATM, "col": COL,
    },
    "lieux": {
        "catr": CATR, "circ": CIRC, "vosp": VOSP, "prof": PROF,
        "plan": PLAN, "surf": SURF, "infra": INFRA, "situ": SITU,
    },
    "vehicules": {
        "senc": SENC, "catv": CATV, "obs": OBS, "obsm": OBSM,
        "choc": CHOC, "manv": MANV,
    },
    "usagers": {
        "catu": CATU, "grav": GRAV, "sexe": SEXE, "trajet": TRAJET,
        "locp": LOCP, "actp": ACTP, "etatp": ETATP,
    },
}

# Colonnes dont les codes sont stockés zero-paddés sur 2 chiffres.
# Avant lookup, on force la valeur à 2 chiffres si elle n'en a qu'un.
COLONNES_PADDEES_2 = {"catv", "obs", "manv"}

# Marqueurs courants de "valeur absente" (cf. doc BAAC §2 et schema_baac.md).
MARQUEURS_ABSENTS = {"", ".", "-1"}


def normaliser_code(colonne: str, valeur: str) -> str:
    """Renvoie la valeur sous la forme attendue par le dictionnaire.

    - Pour catv / obs / manv : zero-padding sur 2 chiffres.
    - Pour les autres colonnes : trim simple.
    """
    s = valeur.strip()
    if colonne in COLONNES_PADDEES_2 and s.isdigit() and len(s) < 2:
        return s.zfill(2)
    return s


def enrichir_fichier(source, destination, type_fichier: str) -> dict:
    """Lit `source`, écrit `destination` avec valeurs enrichies. Renvoie un récap."""
    mapping_type = MAPPINGS[type_fichier]
    nb_enrichis: dict[str, int] = {col: 0 for col in mapping_type}
    nb_inconnus: dict[str, int] = {col: 0 for col in mapping_type}
    nb_absents: dict[str, int] = {col: 0 for col in mapping_type}
    nb_lignes = 0
    echantillon: list[tuple[str, str, str]] = []  # (colonne, avant, après)

    with source.open("r", encoding="utf-8", newline="") as f_in, \
         destination.open("w", encoding="utf-8", newline="") as f_out:
        lecteur = csv.reader(f_in)
        ecrivain = csv.writer(f_out, quoting=csv.QUOTE_MINIMAL)

        entete = next(lecteur)
        ecrivain.writerow(entete)

        # On ne mappe que les colonnes effectivement présentes dans l'en-tête.
        index_par_col = {
            col: entete.index(col) for col in mapping_type if col in entete
        }

        for ligne in lecteur:
            for col, idx in index_par_col.items():
                valeur_avant = ligne[idx]
                cle = normaliser_code(col, valeur_avant)
                dico = mapping_type[col]
                if cle in dico:
                    valeur_apres = f"{cle} - {dico[cle]}"
                    ligne[idx] = valeur_apres
                    nb_enrichis[col] += 1
                    if len(echantillon) < 30 and (col, cle) not in {
                        (c, v.split(" - ")[0]) for c, _, v in echantillon
                    }:
                        echantillon.append((col, valeur_avant, valeur_apres))
                elif valeur_avant.strip() in MARQUEURS_ABSENTS:
                    nb_absents[col] += 1
                else:
                    nb_inconnus[col] += 1
            ecrivain.writerow(ligne)
            nb_lignes += 1

    return {
        "nb_lignes": nb_lignes,
        "nb_enrichis": nb_enrichis,
        "nb_inconnus": nb_inconnus,
        "nb_absents": nb_absents,
        "echantillon": echantillon,
    }


def main() -> int:
    if not UTF8.is_dir():
        print(f"Dossier source introuvable : {UTF8}", file=sys.stderr)
        return 1
    ENRICHED.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)

    rapports: list[dict] = []
    fichiers_manquants: list[str] = []

    for type_fichier in TYPES_FICHIERS:
        print(f"\n=== {type_fichier} ===")
        for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
            nom = f"{type_fichier}_{annee}.csv"
            source = UTF8 / nom
            destination = ENRICHED / nom
            if not source.exists():
                print(f"  [MANQUANT] {nom}")
                fichiers_manquants.append(nom)
                continue

            print(f"  [..]   {nom}")
            recap = enrichir_fichier(source, destination, type_fichier)
            recap["fichier"] = nom
            recap["type"] = type_fichier
            recap["annee"] = annee
            rapports.append(recap)
            total_e = sum(recap["nb_enrichis"].values())
            total_i = sum(recap["nb_inconnus"].values())
            print(
                f"  [OK]   {nom} : {recap['nb_lignes']} lignes, "
                f"{total_e} cellules enrichies, "
                f"{total_i} valeurs hors mapping"
            )

    chemin_rapport = RESULTS / "reponse13.txt"
    with chemin_rapport.open("w", encoding="utf-8") as f:
        f.write("Question 1.3 — Enrichissement des codes énumérés\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Période : {ANNEE_DEBUT}-{ANNEE_FIN} (Groupe 1)\n")
        f.write(f"Source       : {UTF8}\n")
        f.write(f"Destination  : {ENRICHED}\n\n")
        f.write(f"Nombre de fichiers enrichis : {len(rapports)}\n")
        if fichiers_manquants:
            f.write(f"Fichiers absents : {len(fichiers_manquants)} "
                    f"({', '.join(fichiers_manquants)})\n")
        f.write("\n")

        # 1. Récapitulatif par fichier (lignes + total enrichi/inconnu).
        f.write("1. Récapitulatif par fichier\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Fichier':<32} {'Lignes':>8} {'Enrichis':>10} "
                f"{'Hors map.':>10} {'Absents':>9}\n")
        for r in rapports:
            total_e = sum(r["nb_enrichis"].values())
            total_i = sum(r["nb_inconnus"].values())
            total_a = sum(r["nb_absents"].values())
            f.write(
                f"{r['fichier']:<32} {r['nb_lignes']:>8} {total_e:>10} "
                f"{total_i:>10} {total_a:>9}\n"
            )
        f.write("\n")

        # 2. Synthèse par (type, colonne) : cumul sur les 11 ans.
        f.write("2. Synthèse par colonne énumérée (cumul 2005-2015)\n")
        f.write("-" * 60 + "\n")
        for type_fichier in TYPES_FICHIERS:
            mapping_type = MAPPINGS[type_fichier]
            rapports_type = [r for r in rapports if r["type"] == type_fichier]
            if not rapports_type:
                continue
            f.write(f"\n  {type_fichier} :\n")
            f.write(f"    {'colonne':<8} {'enrichies':>12} "
                    f"{'hors map.':>12} {'absents':>10}\n")
            for col in mapping_type:
                total_e = sum(r["nb_enrichis"].get(col, 0) for r in rapports_type)
                total_i = sum(r["nb_inconnus"].get(col, 0) for r in rapports_type)
                total_a = sum(r["nb_absents"].get(col, 0) for r in rapports_type)
                f.write(f"    {col:<8} {total_e:>12} {total_i:>12} {total_a:>10}\n")
        f.write("\n")

        # 3. Échantillons avant/après pour chaque type (sur fichier 2010).
        f.write("3. Échantillons avant/après (fichier 2010)\n")
        f.write("-" * 60 + "\n")
        for type_fichier in TYPES_FICHIERS:
            r2010 = next(
                (r for r in rapports
                 if r["type"] == type_fichier and r["annee"] == 2010),
                None,
            )
            if not r2010:
                continue
            f.write(f"\n  {type_fichier}_2010.csv :\n")
            for col, avant, apres in r2010["echantillon"][:15]:
                f.write(f"    {col:<8} {avant!r:<8} → {apres}\n")
        f.write("\n")

        # 4. Vérification ciblée catv : couverture des codes rencontrés.
        f.write("4. Vérification ciblée — colonne catv (vehicules)\n")
        f.write("-" * 60 + "\n")
        codes_catv: dict[str, int] = {}
        for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
            chemin = ENRICHED / f"vehicules_{annee}.csv"
            if not chemin.exists():
                continue
            with chemin.open("r", encoding="utf-8", newline="") as fv:
                lec = csv.reader(fv)
                entete = next(lec)
                idx = entete.index("catv")
                for ligne in lec:
                    cle = ligne[idx].split(" - ", 1)[0]
                    codes_catv[cle] = codes_catv.get(cle, 0) + 1
        # Trie par fréquence décroissante.
        f.write(f"    {'code':<10} {'occurrences':>14} statut\n")
        for cle, n in sorted(codes_catv.items(), key=lambda kv: -kv[1]):
            statut = "enrichi" if cle in CATV else "non répertorié"
            f.write(f"    {cle:<10} {n:>14} {statut}\n")

    print(f"\nRapport écrit dans {chemin_rapport}")
    print(f"Total : {len(rapports)} fichier(s) enrichi(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
