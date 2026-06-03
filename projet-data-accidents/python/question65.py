"""Question 6.5 (facultative) — Carte animée des accidents par département, année par année.

On reprend le principe de la question 6.3 (nombre d'accidents par département de
métropole, cercles proportionnels), mais au lieu d'une seule carte cumulée on
produit **une carte par année** de ANNEE_DEBUT à ANNEE_FIN, puis on assemble les
images en un **GIF animé** (results/reponse65.gif).

Choix techniques :
  - cartes tracées avec matplotlib (et non folium) car il faut des images PNG
    fixes que Pillow saura empiler dans un GIF ;
  - les positions des cercles viennent de CENTROIDES_DEPARTEMENTS (lat, lon) ;
  - l'aire de chaque cercle est proportionnelle au nombre d'accidents de l'année,
    normalisée par le **maximum tous départements / toutes années confondus** :
    ainsi les tailles sont comparables d'une image à l'autre et l'animation
    montre bien l'évolution dans le temps ;
  - les bornes des axes (cadre France) sont fixes sur toutes les images pour que
    les frames se superposent sans « sauter ».

Les PNG sont écrits dans results/ puis supprimés une fois le GIF construit.
"""

import csv
import sys
from collections import Counter

import matplotlib
matplotlib.use("Agg")  # backend sans fenêtre, on ne fait qu'enregistrer des fichiers
import matplotlib.pyplot as plt
from PIL import Image

from common import (
    ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN,
    normaliser_dep, CENTROIDES_DEPARTEMENTS,
)


# Cadre géographique de la France métropolitaine (en degrés), identique pour
# toutes les images afin que l'animation reste stable.
LON_MIN, LON_MAX = -5.5, 10.0
LAT_MIN, LAT_MAX = 41.0, 51.5

# Aire maximale d'un cercle (en points^2) pour le département le plus accidenté.
AIRE_MAX = 2500


def compter_accidents_par_departement(annee: int) -> Counter:
    """Compte les accidents par département de métropole pour une année donnée."""
    compteur: Counter = Counter()
    chemin = ENRICHED / f"caracteristiques_{annee}.csv"
    if not chemin.exists():
        print(f"  [MANQUANT] {chemin.name}")
        return compteur
    with chemin.open("r", encoding="utf-8", newline="") as f:
        lecteur = csv.reader(f)
        entete = next(lecteur)
        idx_dep = entete.index("dep")
        for ligne in lecteur:
            dep = normaliser_dep(ligne[idx_dep])
            if dep is not None:
                compteur[dep] += 1
    return compteur


def tracer_carte_annee(annee: int, compteur: Counter, nb_max: int, chemin_png) -> None:
    """Trace la carte d'une année et l'enregistre en PNG.

    L'aire de chaque cercle est proportionnelle au nombre d'accidents du
    département, rapportée à `nb_max` (maximum global) pour que l'échelle soit
    la même sur toutes les images.
    """
    lons, lats, aires = [], [], []
    for dep, nb in compteur.items():
        if dep not in CENTROIDES_DEPARTEMENTS:
            continue
        lat, lon = CENTROIDES_DEPARTEMENTS[dep]
        lons.append(lon)
        lats.append(lat)
        aires.append(AIRE_MAX * (nb / nb_max))

    fig, ax = plt.subplots(figsize=(6, 6), dpi=100)
    ax.scatter(
        lons, lats, s=aires,
        color="#e34a33", edgecolors="#b30000", linewidths=0.6, alpha=0.6,
    )
    ax.set_xlim(LON_MIN, LON_MAX)
    ax.set_ylim(LAT_MIN, LAT_MAX)
    ax.set_aspect("equal")  # repère lon/lat « carré » pour ne pas déformer la France
    ax.set_xticks([])
    ax.set_yticks([])
    total = sum(compteur.values())
    ax.set_title(f"Accidents par département — {annee}\n({total} accidents en métropole)")

    fig.tight_layout()
    fig.savefig(chemin_png)
    plt.close(fig)


def main() -> int:
    if not ENRICHED.is_dir():
        print(f"Dossier source introuvable : {ENRICHED}", file=sys.stderr)
        return 1
    RESULTS.mkdir(parents=True, exist_ok=True)

    # 1) Comptage de toutes les années (gardé en mémoire) pour connaître le
    #    maximum global avant de tracer quoi que ce soit.
    print(f"Comptage des accidents par département, année par année "
          f"({ANNEE_DEBUT}-{ANNEE_FIN}) :")
    comptages: dict[int, Counter] = {}
    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        compteur = compter_accidents_par_departement(annee)
        comptages[annee] = compteur
        print(f"  {annee} : {sum(compteur.values())} accidents en métropole")

    nb_max = max(
        (nb for compteur in comptages.values() for nb in compteur.values()),
        default=0,
    )
    if nb_max == 0:
        print("Aucun accident compté, GIF non généré.", file=sys.stderr)
        return 1
    print(f"\nMaximum global (1 département, 1 année) : {nb_max} accidents "
          f"→ aire de cercle de référence.")

    # 2) Une image PNG par année.
    chemins_png = []
    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        chemin_png = RESULTS / f"_carte_{annee}.png"
        tracer_carte_annee(annee, comptages[annee], nb_max, chemin_png)
        chemins_png.append(chemin_png)
        print(f"  image générée : {chemin_png.name}")

    # 3) Assemblage des PNG en GIF animé avec Pillow.
    images = [Image.open(c) for c in chemins_png]
    chemin_gif = RESULTS / "reponse65.gif"
    images[0].save(
        chemin_gif,
        save_all=True,
        append_images=images[1:],
        duration=800,  # 800 ms par image
        loop=0,         # boucle infinie
    )
    for img in images:
        img.close()
    print(f"\nGIF animé écrit dans {chemin_gif} ({len(images)} images)")

    # 4) Nettoyage des PNG temporaires.
    for chemin_png in chemins_png:
        chemin_png.unlink()
    print("PNG temporaires supprimés.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
