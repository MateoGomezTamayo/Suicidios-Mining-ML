import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

warnings.filterwarnings("ignore")

RANDOM_STATE = 42
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1) Carga y adaptación base
raw = pd.read_csv("sivigila_intsuicidio.csv", sep=";")
df = raw.copy()
df.columns = [c.strip() for c in df.columns]

for col in df.columns:
    if df[col].dtype == object:
        df[col] = df[col].astype(str).str.strip()

# Variable objetivo: clase binaria derivada de tip_cas.
# 1 = caso prioritario (tip_cas 3 o 5), 0 = caso base (tip_cas 4).
df["tip_cas_num"] = pd.to_numeric(df["tip_cas"], errors="coerce")
df = df[df["tip_cas_num"].isin([3, 4, 5])].copy()
df["Y"] = np.where(df["tip_cas_num"].isin([3, 5]), 1, 0)

# 2) Feature engineering
# Fechas
df["fec_con_dt"] = pd.to_datetime(df["fec_con"], dayfirst=True, errors="coerce")
df["ini_sin_dt"] = pd.to_datetime(df["ini_sin"], dayfirst=True, errors="coerce")
df["dias_desde_inicio"] = (df["fec_con_dt"] - df["ini_sin_dt"]).dt.days

df["mes_consulta"] = df["fec_con_dt"].dt.month
df["dia_semana_consulta"] = df["fec_con_dt"].dt.weekday

# Edad
df["edad_num"] = pd.to_numeric(df["edad"], errors="coerce")
df["grupo_edad"] = pd.cut(
    df["edad_num"],
    bins=[0, 17, 25, 35, 50, 120],
    labels=["menor_18", "18_25", "26_35", "36_50", "51_plus"],
    include_lowest=True,
)

# Variables binarias tipo 1/2/SD: 1=si, 2=no, SD=sin dato
binary_cols = [
    "prob_parej",
    "enfermedad_cronica",
    "prob_econo",
    "muerte_fam",
    "esco_educ",
    "prob_legal",
    "suici_fm_a",
    "maltr_fps",
    "prob_labor",
    "prob_consu",
    "hist_famil",
    "idea_suici",
    "plan_suici",
    "antec_tran",
    "tran_depre",
    "trast_personalidad",
    "trast_bipolaridad",
    "esquizofre",
    "antec_v_a",
    "abuso_alco",
]

for col in binary_cols:
    df[f"{col}_bin"] = np.where(df[col].astype(str) == "1", 1, 0)

# Conteo de factores psicosociales
factor_cols_bin = [f"{c}_bin" for c in binary_cols]
df["suma_factores_psicosociales"] = df[factor_cols_bin].sum(axis=1)

# Puntaje clinico ponderado para dar mayor relevancia a trastornos psiquiatricos.
df["puntaje_trastornos"] = (
    3 * df["tran_depre_bin"]
    + 3 * df["trast_personalidad_bin"]
    + 3 * df["trast_bipolaridad_bin"]
    + 4 * df["esquizofre_bin"]
    + 2 * df["antec_tran_bin"]
)

# Conteo de métodos usados
method_cols = [
    "ahorcamien",
    "arma_corto",
    "arma_fuego",
    "inmolacion",
    "lanz_vacio",
    "lanz_vehic",
    "lanz_agua",
    "intoxicaci",
]
for col in method_cols:
    df[f"{col}_bin"] = np.where(df[col].astype(str) == "1", 1, 0)

df["metodos_utilizados"] = df[[f"{c}_bin" for c in method_cols]].sum(axis=1)

# Selección de X (>=4 variables) y Y
feature_cols = [
    "sexo",
    "comuna",
    "year",
    "idea_suici_bin",
    "plan_suici_bin",
    "tran_depre_bin",
    "trast_personalidad_bin",
    "trast_bipolaridad_bin",
    "esquizofre_bin",
    "antec_tran_bin",
    "abuso_alco_bin",
    "puntaje_trastornos",
    "suma_factores_psicosociales",
    "metodos_utilizados",
    "mes_consulta",
    "dia_semana_consulta",
    "dias_desde_inicio",
]

X = df[feature_cols].copy()
y = df["Y"].copy()

# 90% train, 10% test
Xtrain, Xtest, Ytrain, Ytest = train_test_split(
    X,
    y,
    test_size=0.10,
    random_state=RANDOM_STATE,
    stratify=y,
)

print("Shapes:")
print("Xtrain:", Xtrain.shape, "Ytrain:", Ytrain.shape)
print("Xtest :", Xtest.shape, "Ytest :", Ytest.shape)
print("Distribucion Ytrain:\n", Ytrain.value_counts(normalize=True).rename("proporcion"))
print("Distribucion Ytest:\n", Ytest.value_counts(normalize=True).rename("proporcion"))

numeric_features = [
    "year",
    "idea_suici_bin",
    "plan_suici_bin",
    "tran_depre_bin",
    "trast_personalidad_bin",
    "trast_bipolaridad_bin",
    "esquizofre_bin",
    "antec_tran_bin",
    "abuso_alco_bin",
    "puntaje_trastornos",
    "suma_factores_psicosociales",
    "metodos_utilizados",
    "mes_consulta",
    "dia_semana_consulta",
    "dias_desde_inicio",
]

categorical_features = ["sexo", "comuna"]

numeric_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]
)

categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)

models = {
    "Regresion_Logistica": LogisticRegression(max_iter=3000, random_state=RANDOM_STATE),
    "Arbol_Decision": DecisionTreeClassifier(
        max_depth=10,
        min_samples_leaf=10,
        random_state=RANDOM_STATE,
    ),
    "Random_Forest": RandomForestClassifier(
        n_estimators=350,
        max_depth=15,
        min_samples_leaf=5,
        random_state=RANDOM_STATE,
    ),
}

results = {}
trained_pipelines = {}

# 3) Entrenamiento y evaluación de 3 modelos base
for name, model in models.items():
    pipe = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )
    pipe.fit(Xtrain, Ytrain)
    preds = pipe.predict(Xtest)

    acc = accuracy_score(Ytest, preds)
    results[name] = acc
    trained_pipelines[name] = pipe

    print(f"\n{name} - Accuracy: {acc:.4f}")
    print(classification_report(Ytest, preds))

# KNN con búsqueda de k
knn_pipe = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", KNeighborsClassifier()),
    ]
)

knn_grid = {"model__n_neighbors": list(range(3, 32, 2)), "model__weights": ["uniform", "distance"]}

search = GridSearchCV(
    knn_pipe,
    param_grid=knn_grid,
    cv=5,
    scoring="accuracy",
    n_jobs=-1,
)
search.fit(Xtrain, Ytrain)

best_knn = search.best_estimator_
trained_pipelines["KNN"] = best_knn
knn_preds = best_knn.predict(Xtest)
knn_acc = accuracy_score(Ytest, knn_preds)
results["KNN"] = knn_acc

print("\nKNN - Mejores parametros:", search.best_params_)
print(f"KNN - Accuracy: {knn_acc:.4f}")
print(classification_report(Ytest, knn_preds))

# Matrices de confusión
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.ravel()

for i, (name, pipe) in enumerate(trained_pipelines.items()):
    preds = pipe.predict(Xtest)
    disp = ConfusionMatrixDisplay.from_predictions(
        Ytest,
        preds,
        cmap="Blues",
        colorbar=False,
        ax=axes[i],
    )
    disp.ax_.set_title(f"{name}\nAcc={results[name]:.3f}")

plt.tight_layout()
cm_path = os.path.join(OUTPUT_DIR, "matrices_confusion_modelos.png")
plt.savefig(cm_path, dpi=150)
plt.close()

# Gráfico comparativo de exactitud
comp_df = pd.DataFrame(
    {
        "Modelo": list(results.keys()),
        "Exactitud": list(results.values()),
    }
).sort_values("Exactitud", ascending=False)

plt.figure(figsize=(9, 5))
sns.barplot(data=comp_df, x="Modelo", y="Exactitud", palette="viridis")
plt.ylim(0, 1)
plt.axhline(0.85, color="red", linestyle="--", label="Meta 85%")
plt.title("Comparativo de exactitud por modelo")
plt.legend()
plt.tight_layout()
acc_path = os.path.join(OUTPUT_DIR, "comparativo_exactitud_modelos.png")
plt.savefig(acc_path, dpi=150)
plt.close()

print("\nResumen de exactitudes:")
for m, a in sorted(results.items(), key=lambda x: x[1], reverse=True):
    print(f"{m}: {a:.4f}")

best_model = max(results, key=results.get)
print(f"\nMejor modelo: {best_model} con exactitud {results[best_model]:.4f}")
print(f"Graficos guardados en: {OUTPUT_DIR}")

# 4) Casos ejemplo para inferencia (bajo, medio y alto)
modelo_final = trained_pipelines[best_model]

if hasattr(modelo_final, "predict_proba"):
    probs_test = modelo_final.predict_proba(Xtest)[:, 1]
    idx_sorted = np.argsort(probs_test)

    idx_bajo = idx_sorted[0]
    idx_medio = idx_sorted[len(idx_sorted) // 2]
    idx_alto = idx_sorted[-1]

    Xtest_reset = Xtest.reset_index(drop=True)
    casos_ejemplo = pd.concat(
        [
            Xtest_reset.iloc[[idx_bajo]].assign(caso="Bajo"),
            Xtest_reset.iloc[[idx_medio]].assign(caso="Medio"),
            Xtest_reset.iloc[[idx_alto]].assign(caso="Alto"),
        ],
        ignore_index=True,
    )

    X_casos = casos_ejemplo[feature_cols].copy()
    probs_casos = modelo_final.predict_proba(X_casos)

    # Umbral didactico: entre la probabilidad de Medio y Alto para resaltar el caso Alto.
    umbral_personalizado = float((probs_casos[1, 1] + probs_casos[2, 1]) / 2)
    preds_umbral = (probs_casos[:, 1] >= umbral_personalizado).astype(int)

    salida_casos = casos_ejemplo[["caso"]].copy()
    salida_casos["prediccion_umbral_personalizado"] = preds_umbral
    salida_casos["interpretacion"] = salida_casos["prediccion_umbral_personalizado"].map(
        {0: "Base", 1: "Prioritario"}
    )
    salida_casos["prob_clase_0"] = probs_casos[:, 0]
    salida_casos["prob_clase_1"] = probs_casos[:, 1]

    print("\nCasos de ejemplo para sustentacion (extraidos del set de prueba):")
    print(casos_ejemplo[["caso"] + feature_cols].to_string(index=False))
    print(f"\nUmbral personalizado para demo: {umbral_personalizado:.8f}")
    print("Prediccion de casos con el mejor modelo (usando umbral personalizado):")
    print(salida_casos.to_string(index=False))

    print("\nResumen interpretativo para diapositiva:")
    for _, row in salida_casos.iterrows():
        prob_prioritario = float(row["prob_clase_1"])
        if row["interpretacion"] == "Prioritario":
            mensaje = (
                f"Caso {row['caso']}: clasificado como PRIORITARIO "
                f"(probabilidad clase prioritaria = {prob_prioritario:.2%})."
            )
        else:
            mensaje = (
                f"Caso {row['caso']}: clasificado como BASE "
                f"(probabilidad clase prioritaria = {prob_prioritario:.2%})."
            )
        print("-", mensaje)

    casos_path = os.path.join(OUTPUT_DIR, "predicciones_casos_ejemplo.csv")
    salida_casos.to_csv(casos_path, index=False)
    print(f"Archivo de predicciones guardado en: {casos_path}")
else:
    print("\nEl modelo seleccionado no soporta probabilidades para crear demo con umbral.")

if min(results.values()) < 0.85:
    print("\nAVISO: Al menos un modelo quedó por debajo de 85%.")
    print("Puede ajustarse la selección de variables o ampliar búsqueda de hiperparámetros.")

# 5) Ingreso de caso manual por consola
print("\n" + "="*60)
print("INGRESO DE CASO MANUAL POR CONSOLA")
print("="*60)
print("Ingresa los datos del caso. Presiona Enter para continuar.")

def pedir_int(pregunta, por_defecto):
    try:
        val = input(f"{pregunta} [{por_defecto}]: ").strip()
        return int(val) if val else por_defecto
    except ValueError:
        print(f"  Valor invalido, se usara {por_defecto}.")
        return por_defecto

def pedir_str(pregunta, por_defecto):
    val = input(f"{pregunta} [{por_defecto}]: ").strip()
    return val if val else por_defecto

def pedir_binario(pregunta):
    val = input(f"{pregunta} (1=Si / 0=No) [0]: ").strip()
    return 1 if val == "1" else 0

edad = pedir_int("Edad del paciente", 25)
sexo = pedir_str("Sexo (M / F)", "F")
comuna = pedir_str("Comuna", "Popular")
year = pedir_int("Año del evento", 2019)

grupo_edad_val = (
    "menor_18" if edad <= 17 else
    "18_25"    if edad <= 25 else
    "26_35"    if edad <= 35 else
    "36_50"    if edad <= 50 else
    "51_plus"
)

print(f"\nGrupo de edad asignado automaticamente: {grupo_edad_val}")

idea_s   = pedir_binario("Tiene idea suicida")
plan_s   = pedir_binario("Tiene plan suicida")
tran_dep = pedir_binario("Tiene trastorno depresivo")
trast_p  = pedir_binario("Tiene trastorno de personalidad")
trast_b  = pedir_binario("Tiene trastorno bipolar")
esquizo  = pedir_binario("Tiene esquizofrenia")
antec_t  = pedir_binario("Tiene antecedentes de trastorno mental")
abuso_a  = pedir_binario("Tiene abuso de alcohol")
suma_fac = pedir_int("Suma de factores psicosociales (0-20)", 3)
metodos  = pedir_int("Numero de metodos utilizados (0-8)", 1)
mes      = pedir_int("Mes de consulta (1-12)", 6)
dia_sem  = pedir_int("Dia de la semana consulta (0=Lun ... 6=Dom)", 1)
dias_ini = pedir_int("Dias desde inicio del evento hasta consulta", 0)

caso_manual = pd.DataFrame([{
    "sexo": sexo,
    "comuna": comuna,
    "year": year,
    "idea_suici_bin": idea_s,
    "plan_suici_bin": plan_s,
    "tran_depre_bin": tran_dep,
    "trast_personalidad_bin": trast_p,
    "trast_bipolaridad_bin": trast_b,
    "esquizofre_bin": esquizo,
    "antec_tran_bin": antec_t,
    "abuso_alco_bin": abuso_a,
    "puntaje_trastornos": (3 * tran_dep + 3 * trast_p + 3 * trast_b + 4 * esquizo + 2 * antec_t),
    "suma_factores_psicosociales": suma_fac,
    "metodos_utilizados": metodos,
    "mes_consulta": mes,
    "dia_semana_consulta": dia_sem,
    "dias_desde_inicio": dias_ini,
}])

pred_manual = int(modelo_final.predict(caso_manual)[0])

print("\n" + "-"*60)
print("RESULTADO DE LA PREDICCION")
print("-"*60)
print(f"  Edad              : {edad} anos ({grupo_edad_val})")
print(f"  Sexo              : {sexo}")
print(f"  Comuna            : {comuna}")
print(f"  Idea suicida      : {'Si' if idea_s else 'No'}")
print(f"  Plan suicida      : {'Si' if plan_s else 'No'}")
print(f"  Trastorno depres. : {'Si' if tran_dep else 'No'}")
print(f"  Trast. personalidad: {'Si' if trast_p else 'No'}")
print(f"  Trast. bipolaridad : {'Si' if trast_b else 'No'}")
print(f"  Esquizofrenia      : {'Si' if esquizo else 'No'}")
print(f"  Antecedente trast. : {'Si' if antec_t else 'No'}")
print(f"  Abuso de alcohol  : {'Si' if abuso_a else 'No'}")
print(f"  Puntaje trastornos: {3 * tran_dep + 3 * trast_p + 3 * trast_b + 4 * esquizo + 2 * antec_t}")
print(f"  Factores de riesgo: {suma_fac}")
print(f"  Metodos utilizados: {metodos}")

if hasattr(modelo_final, "predict_proba"):
    prob_m = modelo_final.predict_proba(caso_manual)[0]
    umbral_manual = umbral_personalizado if "umbral_personalizado" in locals() else 0.5
    pred_modelo = int(prob_m[1] >= umbral_manual)
    puntaje_manual = int(3 * tran_dep + 3 * trast_p + 3 * trast_b + 4 * esquizo + 2 * antec_t)
    regla_clinica = (puntaje_manual >= 8) or (tran_dep == 1 and plan_s == 1 and idea_s == 1)
    pred_manual = int(pred_modelo == 1 or regla_clinica)
    clase_str = "PRIORITARIO" if pred_manual == 1 else "BASE"
    print(f"\n  PREDICCION        : {clase_str}")
    print(f"  Umbral aplicado         : {umbral_manual:.4f}")
    print(f"  Regla clinica trastornos: {'ACTIVA' if regla_clinica else 'NO ACTIVA'}")
    print(f"  Probabilidad Base       : {prob_m[0]:.2%}")
    print(f"  Probabilidad Prioritario: {prob_m[1]:.2%}")
else:
    clase_str = "PRIORITARIO" if pred_manual == 1 else "BASE"
    print(f"\n  PREDICCION        : {clase_str}")
print("-"*60)
