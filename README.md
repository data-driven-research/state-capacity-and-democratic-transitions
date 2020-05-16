regimes-and-governance-project
==============================

Group project for Regimes and Governance.

TO-DO
------------
1. Add `Makefile`, `binder`

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README.
    ├── data
    │   ├── processed      <- The final, canonical data sets for analysis.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-hp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as PDF.
    │   └── figures        <- Generated graphics and figures to be used in reporting.
    │
    └── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── data           <- Scripts to download or generate data
        │   └── make_dataset.py
        │
        └── visualization  <- Scripts to create exploratory and results oriented visualizations
            └── visualize.py
