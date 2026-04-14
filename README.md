# Suicidios Mining ML

Proyecto de Big Data y Mineria de Datos para analizar registros de intento de suicidio (SIVIGILA), integrando una arquitectura de datos en AWS (Bronze/Silver/Gold) con un flujo CRISP-DM para modelado de riesgo.

## Autor

- Mateo Gomez Tamayo

## Descripcion general

El proyecto desarrolla modelos de Machine Learning para clasificacion de casos de intento de suicidio, combinando ingenieria de variables, comparacion de algoritmos y una arquitectura de datos escalable en AWS.

## Contenido del proyecto

- `crisp_dm_mineria_sivigila.ipynb`: notebook principal de analitica y modelado.
- `Proyecto_Unificado_BigData_Mineria.md`: documento unificado del anteproyecto.
- `Big Data AWS/`: scripts ETL, SQL y archivos de costeo en AWS.
- `Crispm Suicidios/`: documentos de apoyo CRISP-DM.
- `output_mineria/`: salidas de comparacion de modelos y metadatos del experimento.

## Metodologia resumida

1. Feature engineering sobre variables clinicas y sociodemograficas.
2. Definicion de variable objetivo y seleccion de variables predictoras.
3. Entrenamiento y comparacion de modelos: Regresion Logistica, Arbol de Decision, Random Forest y KNN.
4. Evaluacion con metricas de clasificacion y matrices de confusion.

## Tecnologias usadas

- Python 3.10+
- Jupyter Notebook
- NumPy, Pandas
- Matplotlib, Seaborn
- Scikit-learn
- AWS Glue / Athena (scripts y SQL)

## Estructura Big Data (AWS)

- Bronze: ingesta de datos crudos.
- Silver: limpieza y estandarizacion.
- Gold: tablas analiticas para consulta y modelado.

## Ejecucion local

1. Crear entorno virtual:
   - Windows PowerShell: `python -m venv .venv`
2. Activar entorno:
   - Windows PowerShell: `.\.venv\Scripts\Activate.ps1`
3. Instalar dependencias:
   - `pip install -r requirements.txt`
4. Abrir y ejecutar:
   - `crisp_dm_mineria_sivigila.ipynb`

## Notas sobre datos

Este repositorio excluye datasets grandes y artefactos temporales del control de versiones para mantener el historial limpio. Si necesitas versionar archivos de datos pesados, se recomienda Git LFS o almacenamiento externo (por ejemplo S3).

## Licencia

Este proyecto se distribuye bajo licencia MIT. Ver `LICENSE`.
