"""Question 1.1 — Conversion des fichiers BAAC en UTF-8 avec séparateur ','.

Pour chaque fichier de data/raw/ correspondant aux 4 types et aux années
ANNEE_DEBUT..ANNEE_FIN, on :
  1. détecte l'encodage source (chardet sur un échantillon, fallback latin-1) ;
  2. détecte le séparateur du fichier (',', ';' ou '\\t') sur la ligne d'en-tête ;
  3. relit le fichier ligne par ligne avec csv.reader (gère les guillemets) ;
  4. réécrit le fichier dans data/utf8/ en UTF-8, séparateur ','.

Le résumé par fichier (encodage détecté, séparateur, nb lignes) est écrit
dans results/reponse11.txt.
"""

import csv
import sys
from pathlib import Path

import chardet

from common import RAW, UTF8, RESULTS, TYPES_FICHIERS, ANNEE_DEBUT, ANNEE_FIN


def detecter_encodage(chemin: Path, taille_echantillon: int = 200_000) -> str:
    """Lit un échantillon du fichier et renvoie l'encodage détecté.

    On normalise quelques cas courants : 'ascii' est traité comme 'utf-8'
    (sur-ensemble) et les variantes 'iso-8859-1' / 'windows-1252' sont
    décodables sans erreur en latin-1.
    """
    with chemin.open("rb") as f:
        echantillon = f.read(taille_echantillon)
    detection = chardet.detect(echantillon)
    encodage = (detection.get("encoding") or "latin-1").lower()
    if encodage == "ascii":
        return "utf-8"
    # cp1252 et latin-1 sont tous deux décodables ; on garde tel quel.
    return encodage


def detecter_separateur(chemin: Path, encodage: str) -> str:
    """Devine le séparateur en comptant les occurrences sur l'en-tête."""
    with chemin.open("r", encoding=encodage, errors="replace", newline="") as f:
        ligne = f.readline()
    candidats = {",": ligne.count(","), ";": ligne.count(";"), "\t": ligne.count("\t")}
    # On choisit le séparateur le plus fréquent, ',' en cas d'égalité.
    sep, nb = max(candidats.items(), key=lambda kv: (kv[1], kv[0] == ","))
    if nb == 0:
        # Aucun séparateur reconnu : on retombe sur la virgule.
        return ","
    return sep


def convertir_fichier(source: Path, destination: Path) -> dict:
    """Convertit un fichier vers UTF-8 + ','. Renvoie un petit récap."""
    encodage = detecter_encodage(source)
    separateur = detecter_separateur(source, encodage)

    nb_lignes = 0
    with source.open("r", encoding=encodage, newline="", errors="replace") as f_in, \
         destination.open("w", encoding="utf-8", newline="") as f_out:
        lecteur = csv.reader(f_in, delimiter=separateur)
        ecrivain = csv.writer(f_out, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        for ligne in lecteur:
            ecrivain.writerow(ligne)
            nb_lignes += 1

    return {
        "source": source.name,
        "encodage_source": encodage,
        "separateur_source": "TAB" if separateur == "\t" else separateur,
        "nb_lignes": nb_lignes,
        "destination": destination.name,
    }


def main() -> int:
    if not RAW.is_dir():
        print(f"Dossier source introuvable : {RAW}", file=sys.stderr)
        return 1
    UTF8.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)

    rapports = []
    fichiers_manquants = []

    for type_fichier in TYPES_FICHIERS:
        for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
            nom = f"{type_fichier}_{annee}.csv"
            source = RAW / nom
            destination = UTF8 / nom
            if not source.exists():
                print(f"  [SKIP] {nom} absent de data/raw/")
                fichiers_manquants.append(nom)
                continue
            print(f"  [..]   {nom}")
            rapport = convertir_fichier(source, destination)
            print(
                f"  [OK]   {nom} : {rapport['encodage_source']} → utf-8, "
                f"sep '{rapport['separateur_source']}' → ',', "
                f"{rapport['nb_lignes']} lignes"
            )
            rapports.append(rapport)

    # Écriture du résumé.
    chemin_rapport = RESULTS / "reponse11.txt"
    with chemin_rapport.open("w", encoding="utf-8") as f:
        f.write("Question 1.1 — Conversion UTF-8 + séparateur ','\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Période traitée : {ANNEE_DEBUT}-{ANNEE_FIN} (Groupe 1)\n")
        f.write(f"Types de fichiers : {', '.join(TYPES_FICHIERS)}\n")
        f.write(f"Source : {RAW}\nDestination : {UTF8}\n\n")
        f.write(f"Nombre de fichiers convertis : {len(rapports)}\n")
        if fichiers_manquants:
            f.write(f"Fichiers absents : {len(fichiers_manquants)} "
                    f"({', '.join(fichiers_manquants)})\n")
        f.write("\n")
        f.write(f"{'Fichier':<35} {'Encodage':<14} {'Sep.':<6} {'Lignes':>10}\n")
        f.write("-" * 70 + "\n")
        for r in rapports:
            f.write(
                f"{r['source']:<35} {r['encodage_source']:<14} "
                f"{r['separateur_source']:<6} {r['nb_lignes']:>10}\n"
            )
        f.write("\n")
        # Synthèse par encodage rencontré.
        encodages = {}
        for r in rapports:
            encodages[r["encodage_source"]] = encodages.get(r["encodage_source"], 0) + 1
        f.write("Synthèse des encodages détectés :\n")
        for enc, n in sorted(encodages.items()):
            f.write(f"  - {enc} : {n} fichier(s)\n")
        seps = {}
        for r in rapports:
            seps[r["separateur_source"]] = seps.get(r["separateur_source"], 0) + 1
        f.write("\nSynthèse des séparateurs source :\n")
        for s, n in sorted(seps.items()):
            f.write(f"  - '{s}' : {n} fichier(s)\n")

    print(f"\nRapport écrit dans {chemin_rapport}")
    print(f"Total : {len(rapports)} fichier(s) converti(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
