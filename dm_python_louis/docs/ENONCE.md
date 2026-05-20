# Devoir maison

## Introduction

### Presentation

Ce devoir maison a pour ambition de mettre en pratique les connaissances et notions acquises autour de la programmation en Python et notamment:
- La manipulation de fonctions
- L'utilisation de packages standards et notamment Pandas
- La manipulation de données avec Pandas
- La visualisation de données avec Matplotlib

L'un des challenges des Data Analyst/Scientist est de présenter proprement et intelligiblement les résultats de leurs analyses.. Dans ce devoir maison, nous allons nous intéresser à la bibliothèque Streamlit qui permet de créer des applications web interactives en Python.

### Objectif

L'objectif de ce devoir maison est de créer une application ``Streamlit`` permettant de visualiser les données que vous aurez choisies. L'application doit permettre de:
- Visualiser le jeu de données
- Visualiser des indicateurs statistiques sur les données
- Interagir avec l'utilisateur pour lui fournir des informations sur les données
- Visualiser un graphique sur les données

### Pré-requis

- Python 3.10 ou supérieur
- Streamlit
- Pandas
- Matplotlib

Nous pourrons nous assurer que ces pré-requis sont bien respectés en classe.

## Données

Vous devez choisir un jeu de données parmi ceux proposés ci-dessous:

- [Average Daily Screen Time for Children](https://www.kaggle.com/datasets/ak0212/average-daily-screen-time-for-children)
  - *A dataset children's daily screen time habits*
- [Soil Pollution and Associated Health Impacts](https://www.kaggle.com/datasets/khushikyad001/soil-pollution-and-associated-health-impacts)
  - *A comprehensive synthetic dataset highlighting soil pollution cases.*
- [Fraud Detection Dataset](https://www.kaggle.com/datasets/amanalisiddiqui/fraud-detection-dataset)
  - *Records of financial transactions for fraud detection. A selection of 100 000 line items from the original dataset, randomly selected from the 6.3 million records.*
- [Hourly Energy Consumption](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption)
  - *Over 10 years of hourly energy consumption data from PJM in Megawatts.*
- [IMDB Movies Dataset](https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows)
  - *Top 1000 Movies by IMDB Rating*

## Organisation

Le devoir maison est à **réaliser seul**. Vous pouvez vous aider entre vous mais il est important que chacun réalise son propre devoir maison.

Le devoir maison est à rendre **au plus tard le 16 juin 2025**, lors du dernier cours de Python.

### Notation

Le devoir maison sera noté sur 20 points. La note se basera sur les critères suivants:
- La présence des 4 composants suivants dans l'application
  - Visualiser le jeu de données
  - Visualiser des indicateurs statistiques sur les données
  - Interagir avec l'utilisateur pour lui fournir des informations sur les données
  - Visualiser un graphique sur les données
- Le code est propre, lisible et bien structuré (e.g. naming conventions, indentation, utilisation des fonctions avec respects des bonnes pratiques etc.)
- La pertinence des choix de visualisation (e.g. le choix des graphiques, la pertinence des informations fournies etc.)
- La qualité de l'application

### Le rendu

Le rendu se fera sous la forme d'un PDF généré à partir de l'application Streamlit. Il vous suffira de lancer l'application Streamlit et d'utiliser la fonction d'export PDF de votre navigateur.

Vous devrez également rendre le code source de l'application Streamlit.

Le rendu via un dépôt GitHub sera préféré. Vous pouvez également rendre le code source sous la forme d'une archive ZIP. Dans ce cas, il faudra s'assurer que l'archive ZIP contient bien tous les fichiers nécessaires à l'exécution de l'application Streamlit.

## Détail du devoir maison

### 1. Mise en place de l'environnement

Installer streamlit dans l'environnement virtuel que vous utilisez pour le cours Python. Pour cela, vous pouvez utiliser la commande suivante:

```bash
mamba activate <nom_de_l_environnement>
mamba install streamlit
```

Assurez-vous que Streamlit est bien installé en lançant la commande suivante:

```bash
streamlit --version
```

### 2. Créer l'application Streamlit
Créer un fichier `app.py` dans lequel vous allez créer votre application Streamlit. Vous pouvez vous inspirer du code ci-dessous pour créer votre application:

```python
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set the page configuration
st.set_page_config(
    page_title="Devoir maison - Master MIMO - 2025",
    page_icon=":python:",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("Devoir maison - Master MIMO - 2025")
```

### 3. Lancer l'application Streamlit
Lancer l'application Streamlit en lançant la commande suivante:

```bash
streamlit run app.py
```
Vous devriez voir l'application s'ouvrir dans votre navigateur par défaut. Si ce n'est pas le cas, vous pouvez ouvrir votre navigateur et entrer l'URL suivante:

```
http://localhost:8501
```

### 4. Les composants obligatoires de l'application

#### 4.1 Visualiser le jeu de données

Ajouter un composant permettant de visualiser le jeu de données. Pour cela, vous pouvez utiliser la fonction `st.dataframe()` de Streamlit.

```python
# Load the dataset
df = pd.read_csv("/path/to/data.csv")
st.write("## Visualiser le jeu de données")
st.dataframe(df)
```

#### 4.2 Visualiser des indicateurs statistiques sur les données

Ajouter 3 indicateurs statistiques sur les données. Pour cela, vous pouvez utiliser la fonction `st.metric()` de Streamlit. Par exemple, pour afficher le nombre de lignes et de colonnes du jeu de données, vous pouvez utiliser le code suivant:

```python
st.write("## Indicateurs statistiques")
st.metric("Moyenne de la colonne", df[col].mean())
```

#### 4.3 Interagir avec l'utilisateur pour lui fournir des informations sur les données

Ajouter un composant permettant d'interagir avec l'utilisateur pour lui fournir des informations sur les données. Pour cela, vous pouvez utiliser la fonction `st.selectbox()` de Streamlit. Par exemple, pour afficher le nom de la colonne sélectionnée par l'utilisateur, vous pouvez utiliser le code suivant:

```python
st.write("## Interagir avec l'utilisateur")
column = st.selectbox("Sélectionner une colonne", df.columns)
st.write(f"Vous avez sélectionné la colonne: {column}")
```

Puis ajouter une opération sur le dataset en fonction de la colonne sélectionnée. Par exemple, vous pouvez afficher la moyenne de la colonne sélectionnée:

```python
st.write(f"Moyenne de la colonne {column}: {df[column].mean()}")
```

#### 4.4 Visualiser un graphique sur les données

Ajouter un composant permettant de visualiser un graphique sur les données. Pour cela, vous pouvez utiliser la fonction `st.pyplot()` de Streamlit et la bibliothèque Matplotlib. Vous pouvez également utiliser les fonctions **built-in** de Streamlit pour créer des graphiques (e.g. `st.line_chart()`, `st.bar_chart()`, `st.area_chart()`, etc.). 

```python
st.write("## Visualiser un graphique")
fig, ax = plt.subplots()
ax.plot(
    df[column],
    label=column,
)
ax.set_title(f"Graphique de la colonne {column}")
ax.set_xlabel("Index")
ax.set_ylabel(column)
ax.legend()
st.pyplot(fig)
```
Ou bien utiliser les fonctions **built-in** de Streamlit:

```python
st.write("## Visualiser un graphique")
st.line_chart(df[column])
```