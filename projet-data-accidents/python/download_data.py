"""Télécharge les fichiers BAAC pour la période du groupe dans data/raw/.

Utilise l'API data.gouv.fr pour lister les ressources du dataset
"base-de-donnees-accidents-corporels-de-la-circulation", filtre par année
et par type (caracteristiques, lieux, vehicules, usagers), exclut les
fichiers 'vehicules-immatricules-baac...' (piège du sujet), puis télécharge.

Usage : python Python/download_data.py
"""
from __future__ import annotations

import sys
import unicodedata
import urllib.request
from pathlib import Path

# Le script doit être exécutable depuis n'importe quel cwd (ex: depuis la racine
# du repo, ou par double-clic). On ajoute Python/ au sys.path pour pouvoir
# importer common.py de manière fiable.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ANNEE_DEBUT, ANNEE_FIN, RAW, TYPES_FICHIERS  # noqa: E402


def _norm(s: str) -> str:
    """Lowercase + sans accents, pour matcher 'caractéristiques' == 'caracteristiques'."""
    return "".join(
        c for c in unicodedata.normalize("NFD", s.lower())
        if unicodedata.category(c) != "Mn"
    )

DATASET = "base-de-donnees-accidents-corporels-de-la-circulation"
API_URL = f"https://www.data.gouv.fr/api/1/datasets/{DATASET}/"


def fetch_resources() -> list[dict]:
    import json
    with urllib.request.urlopen(API_URL) as r:
        return json.load(r)["resources"]


def is_target(title: str, url: str, years: set[str]) -> bool:
    # On combine titre + nom de fichier de l'URL pour être robuste
    hay = _norm(title + " " + url.rsplit("/", 1)[-1])
    if "immatricul" in hay:
        return False
    if not any(k in hay for k in TYPES_FICHIERS):
        return False
    return any(y in hay for y in years)


def is_doc(title: str, url: str) -> bool:
    hay = _norm(title + " " + url)
    return "description" in hay and ".pdf" in hay


def download(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        print(f"  skip (déjà présent) {dest.name}")
        return
    print(f"  → {dest.name}")
    urllib.request.urlretrieve(url, dest)


def main() -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    years = {str(y) for y in range(ANNEE_DEBUT, ANNEE_FIN + 1)}
    print(f"Période : {ANNEE_DEBUT}–{ANNEE_FIN} ({len(years)} années)")

    resources = fetch_resources()
    targets = []
    for r in resources:
        title = r.get("title") or ""
        url = r.get("url")
        if not url:
            continue
        if is_target(title, url, years) or is_doc(title, url):
            targets.append((title, url))

    if not targets:
        print("Aucune ressource trouvée — vérifiez l'API.", file=sys.stderr)
        return 1

    print(f"{len(targets)} fichiers à récupérer dans {RAW}")
    for title, url in targets:
        name = url.rsplit("/", 1)[-1].split("?")[0]
        download(url, RAW / name)

    print("Terminé.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
