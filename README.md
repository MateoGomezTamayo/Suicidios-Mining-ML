# Suicidios Mining ML

Big Data and Data Mining project to analyze suicide attempt records (SIVIGILA), integrating an AWS data architecture (Bronze/Silver/Gold) with a CRISP-DM workflow for risk modeling.

## Author

- Mateo Gomez Tamayo

## Overview

This project builds Machine Learning models to classify suicide attempt cases by combining feature engineering, model comparison, and a scalable AWS-based data architecture.

## Project Contents

- `crisp_dm_mineria_sivigila.ipynb`: main analytics and modeling notebook.
- `Proyecto_Unificado_BigData_Mineria.md`: unified formal project document.
- `Big Data AWS/`: ETL scripts, SQL files, and AWS cost projection files.
- `Crispm Suicidios/`: CRISP-DM support documents.
- `output_mineria/`: model comparison outputs and experiment metadata.

## Methodology Summary

1. Feature engineering over clinical and sociodemographic variables.
2. Target definition and predictive feature selection.
3. Training and comparison of models: Logistic Regression, Decision Tree, Random Forest, and KNN.
4. Evaluation using classification metrics and confusion matrices.

## Technologies

- Python 3.10+
- Jupyter Notebook
- NumPy, Pandas
- Matplotlib, Seaborn
- Scikit-learn
- AWS Glue / Athena (scripts and SQL)

## Big Data Architecture (AWS)

- Bronze: raw data ingestion.
- Silver: cleaning and standardization.
- Gold: analytics-ready tables for querying and modeling.

## Local Execution

1. Create virtual environment:
   - Windows PowerShell: `python -m venv .venv`
2. Activate environment:
   - Windows PowerShell: `.\.venv\Scripts\Activate.ps1`
3. Install dependencies:
   - `pip install -r requirements.txt`
4. Open and run:
   - `crisp_dm_mineria_sivigila.ipynb`

## Data Notes

This repository excludes large datasets and temporary artifacts from version control to keep history clean. If you need to version large data files, use Git LFS or external storage (for example, S3).

## License

This project is distributed under the MIT license. See `LICENSE`.
