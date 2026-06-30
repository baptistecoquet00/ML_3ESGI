# TP : Machine Learning 2ESGI

Trois travaux pratiques complets, un par algorithme de mise en pratique du cours.
Code Python 3.13, environnement gere avec [uv](https://docs.astral.sh/uv/).

| TP | Sujet | Algorithme | Jeu de donnees reel | Script |
|----|-------|------------|---------------------|--------|
| 1 | Segmentation de vins | K-means + ACP | *Wine* (178 vins) | `tp1_kmeans_acp.py` |
| 2 | Diagnostic de tumeurs | Arbre de decision | *Breast Cancer* (569 cas) | `tp2_arbre_decision.py` |
| 3 | Prix de l'immobilier | Regression lineaire | *California Housing* (20 640) | `tp3_regression_lineaire.py` |

Chaque TP suit le meme procede que le cours : **fonctionnement -> modelisation
-> evaluation -> visualisation -> qualification / prise de decision**. Les
donnees sont **reelles** (datasets scikit-learn), chargees dans `data.py`. Wine et
Breast Cancer sont embarques ; California Housing est telecharge une fois puis
mis en cache.

## Prerequis

- [uv](https://docs.astral.sh/uv/) installe (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- uv installe automatiquement Python 3.13 si besoin.
- **Sans uv / stack plus ancienne** : Python 3.9+ et `pip` suffisent (voir ci-dessous).

## Installation

```bash
make install      # uv sync : cree la venv .tp_ml_2esgi et installe les dependances
# Alternative sans uv (Python 3.9+) :
make venv-pip     # python -m venv .tp_ml_2esgi + pip install -r requirements.txt
```

## Lancer les TP

```bash
make tp1          # Clustering K-means + ACP
make tp2          # Arbre de decision
make tp3          # Regression lineaire
make all          # les trois a la suite
```

Chaque commande affiche les resultats etape par etape dans le terminal et
ecrit les figures (et un CSV pour le TP1) dans `outputs/`.

## Notebooks (version pedagogique)

Les memes TP existent au format **Jupyter**, en deux versions :

- `notebooks/` : **corriges** complets, avec explications et **sorties executees**.
- `todo/` : **versions a trous** pour les etudiants (`# TODO` a completer) +
  un `README.md` de **consignes** detaillees par algo.

Les notebooks sont **auto-suffisants** (chargement des donnees inclus).

```bash
make lab          # ouvre JupyterLab
make notebooks    # (re)genere corriges (executes) + versions a trous
```

> Les `.ipynb` sont generes par des scripts (`notebooks/_build_notebooks.py` et
> `todo/_build_todo.py`) pour rester reproductibles et faciles a versionner.
> Pour modifier durablement un notebook, editez le script puis `make notebooks`.

## Autres commandes

```bash
make format       # formate le code (ruff)
make lint         # analyse statique (ruff)
make clean        # supprime les sorties de outputs/
make help         # liste toutes les cibles
```

## Structure

```
tp/
├── pyproject.toml          # dependances + config (uv, Python >=3.13)
├── requirements.txt        # alternative pip (Python 3.9+)
├── .python-version         # 3.13
├── Makefile                # raccourcis make (venv .tp_ml_2esgi)
├── data.py                 # chargement des jeux de donnees REELS (sklearn)
├── _viz.py                 # palette + helpers matplotlib (style du cours)
├── tp1_kmeans_acp.py       # scripts (version "tout-en-un")
├── tp2_arbre_decision.py
├── tp3_regression_lineaire.py
├── notebooks/              # corriges Jupyter (avec sorties)
│   ├── _build_notebooks.py
│   ├── TP1_kmeans_acp.ipynb
│   ├── TP2_arbre_decision.ipynb
│   └── TP3_regression_lineaire.ipynb
├── todo/                   # versions a trous + consignes etudiants
│   ├── README.md
│   ├── _build_todo.py
│   ├── TP1_kmeans_acp_TODO.ipynb
│   ├── TP2_arbre_decision_TODO.ipynb
│   └── TP3_regression_lineaire_TODO.ipynb
└── outputs/                # figures PNG + CSV generes par les scripts
```

## Pistes d'exercices (pour les etudiants)

- **TP1** : changer `k` et observer silhouette + ARI ; retirer la standardisation
  et constater la degradation.
- **TP2** : faire varier `max_depth` (2, 3, 6, None) et comparer accuracy
  train/test pour visualiser le sur-apprentissage.
- **TP3** : entrainer la regression sur la seule `MedInc` puis sur toutes les
  variables et comparer le R2.

Les consignes detaillees et le bareme sont dans [`todo/README.md`](todo/README.md).
