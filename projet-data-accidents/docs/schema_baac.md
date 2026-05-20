# Schéma de référence BAAC — Groupe 1 (2005-2015)

> Document de référence construit à partir des PDF officiels ONISR (`description-des-bases-de-donnees-onisr-annees-2005-a-2018.pdf`) et vérifié sur les fichiers réels de `Données/utf8/`.

---

## 1. Architecture des données

Chaque accident corporel donne lieu à **4 fichiers CSV** reliés entre eux :

| Fichier | Granularité | Clé primaire | Clé vers autre table |
|---------|-------------|--------------|----------------------|
| **caracteristiques** | 1 ligne = 1 accident | `Num_Acc` | — |
| **lieux** | 1 ligne = 1 accident | `Num_Acc` | → `caracteristiques.Num_Acc` |
| **vehicules** | 1 ligne = 1 véhicule | `Num_Acc` + `num_veh` | → `caracteristiques.Num_Acc` |
| **usagers** | 1 ligne = 1 usager | `Num_Acc` + `num_veh` + `place` | → `vehicules.(Num_Acc, num_veh)` |

- **`Num_Acc`** (numérique) : identifiant unique de l'accident, présent dans les 4 fichiers.
- **`num_veh`** (alphanumérique, ex. `A01`, `B02`) : identifiant du véhicule au sein d'un accident.
- **`place`** (numérique) : place occupée par l'usager dans le véhicule.

### Remarques importantes pour les jointures
- Un accident a **toujours** une ligne dans `caracteristiques` et **au moins un** véhicule dans `vehicules`.
- Un véhicule peut n'avoir **aucun** usager dans `usagers` (conducteur en fuite, non créé dans la base) → Q2.2.
- Un usager dans `usagers` doit toujours pointer vers un véhicule existant dans `vehicules` → Q2.1.
- Un accident a **un seul** lieu dans `lieux` → Q2.4.
- Chaque lieu doit correspondre à un accident existant dans `caracteristiques` → Q2.3.

---

## 2. Convention des valeurs manquantes

Les PDF officiels précisent :

> *"La plupart des variables contenues dans les quatre fichiers peuvent contenir des cellules vides ou un zéro ou un point. Il s'agit, dans ces trois cas, d'une cellule non renseignée par les forces de l'ordre ou sans objet."*

**En pratique (2005-2015) :**
- Cellule vide `''`
- Point `'.'`
- Zéro `'0'` ou `'00'` ou `'000'` selon la largeur de la colonne
- `-1` pour certaines variables énumérées (notamment dans les descriptions récentes, mais à vérifier année par année)

**Attention Q4** : distinguer les valeurs manquantes des vraies valeurs numériques (ex. `0` pour `nbv` = "0 voies" est différent de `0` = non renseigné).

---

## 3. Schéma détaillé par fichier

### 3.1 CARACTERISTIQUES

Colonnes réelles (identiques 2005-2015) :
`Num_Acc, an, mois, jour, hrmn, lum, agg, int, atm, col, com, adr, gps, lat, long, dep`

| Colonne | Type | Description | Valeurs énumérées |
|---------|------|-------------|-------------------|
| `Num_Acc` | int | Identifiant unique de l'accident | — |
| `an` | int | Année (dernier(s) chiffre(s)) : 2005→`5`, 2010→`10`, 2015→`15` | — |
| `mois` | int | Mois (1-12) | — |
| `jour` | int | Jour du mois | — |
| `hrmn` | str | Heure et minutes (`HHMM`, ex. `1900`, `0805`) | — |
| `lum` | int | Conditions d'éclairage | 1=Plein jour, 2=Crépuscule/aube, 3=Nuit sans éclairage public, 4=Nuit éclairage public non allumé, 5=Nuit éclairage public allumé |
| `agg` | int | Localisation | 1=Hors agglomération, 2=En agglomération |
| `int` | int | Intersection | 1=Hors intersection, 2=X, 3=T, 4=Y, 5=Plus de 4 branches, 6=Giratoire, 7=Place, 8=Passage à niveau, 9=Autre |
| `atm` | int | Conditions atmosphériques | 1=Normale, 2=Pluie légère, 3=Pluie forte, 4=Neige-grêle, 5=Brouillard-fumée, 6=Vent fort-tempête, 7=Temps éblouissant, 8=Temps couvert, 9=Autre |
| `col` | int | Type de collision | 1=Deux véhicules frontale, 2=Deux véhicules par l'arrière, 3=Deux véhicules par le côté, 4=Trois+ en chaîne, 5=Trois+ collisions multiples, 6=Autre collision, 7=Sans collision |
| `com` | str | Code commune INSEE (3 chiffres calés à droite) | — |
| `adr` | str | Adresse postale (renseignée en agglomération) | — |
| `gps` | str | Indicateur de provenance géo | `M`=Métropole, `A`=Antilles, `G`=Guyane, `R`=Réunion, `Y`=Mayotte |
| `lat` | str | Latitude (en degrés décimaux × 100, ex. `5051500`) | — |
| `long` | str | Longitude (en degrés décimaux × 100, ex. `0294400`) | — |
| `dep` | str | Code département INSEE + `0` (3 caractères). Ex: `590`=Nord, `751`=Paris, `201`=Corse-du-Sud, `202`=Haute-Corse | — |

**Note sur les DOM** : le projet se limite à la France métropolitaine. Filtrer `dep` sur les codes 2 chiffres + `0` (ou 201/202 pour la Corse) et exclure les codes outre-mer (971, 972, 973, 974, 976...).

---

### 3.2 LIEUX

Colonnes réelles (identiques 2005-2015) :
`Num_Acc, catr, voie, v1, v2, circ, nbv, pr, pr1, vosp, prof, plan, lartpc, larrout, surf, infra, situ, env1`

| Colonne | Type | Description | Valeurs énumérées |
|---------|------|-------------|-------------------|
| `Num_Acc` | int | Identifiant de l'accident | — |
| `catr` | int | Catégorie de route | 1=Autoroute, 2=Route nationale, 3=Route départementale, 4=Voie communale, 5=Hors réseau public, 6=Parc de stationnement, 9=Autre |
| `voie` | str | Numéro de la route | — |
| `v1` | str | Indice numérique (ex. `2` pour "bis") | — |
| `v2` | str | Indice alphanumérique (ex. `B`) | — |
| `circ` | int | Régime de circulation | 1=Sens unique, 2=Bidirectionnelle, 3=Chaussées séparées, 4=Voies d'affectation variable |
| `nbv` | str | Nombre total de voies | — |
| `pr` | str | Numéro du PR de rattachement | — |
| `pr1` | str | Distance en mètres au PR | — |
| `vosp` | int | Voie réservée | 0=Sans objet, 1=Piste cyclable, 2=Banque cyclable, 3=Voie réservée |
| `prof` | int | Profil en long | 1=Plat, 2=Pente, 3=Sommet de côte, 4=Bas de côte |
| `plan` | int | Tracé en plan | 1=Partie rectiligne, 2=Courbe à gauche, 3=Courbe à droite, 4=En S |
| `lartpc` | str | Largeur du terre-plein central (m) | — |
| `larrout` | str | Largeur de la chaussée (m) | — |
| `surf` | int | État de la surface | 1=Normale, 2=Mouillée, 3=Flaques, 4=Inondée, 5=Enneigée, 6=Boue, 7=Verglacée, 8=Corps gras-huile, 9=Autre |
| `infra` | int | Aménagement-infrastructure | 0=Aucun, 1=Souterrain-tunnel, 2=Pont-autopont, 3=Bretelle d'échangeur, 4=Voie ferrée, 5=Carrefour aménagé, 6=Zone piétonne, 7=Zone de péage |
| `situ` | int | Situation de l'accident | 1=Sur chaussée, 2=Bande d'arrêt d'urgence, 3=Sur accotement, 4=Sur trottoir, 5=Sur piste cyclable |
| `env1` | str | Proximité d'une école (?) — champ peu documenté dans la tranche 2005-2015 | `00`=Non ? |

**Note** : `vma` (vitesse max autorisée) n'apparaît **pas** dans les fichiers 2005-2015.

---

### 3.3 VEHICULES

Colonnes réelles (identiques 2005-2015) :
`Num_Acc, senc, catv, occutc, obs, obsm, choc, manv, num_veh`

| Colonne | Type | Description | Valeurs énumérées |
|---------|------|-------------|-------------------|
| `Num_Acc` | int | Identifiant de l'accident | — |
| `senc` | int | Sens de circulation | 1=PK/PR croissant, 2=PK/PR décroissant |
| `catv` | str | Catégorie du véhicule | `01`=Bicyclette, `02`=Cyclomoteur <50cm³, `03`=Voiturette, `07`=VL seul, `10`=VU seul 1,5T≤PTAC≤3,5T, `13`=PL 3,5T<PTAC≤7,5T, `14`=PL >7,5T, `15`=PL >3,5T + remorque, `16`=Tracteur routier seul, `17`=Tracteur + semi, `20`=Engin spécial, `21`=Tracteur agricole, `30`=Scooter <50cm³, `31`=Motocyclette >50 et ≤125cm³, `32`=Scooter >50 et ≤125cm³, `33`=Motocyclette >125cm³, `34`=Scooter >125cm³, `35`=Quad léger ≤50cm³, `36`=Quad lourd >50cm³, `37`=Autobus, `38`=Autocar, `39`=Train, `40`=Tramway, `99`=Autre |
| `occutc` | str | Nombre d'occupants dans le transport en commun | — |
| `obs` | str | Obstacle fixe heurté | `00`=Sans objet, `1`=Véhicule en stationnement, `2`=Arbre, `3`=Glissière métallique, `4`=Glissière béton, `5`=Autre glissière, `6`=Bâtiment/mur/pile, `7`=Support de signalisation, `8`=Poteau, `9`=Mobilier urbain, `10`=Parapet, `11`=Ilot/refuge/borne, `12`=Bordure de trottoir, `13`=Fossé/talus/roche, `14`=Autre obstacle fixe chaussée, `15`=Autre obstacle fixe trottoir, `16`=Sortie de chaussée sans obstacle |
| `obsm` | int | Obstacle mobile heurté | `0`=Aucun, `1`=Piéton, `2`=Véhicule, `4`=Véhicule sur rail, `5`=Animal domestique, `6`=Animal sauvage, `9`=Autre |
| `choc` | int | Point de choc initial | `0`=Aucun, `1`=Avant, `2`=Avant droit, `3`=Avant gauche, `4`=Arrière, `5`=Arrière droit, `6`=Arrière gauche, `7`=Côté droit, `8`=Côté gauche, `9`=Chocs multiples |
| `manv` | str | Manœuvre principale avant l'accident | `01`=Sans changement de direction, `02`=Même sens même file, `03`=Entre 2 files, `04`=En marche arrière, `05`=À contresens, `06`=Franchissement TPC, `07`=Couloir bus même sens, `08`=Couloir bus sens inverse, `09`=En s'insérant, `10`=Demi-tour, `11`=Chgt file à gauche, `12`=Chgt file à droite, `13`=Déporté à gauche, `14`=Déporté à droite, `15`=Tournant à gauche, `16`=Tournant à droite, `17`=Dépassant à gauche, `18`=Dépassant à droite, `19`=Traversant, `20`=Stationnement, `21`=Évitement, `22`=Ouverture de porte, `23`=Arrêté (hors stationnement), `24`=En stationnement (avec occupants) |
| `num_veh` | str | Identifiant du véhicule | `A01`, `B02`, ... |

---

### 3.4 USAGERS

Colonnes réelles (identiques 2005-2015) :
`Num_Acc, place, catu, grav, sexe, trajet, secu, locp, actp, etatp, an_nais, num_veh`

| Colonne | Type | Description | Valeurs énumérées |
|---------|------|-------------|-------------------|
| `Num_Acc` | int | Identifiant de l'accident | — |
| `place` | int | Place occupée dans le véhicule | 1=Conducteur, 2=Passager avant, 3=Passager arrière gauche, etc. (schéma dans le PDF) |
| `catu` | int | Catégorie d'usager | 1=Conducteur, 2=Passager, 3=Piéton |
| `grav` | int | Gravité de l'accident | 1=Indemne, 2=Tué, 3=Blessé hospitalisé, 4=Blessé léger |
| `sexe` | int | Sexe | 1=Masculin, 2=Féminin |
| `trajet` | int | Motif du déplacement | 1=Domicile-travail, 2=Domicile-école, 3=Courses-achats, 4=Utilisation professionnelle, 5=Promenade-loisirs, 9=Autre |
| `secu` | str | **2 caractères** : 1er = équipement, 2e = utilisation | Voir ci-dessous |
| `locp` | int | Localisation du piéton | `0`=Sans objet, `1`=À +50m passage piéton, `2`=À -50m passage piéton, `3`=Passage piéton sans signalisation, `4`=Passage piéton avec signalisation, `5`=Sur trottoir, `6`=Sur accotement, `7`=Sur refuge/BAU, `8`=Sur contre-allée |
| `actp` | int | Action du piéton | `0`=Non renseigné/sans objet, `1`=Sens véhicule heurtant, `2`=Sens inverse, `3`=Traversant, `4`=Masqué, `5`=Jouant-courant, `6`=Avec animal, `9`=Autre |
| `etatp` | int | État du piéton | `0`=Non renseigné, `1`=Seul, `2`=Accompagné, `3`=En groupe |
| `an_nais` | int | Année de naissance | — |
| `num_veh` | str | Identifiant du véhicule | `A01`, `B02`, ... |

#### Décodage de `secu` (2 caractères)

| 1er car. (équipement) | 2e car. (utilisation) |
|-----------------------|-----------------------|
| 1=Ceinture | 1=Oui |
| 2=Casque | 2=Non |
| 3=Dispositif enfants | 3=Non déterminable |
| 4=Équipement réfléchissant | |
| 9=Autre | |

Exemple : `secu="11"` = Ceinture portée. `secu="12"` = Ceinture non portée.

---

## 4. Référence rapide pour les questions suivantes

### Q1.3 — Enrichissement
Remplacer les codes numériques des colonnes énumérées par leur libellé textuel.
Colonnes à enrichir :
- **caracteristiques** : `lum`, `agg`, `int`, `atm`, `col`
- **lieux** : `catr`, `circ`, `vosp`, `prof`, `plan`, `surf`, `infra`, `situ`
- **vehicules** : `senc`, `catv`, `obs`, `obsm`, `choc`, `manv`
- **usagers** : `catu`, `grav`, `sexe`, `trajet`, `locp`, `actp`, `etatp`

### Q2.x — Intégrité référentielle
- **Q2.1** : Vérifier que tout `(Num_Acc, num_veh)` dans `usagers` existe dans `vehicules`.
- **Q2.2** : Vérifier que tout véhicule dans `vehicules` a au moins un usager dans `usagers` (sinon = conducteur en fuite).
- **Q2.3** : Vérifier que tout `Num_Acc` dans `lieux` existe dans `caracteristiques`.
- **Q2.4** : Vérifier qu'un `Num_Acc` dans `caracteristiques` n'a qu'une seule ligne dans `lieux`.

### Q3.1 — Répartition des attributs énumérés (usagers)
Calculer les pourcentages pour `catu`, `grav`, `sexe`, `trajet`, `secu`, `locp`, `actp`, `etatp`.

### Q4.1 — Taux de valeurs absentes (véhicules)
Compter les cellules vides / `.` / `0` / `00` / `000` selon la colonne.
Attention : `0` pour `senc` peut être "non renseigné" (dans certaines années) ou "inconnu".

### Q5.x — Cohérences inter-attributs
- **Q5.1** : `lum` vs `hrmn` — ex. `lum=1` (plein jour) à `hrmn=0200` est suspect.
- **Q5.2** et **Q5.3** : À inventer — idées :
  - `agg=2` (en agglomération) mais `adr` vide
  - `catu=3` (piéton) mais `place ≠ 10` (si place=10 signifie piéton)
  - `grav=1` (indemne) mais `an_nais` vide (moins critique)
  - `obs` ou `obsm` renseigné mais `choc=0` (aucun choc)

### Q6.x — Visualisations
- **Q6.1** : Agréger `hrmn` par tranche d'1h (`hrmn // 100`).
- **Q6.2** : `grav=2` (tués) groupés par tranche d'âge de 5 ans et `sexe`.
  Âge = `an - an_nais` (ou `2005..2015 - an_nais`). Attention aux `an_nais` manquants.
- **Q6.3** : Compter les accidents par `dep`, carte Folium.
- **Q6.4** : Question libre — exemple : répartition des accidents par `atm` et `surf` croisées.
- **Q6.5** : GIF animé par année de la carte Q6.3.

---

## 5. Pièges et spécificités de la tranche 2005-2015

| Piège | Explication |
|-------|-------------|
| `an` n'est pas l'année complète | `5` = 2005, `10` = 2010, `15` = 2015. Pour calculer l'âge, utiliser `an + 2000` si `an < 100` (ou mieux : récupérer l'année depuis le nom de fichier ou `an + 2000` si `an < 50` sinon `an + 1900` — mais en pratique pour 2005-2015, `an + 2000` marche sauf si `an=5` donne 2005, `an=10`→2010, `an=15`→2015). |
| `lat` / `long` | Stockés en centièmes de degrés (×100) sous forme de chaînes. `5051500` → `50.51500`. Certains peuvent être vides ou à `0`. |
| `dep` = INSEE + `0` | 3 caractères (`590`, `751`). La Corse est `201` / `202` (pas `2A`/`2B` dans cette tranche). |
| `secu` = 2 caractères | Ne pas traiter comme un entier. `11`, `12`, `21`... |
| `catv`, `manv`, `obs` | Souvent zero-paddés (`07`, `01`, `00`). Les stocker comme chaînes ou normaliser en int selon le besoin. |
| `env1` | Présent dans les CSV mais peu documenté dans les PDF 2005-2018. Probablement école à proximité. |
| DOM à exclure | Si des fichiers contiennent des départements outre-mer, les exclure de l'analyse métropolitaine. |

---

## 6. Fichiers sources

- `Données/raw/description-des-bases-de-donnees-onisr-annees-2005-a-2018.pdf` — description correspondant exactement à notre tranche 2005-2015.
- `Données/raw/description-des-bases-de-donnees-annuelles.pdf` — description plus récente (2005-2024) avec des évolutions de schéma (ex. `id_vehicule`, `secu1/secu2/secu3`, `vma`) qui **n'existent pas** dans nos données.
