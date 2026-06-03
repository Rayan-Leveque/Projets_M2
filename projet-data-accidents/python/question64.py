"""Question 6.4 (question libre) — Conditions atmosphériques × état de la surface.

Question définie pour cette question libre :
  « Comment les accidents se répartissent-ils selon les conditions
    atmosphériques (atm) croisées avec l'état de la surface de la route
    (surf) ? »

Deux types de table sont mobilisés (contrainte de l'énoncé : au moins deux) :
  - caracteristiques : attribut « atm » (conditions atmosphériques).
  - lieux            : attribut « surf » (état de la surface de la route).
Les deux tables sont jointes accident par accident via la clé « Num_Acc ».

Type d'affichage : une HEATMAP (carte de chaleur), affichage non encore
utilisé dans les questions précédentes (camembert exclu par l'énoncé).
Chaque cellule (ligne = condition atmosphérique, colonne = état de surface)
porte le nombre d'accidents cumulés sur 2005-2015 (Groupe 1) correspondant.

Source : data/enriched/caracteristiques_<annee>.csv et lieux_<annee>.csv.

Filtrage :
  France métropolitaine uniquement (normaliser_dep sur le département de la
  table caractéristiques ; les DOM et codes invalides sont écartés).

Valeurs manquantes :
  - atm  : cellule vide → accident ignoré.
  - surf : cellule vide ou « 0 » (sentinelle « non renseigné ») → ignoré.

Sortie :
  - results/reponse64.png : heatmap atm (lignes) × surf (colonnes), chaque
    cellule annotée du nombre d'accidents.
"""

import csv
import sys

import matplotlib

matplotlib.use("Agg")  # rendu hors écran : on écrit directement un fichier PNG
import matplotlib.pyplot as plt

from common import (
    ENRICHED,
    RESULTS,
    ANNEE_DEBUT,
    ANNEE_FIN,
    normaliser_dep,
)

# Modalités attendues, dans l'ordre des codes du référentiel BAAC.
# On fige l'ordre et la liste pour avoir une heatmap stable d'une exécution
# à l'autre, indépendamment des valeurs réellement rencontrées.
VALEURS_ATM = [
    "1 - Normale",
    "2 - Pluie légère",
    "3 - Pluie forte",
    "4 - Neige - grêle",
    "5 - Brouillard - fumée",
    "6 - Vent fort - tempête",
    "7 - Temps éblouissant",
    "8 - Temps couvert",
    "9 - Autre",
]
VALEURS_SURF = [
    "1 - Normale",
    "2 - Mouillée",
    "3 - Flaques",
    "4 - Inondée",
    "5 - Enneigée",
    "6 - Boue",
    "7 - Verglacée",
    "8 - Corps gras - huile",
    "9 - Autre",
]


def abreger(libelle: str) -> str:
    """« 2 - Pluie légère » → « Pluie légère » : libellé court sans le code.

    On retire le code numérique de tête puis on ne garde que les deux
    premiers mots. Deux mots (et non un seul) sont nécessaires pour ne pas
    confondre « Pluie légère »/« Pluie forte » ni « Temps éblouissant »/
    « Temps couvert », tout en gardant des étiquettes d'axe assez courtes.
    """
    texte = libelle.split(" - ", 1)[1] if " - " in libelle else libelle
    texte = texte.replace(" - ", " ")  # « Neige - grêle » → « Neige grêle »
    return " ".join(texte.split()[:2])


def construire_matrice() -> list[list[int]]:
    """Cumule, sur 2005-2015, le nb d'accidents par couple (atm, surf).

    Renvoie une matrice d'entiers : matrice[i][j] = nombre d'accidents dont
    la condition atmosphérique est VALEURS_ATM[i] et l'état de surface
    VALEURS_SURF[j]. France métropolitaine uniquement.
    """
    idx_atm = {valeur: i for i, valeur in enumerate(VALEURS_ATM)}
    idx_surf = {valeur: j for j, valeur in enumerate(VALEURS_SURF)}
    matrice = [[0] * len(VALEURS_SURF) for _ in VALEURS_ATM]

    nb_atm_ignore = 0   # atm vide ou hors référentiel
    nb_surf_ignore = 0  # surf vide / « 0 » / hors référentiel

    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        print(f"[..]   {annee}")

        # 1) Table caractéristiques : on retient, pour les accidents de
        #    métropole, la condition atmosphérique indexée par Num_Acc.
        atm_par_acc: dict[str, str] = {}
        chemin_carac = ENRICHED / f"caracteristiques_{annee}.csv"
        with chemin_carac.open("r", encoding="utf-8", newline="") as f:
            lecteur = csv.reader(f)
            entete = next(lecteur)
            i_num = entete.index("Num_Acc")
            i_dep = entete.index("dep")
            i_atm = entete.index("atm")
            for ligne in lecteur:
                if normaliser_dep(ligne[i_dep]) is None:
                    continue  # hors métropole
                atm_par_acc[ligne[i_num]] = ligne[i_atm]

        # 2) Table lieux : pour chaque accident de métropole, on lit l'état
        #    de surface et on incrémente la cellule (atm, surf).
        chemin_lieux = ENRICHED / f"lieux_{annee}.csv"
        with chemin_lieux.open("r", encoding="utf-8", newline="") as f:
            lecteur = csv.reader(f)
            entete = next(lecteur)
            i_num = entete.index("Num_Acc")
            i_surf = entete.index("surf")
            for ligne in lecteur:
                num_acc = ligne[i_num]
                if num_acc not in atm_par_acc:
                    continue  # accident hors métropole (ou absent de carac)

                atm = atm_par_acc[num_acc]
                surf = ligne[i_surf]

                if atm not in idx_atm:
                    nb_atm_ignore += 1
                    continue
                if surf not in idx_surf:
                    nb_surf_ignore += 1
                    continue

                matrice[idx_atm[atm]][idx_surf[surf]] += 1

        cumul = sum(sum(ligne) for ligne in matrice)
        print(f"  [OK] {annee} : {cumul} accidents cumulés (métropole)")

    print(f"\nAccidents à atm non exploitable (ignorés)  : {nb_atm_ignore}")
    print(f"Accidents à surf non exploitable (ignorés) : {nb_surf_ignore}")
    return matrice


def tracer_heatmap(matrice: list[list[int]]) -> None:
    """Trace et enregistre la heatmap dans results/reponse64.png."""
    etiquettes_atm = [abreger(v) for v in VALEURS_ATM]
    etiquettes_surf = [abreger(v) for v in VALEURS_SURF]

    fig, ax = plt.subplots(figsize=(11, 8))
    # Échelle de couleur logarithmique : sans cela, la modalité ultra-
    # dominante (atm « Normale » × surf « Normale ») écrase toutes les
    # autres cellules dans la même teinte.
    image = ax.imshow(
        matrice,
        cmap="YlOrRd",
        aspect="auto",
        norm=matplotlib.colors.LogNorm(vmin=1),
    )

    # Graduation des axes avec les libellés abrégés.
    ax.set_xticks(range(len(etiquettes_surf)))
    ax.set_xticklabels(etiquettes_surf, rotation=45, ha="right")
    ax.set_yticks(range(len(etiquettes_atm)))
    ax.set_yticklabels(etiquettes_atm)

    # Annotation de chaque cellule par son effectif (séparateur de milliers).
    # Texte en blanc sur les cellules foncées, en noir sinon, pour le contraste.
    max_val = max(max(ligne) for ligne in matrice)
    for i, ligne in enumerate(matrice):
        for j, valeur in enumerate(ligne):
            couleur = "white" if valeur > max_val * 0.10 else "black"
            ax.text(j, i, f"{valeur:,}".replace(",", " "),
                    ha="center", va="center", color=couleur, fontsize=8)

    ax.set_title("Accidents par conditions atmosphériques et état de la "
                 "surface\n(France métropolitaine, cumul 2005-2015)")
    ax.set_xlabel("État de la surface (surf)")
    ax.set_ylabel("Conditions atmosphériques (atm)")
    fig.colorbar(image, ax=ax, label="Nombre d'accidents (échelle log)")
    fig.tight_layout()

    chemin = RESULTS / "reponse64.png"
    fig.savefig(chemin, dpi=150)
    plt.close(fig)
    print(f"Heatmap écrite dans {chemin}")


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    matrice = construire_matrice()

    total = sum(sum(ligne) for ligne in matrice)
    print(f"\nTotal accidents exploités (métropole, 2005-2015) : {total}")

    # Couple (atm, surf) le plus fréquent.
    i_max = j_max = 0
    for i, ligne in enumerate(matrice):
        for j, valeur in enumerate(ligne):
            if valeur > matrice[i_max][j_max]:
                i_max, j_max = i, j
    effectif_max = f"{matrice[i_max][j_max]:,}".replace(",", " ")
    print(f"Couple le plus fréquent : atm « {VALEURS_ATM[i_max]} » × "
          f"surf « {VALEURS_SURF[j_max]} » "
          f"({effectif_max} accidents, "
          f"{100 * matrice[i_max][j_max] / total:.1f} %)")

    tracer_heatmap(matrice)
    return 0


if __name__ == "__main__":
    sys.exit(main())
