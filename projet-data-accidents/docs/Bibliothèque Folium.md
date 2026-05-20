# Bibliothèque Python Folium

**Auteurs :** Georges Grosz, Louis Giron  
**Date :** Mai 2026

---

## Définition

**FOLIUM** est :
- Bibliothèque Python basée sur Leaflet.js (bibliothèque JavaScript dédiée à la création de cartes interactives sur le web).
- Génère des cartes interactives HTML.
- Facile à utiliser avec Pandas.
- Fonctionne dans Jupyter Notebook.

**Installation :**
```bash
pip install folium
```

**Première carte :**
```python
import folium

# Carte centrée sur Paris avec un marqueur
m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)
folium.Marker([48.8566, 2.3522], popup="Paris").add_to(m)
m.save("folium1.html")
```

---

## Exemple avec plusieurs marqueurs

```python
import pandas as pd
import folium
from folium.plugins import HeatMap

# Création des données
data = pd.DataFrame({
    "ville": ["Paris", "Lyon", "Marseille"],
    "lat": [48.85, 45.76, 43.29],
    "lon": [2.35, 4.83, 5.37],
    "nb_accidents": [10, 500, 300]
})

# Création de la carte
carte = folium.Map(location=[46.5, 2.5], zoom_start=6)

# Ajout des marqueurs
for _, row in data.iterrows():
    folium.Marker(
        [row["lat"], row["lon"]],
        popup=row["ville"]
    ).add_to(carte)

# Sauvegarde
carte.save("folium2.html")
```

---

## Ajouts avancés

### Cercles proportionnels

```python
for _, row in data.iterrows():
    folium.Circle(
        location=[row["lat"], row["lon"]],
        radius=row["nb_accidents"] * 200,  # proportionnel
        color="red",
        fill=True,
        fill_opacity=0.4,
        popup=f"{row['ville']} - Intensité"
    ).add_to(carte)
```

### Heatmap (carte de chaleur)

Met en évidence l'intensité ou la densité d'un phénomène sur une zone géographique grâce à des couleurs.

```python
points = data[["lat", "lon"]].values.tolist()
HeatMap(points).add_to(carte)

# Sauvegarde de la carte
carte.save("carte_folium.html")
```

---

## Objets folium

| # | Objet | Description |
|---|-------|-------------|
| 1 | **Markers** | Affichent un point précis sur la carte |
| 2 | **Circle / CircleMarker** | Représentent une intensité d'un point d'une carte |
| 3 | **Heatmap** | Montre la densité de points |
| 4 | **Choropleth** | Colore des zones géographiques |
| 5 | **Polyline** | Représentent des trajets |
| 6 | **Polygon** | Délimitent une zone |
| 7 | **TileLayer** | Permettent de changer le fond de carte (vue satellite, vue terrain) |

### Synthèse métier

| Besoin métier | Objet folium |
|---------------|--------------|
| Localiser | Marker |
| Quantifier | Circle |
| Identifier zones denses | Heatmap |
| Comparer territoires | Choropleth |
| Visualiser flux | Polyline |
| Délimiter | Polygon |

---

## Conclusion

Folium : bibliothèque python simple et puissante pour la visualisation géographique.

### Limites

- Peu adapté aux très gros volumes.
- Moins puissant que des outils SIG.
- Personnalisation limitée.
