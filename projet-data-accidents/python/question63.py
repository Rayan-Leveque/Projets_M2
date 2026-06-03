"""Question 6.3 — Top 10 des départements avec le plus d'accidents (carte folium).

On parcourt les fichiers caracteristiques enrichis de ANNEE_DEBUT à ANNEE_FIN.
Chaque ligne = un accident (Num_Acc unique dans le fichier d'une année).
On cumule le nombre d'accidents par département de métropole (normaliser_dep),
puis :

  1. on écrit le tableau des 10 premiers départements dans results/reponse63.txt ;
  2. on construit une carte de France interactive (results/reponse63.html) :
       - cercles proportionnels au nb d'accidents pour les 10 premiers,
       - petits marqueurs discrets pour tous les autres départements,
       - popup indiquant le nom du département et le nombre d'accidents.
"""

import csv
import sys
from collections import Counter

import folium

from common import (
    ENRICHED, RESULTS, ANNEE_DEBUT, ANNEE_FIN,
    normaliser_dep, CENTROIDES_DEPARTEMENTS,
)


# Noms des départements de métropole (code INSEE -> nom), pour les popups.
NOMS_DEPARTEMENTS: dict[str, str] = {
    "01": "Ain", "02": "Aisne", "03": "Allier",
    "04": "Alpes-de-Haute-Provence", "05": "Hautes-Alpes",
    "06": "Alpes-Maritimes", "07": "Ardèche", "08": "Ardennes",
    "09": "Ariège", "10": "Aube", "11": "Aude", "12": "Aveyron",
    "13": "Bouches-du-Rhône", "14": "Calvados", "15": "Cantal",
    "16": "Charente", "17": "Charente-Maritime", "18": "Cher",
    "19": "Corrèze", "2A": "Corse-du-Sud", "2B": "Haute-Corse",
    "21": "Côte-d'Or", "22": "Côtes-d'Armor", "23": "Creuse",
    "24": "Dordogne", "25": "Doubs", "26": "Drôme", "27": "Eure",
    "28": "Eure-et-Loir", "29": "Finistère", "30": "Gard",
    "31": "Haute-Garonne", "32": "Gers", "33": "Gironde", "34": "Hérault",
    "35": "Ille-et-Vilaine", "36": "Indre", "37": "Indre-et-Loire",
    "38": "Isère", "39": "Jura", "40": "Landes", "41": "Loir-et-Cher",
    "42": "Loire", "43": "Haute-Loire", "44": "Loire-Atlantique",
    "45": "Loiret", "46": "Lot", "47": "Lot-et-Garonne", "48": "Lozère",
    "49": "Maine-et-Loire", "50": "Manche", "51": "Marne",
    "52": "Haute-Marne", "53": "Mayenne", "54": "Meurthe-et-Moselle",
    "55": "Meuse", "56": "Morbihan", "57": "Moselle", "58": "Nièvre",
    "59": "Nord", "60": "Oise", "61": "Orne", "62": "Pas-de-Calais",
    "63": "Puy-de-Dôme", "64": "Pyrénées-Atlantiques",
    "65": "Hautes-Pyrénées", "66": "Pyrénées-Orientales", "67": "Bas-Rhin",
    "68": "Haut-Rhin", "69": "Rhône", "70": "Haute-Saône",
    "71": "Saône-et-Loire", "72": "Sarthe", "73": "Savoie",
    "74": "Haute-Savoie", "75": "Paris", "76": "Seine-Maritime",
    "77": "Seine-et-Marne", "78": "Yvelines", "79": "Deux-Sèvres",
    "80": "Somme", "81": "Tarn", "82": "Tarn-et-Garonne", "83": "Var",
    "84": "Vaucluse", "85": "Vendée", "86": "Vienne", "87": "Haute-Vienne",
    "88": "Vosges", "89": "Yonne", "90": "Territoire de Belfort",
    "91": "Essonne", "92": "Hauts-de-Seine", "93": "Seine-Saint-Denis",
    "94": "Val-de-Marne", "95": "Val-d'Oise",
}


def compter_accidents_par_departement() -> Counter:
    """Cumule le nombre d'accidents par département de métropole."""
    compteur: Counter = Counter()
    for annee in range(ANNEE_DEBUT, ANNEE_FIN + 1):
        chemin = ENRICHED / f"caracteristiques_{annee}.csv"
        if not chemin.exists():
            print(f"  [MANQUANT] {chemin.name}")
            continue
        nb_annee = 0
        with chemin.open("r", encoding="utf-8", newline="") as f:
            lecteur = csv.reader(f)
            entete = next(lecteur)
            idx_dep = entete.index("dep")
            for ligne in lecteur:
                dep = normaliser_dep(ligne[idx_dep])
                if dep is not None:
                    compteur[dep] += 1
                    nb_annee += 1
        print(f"  {annee} : {nb_annee} accidents en métropole")
    return compteur


def ecrire_tableau(top10: list[tuple[str, int]]) -> None:
    """Écrit le tableau des 10 départements dans results/reponse63.txt."""
    chemin = RESULTS / "reponse63.txt"
    with chemin.open("w", encoding="utf-8") as f:
        f.write("Question 6.3 — Top 10 des départements avec le plus d'accidents\n")
        f.write("=" * 62 + "\n\n")
        f.write(f"Période cumulée : {ANNEE_DEBUT}-{ANNEE_FIN} (Groupe 1)\n")
        f.write("Champ : France métropolitaine (DOM exclus)\n\n")
        f.write(f"{'Rang':<5} {'Dép.':<5} {'Nom':<26} {'Nb accidents':>13}\n")
        f.write("-" * 51 + "\n")
        for rang, (dep, nb) in enumerate(top10, start=1):
            nom = NOMS_DEPARTEMENTS.get(dep, "?")
            f.write(f"{rang:<5} {dep:<5} {nom:<26} {nb:>13}\n")
    print(f"\nTableau écrit dans {chemin}")


def construire_carte(
    compteur: Counter, top10: list[tuple[str, int]]
) -> None:
    """Construit la carte folium (cercles top 10 + marqueurs discrets)."""
    nb_max = top10[0][1]  # plus gros département, pour normaliser les rayons
    deps_top10 = {dep for dep, _ in top10}

    carte = folium.Map(location=(46.5, 2.0), zoom_start=6, tiles="CartoDB positron")

    # Tous les autres départements : petit marqueur discret.
    for dep, nb in compteur.items():
        if dep in deps_top10 or dep not in CENTROIDES_DEPARTEMENTS:
            continue
        lat, lon = CENTROIDES_DEPARTEMENTS[dep]
        nom = NOMS_DEPARTEMENTS.get(dep, dep)
        folium.CircleMarker(
            location=(lat, lon),
            radius=2,
            color="#888888",
            fill=True,
            fill_color="#888888",
            fill_opacity=0.5,
            popup=folium.Popup(f"{nom} ({dep}) : {nb} accidents", max_width=250),
        ).add_to(carte)

    # Top 10 : cercles proportionnels au nb d'accidents (rayon en pixels).
    for rang, (dep, nb) in enumerate(top10, start=1):
        if dep not in CENTROIDES_DEPARTEMENTS:
            print(f"  [ATTENTION] pas de centroïde pour le département {dep}")
            continue
        lat, lon = CENTROIDES_DEPARTEMENTS[dep]
        nom = NOMS_DEPARTEMENTS.get(dep, dep)
        # Rayon proportionnel à nb : entre ~8 et 40 pixels selon l'ampleur.
        rayon = 8 + 32 * (nb / nb_max)
        texte = f"<b>#{rang} — {nom} ({dep})</b><br>{nb} accidents"
        folium.CircleMarker(
            location=(lat, lon),
            radius=rayon,
            color="#b30000",
            weight=2,
            fill=True,
            fill_color="#e34a33",
            fill_opacity=0.6,
            popup=folium.Popup(texte, max_width=250),
            tooltip=f"{nom} : {nb}",
        ).add_to(carte)

    chemin = RESULTS / "reponse63.html"
    carte.save(str(chemin))
    print(f"Carte écrite dans {chemin}")


def main() -> int:
    if not ENRICHED.is_dir():
        print(f"Dossier source introuvable : {ENRICHED}", file=sys.stderr)
        return 1
    RESULTS.mkdir(parents=True, exist_ok=True)

    print(f"Comptage des accidents par département ({ANNEE_DEBUT}-{ANNEE_FIN}) :")
    compteur = compter_accidents_par_departement()

    total = sum(compteur.values())
    print(f"\nTotal accidents métropole cumulés : {total}")
    print(f"Nombre de départements représentés : {len(compteur)}")

    top10 = compteur.most_common(10)
    print("\nTop 10 :")
    for rang, (dep, nb) in enumerate(top10, start=1):
        nom = NOMS_DEPARTEMENTS.get(dep, "?")
        print(f"  {rang:>2}. {dep} {nom:<22} {nb:>8}")

    ecrire_tableau(top10)
    construire_carte(compteur, top10)
    return 0


if __name__ == "__main__":
    sys.exit(main())
