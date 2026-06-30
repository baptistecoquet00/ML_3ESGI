.DEFAULT_GOAL := help

# Nom de l'environnement virtuel (utilise par uv ET par la voie pip).
VENV := .tp_ml_2esgi
UV := uv
# uv cree/charge la venv au nom choisi via cette variable d'environnement.
export UV_PROJECT_ENVIRONMENT := $(VENV)

.PHONY: help install venv-pip tp1 tp2 tp3 all lab notebooks format lint clean

help:  ## Affiche cette aide
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

install:  ## Cree la venv .tp_ml_2esgi et installe les dependances (uv, recommande)
	$(UV) sync
	@echo "venv prete : $(VENV)  (activer : source $(VENV)/bin/activate)"

venv-pip:  ## Alternative sans uv : venv + pip install -r requirements.txt
	python3 -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install -r requirements.txt
	@echo "venv prete : $(VENV)  (activer : source $(VENV)/bin/activate)"

tp1:  ## TP1 : Clustering K-means + ACP (Wine)
	$(UV) run python tp1_kmeans_acp.py

tp2:  ## TP2 : Classification par arbre de decision (Breast Cancer)
	$(UV) run python tp2_arbre_decision.py

tp3:  ## TP3 : Regression lineaire (California Housing)
	$(UV) run python tp3_regression_lineaire.py

all: tp1 tp2 tp3  ## Lance les trois TP

lab:  ## Ouvre JupyterLab sur les notebooks
	$(UV) run jupyter lab notebooks

notebooks:  ## (Re)genere les notebooks corriges (executes) et a trous
	$(UV) run python notebooks/_build_notebooks.py
	$(UV) run python todo/_build_todo.py
	$(UV) run jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb
	@echo "Corriges executes (avec sorties) ; versions a trous laissees vierges."

format:  ## Formate le code (ruff)
	$(UV) run ruff format .

lint:  ## Analyse le code (ruff)
	$(UV) run ruff check .

clean:  ## Supprime les sorties generees
	rm -rf outputs/*.png outputs/*.csv
