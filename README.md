#  Clasificación de Intentos de Suicidio

Autores
Mateo Gómez Tamayo
Lorenzo Vargas


# Descripción del Proyecto

Este proyecto consiste en el desarrollo de un modelo de Machine Learning para la clasificación de casos de intento de suicidio, utilizando datos del sistema SIVIGILA
- El objetivo principal es transformar variables clínicas y sociodemográficas mediante Feature Engineering para predecir con precisión la clase de cada caso, facilitando la toma de decisiones en salud pública

# Dataset
Se trabajó con un conjunto de datos que contiene:
13.699 registros y 46 variables iniciales

Información detallada sobre edad, sexo, ubicación (comuna), antecedentes clínicos y factores de riesgo psicosocial

# Metodología
# 1. Feature Engineering (Ingeniería de Variables)
Se realizaron transformaciones clave para mejorar la capacidad predictiva de los modelos, tales como
:
Transformación de fechas y edades: Ajuste de formatos y categorización.
Variables Agregadas: Creación de indicadores como la "Suma de factores psicosociales" y "Métodos utilizados".
Codificación: Ajuste de variables tipo 1/2/SD para su procesamiento numérico.


 # 3. Configuración del Modelo
Variable Objetivo (Y): Definida de forma binaria a partir de la columna tip_cas
.
Variables Predictoras (X): Selección de 14 variables determinantes
.
División de Datos: Partición de 90% para entrenamiento y 10% para prueba

.
# 4. Modelos Entrenados
Se implementaron y compararon cuatro algoritmos de clasificación
:
Regresión Logística
Árbol de Decisión
Random Forest
K-Nearest Neighbors (KNN): Optimizado mediante GridSearchCV para encontrar el valor ideal de k
.
Resultados y Evaluación
Desempeño: Los modelos alcanzaron una exactitud (accuracy) superior al 85% (con picos reportados del 99% según la configuración final)
.
Herramientas de Análisis: Se utilizaron matrices de confusión para evaluar los aciertos y errores por clase, complementando métricas de precisión y recall
.
Casos de Aplicación Práctica
El sistema fue validado mediante un caso hipotético evaluando tres escenarios (Bajo, Medio y Alto riesgo), permitiendo interpretar las probabilidades de predicción en un lenguaje comprensible para entornos reales de atención médica
.
Conclusiones
El flujo de trabajo permitió demostrar que la ingeniería de variables y la comparación de modelos robustos son fundamentales para el análisis de datos de salud pública
. Como recomendación futura, se sugiere optimizar el tratamiento del desbalance de clases para mejorar la detección en la clase minoritaria
.
