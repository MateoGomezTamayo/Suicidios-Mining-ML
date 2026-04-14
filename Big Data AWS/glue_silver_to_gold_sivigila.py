import sys
from pyspark.context import SparkContext
from pyspark.sql import functions as F
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions

args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext.getOrCreate()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

job = Job(glue_context)
job.init(args["JOB_NAME"], args)

input_path  = "s3://datalake-silver-039781381637/sales/sivigila_intsuicidio/"
output_gold_resumen  = "s3://datalake-gold-039781381637/sales/sivigila_resumen_comuna/"
output_gold_riesgo   = "s3://datalake-gold-039781381637/sales/sivigila_perfil_riesgo/"

# ─────────────────────────────────────────
# Leer Silver (Parquet)
# ─────────────────────────────────────────
df = spark.read.parquet(input_path)

print(f"Columnas disponibles: {df.columns}")
print(f"Registros leidos desde Silver: {df.count()}")

# ─────────────────────────────────────────
# TRANSFORMACIÓN 1
# Resumen epidemiológico por comuna y año
# Responde: ¿en qué zonas y años hay más casos?
#           ¿qué proporción requirió hospitalización?
# ─────────────────────────────────────────
# pac_hos indica si el paciente fue hospitalizado (1 = sí)
pac_hos_num = F.col("pac_hos").cast("int")

df_resumen = (
    df.groupBy("comuna", "year")
    .agg(
        F.count("*").alias("total_casos"),
        F.sum(pac_hos_num).alias("total_hospitalizados"),
        F.round(
            F.sum(pac_hos_num) / F.count("*") * 100, 2
        ).alias("pct_hospitalizados"),
        F.avg(F.col("edad").cast("double")).alias("edad_promedio"),
        F.sum(F.when(F.col("sexo") == "1", 1).otherwise(0)).alias("casos_masculino"),
        F.sum(F.when(F.col("sexo") == "2", 1).otherwise(0)).alias("casos_femenino"),
    )
    .orderBy("year", "comuna")
)

(
    df_resumen.coalesce(1)
    .write
    .mode("overwrite")
    .parquet(output_gold_resumen)
)
print("Transformacion 1 guardada: resumen por comuna y año")

# ─────────────────────────────────────────
# TRANSFORMACIÓN 2
# Perfil de riesgo individual
# Crea columna nueva: puntaje_riesgo = suma de todos
# los factores de riesgo presentes en el registro.
# Clasifica en: bajo / medio / alto
# ─────────────────────────────────────────
# Columnas de factores de riesgo presentes en el dataset
risk_cols = [
    "prob_parej",       # problemas de pareja
    "enfermedad_cronica",
    "prob_econo",       # problemas económicos
    "muerte_fam",       # muerte de familiar
    "prob_legal",       # problemas legales
    "prob_labor",       # problemas laborales
    "prob_consu",       # consumo de sustancias
    "hist_famil",       # historia familiar de suicidio
    "idea_suici",       # ideación suicida previa
    "plan_suici",       # plan suicida previo
    "antec_tran",       # antecedentes de trastorno
    "tran_depre",       # trastorno depresivo
    "trast_personalidad",
    "trast_bipolaridad",
    "esquizofre",
    "abuso_alco",       # abuso de alcohol
    "maltr_fps",        # maltrato físico/psicológico
    "antec_v_a",        # antecedentes de violencia
]

# Solo suma los que realmente existen en el DataFrame
existing_risk_cols = [c for c in risk_cols if c in df.columns]

# Suma de factores: cada columna binaria vale 1 si es "1" o 1
puntaje_expr = sum(
    F.coalesce(F.col(c).cast("int"), F.lit(0))
    for c in existing_risk_cols
)

df_riesgo = df.withColumn("puntaje_riesgo", puntaje_expr)

# Clasificación según puntaje
df_riesgo = df_riesgo.withColumn(
    "nivel_riesgo",
    F.when(F.col("puntaje_riesgo") <= 2, "bajo")
     .when(F.col("puntaje_riesgo") <= 5, "medio")
     .otherwise("alto")
)

# Método del intento más frecuente por nivel de riesgo (columna informativa adicional)
metodos = ["ahorcamien", "arma_corto", "arma_fuego", "inmolacion",
           "lanz_vacio", "lanz_vehic", "lanz_agua", "intoxicaci"]
existing_metodos = [c for c in metodos if c in df.columns]

# Columna con el primer método activo encontrado por registro
metodo_expr = F.lit("no_especificado")
for m in reversed(existing_metodos):
    metodo_expr = F.when(F.col(m).cast("int") == 1, F.lit(m)).otherwise(metodo_expr)

df_riesgo = df_riesgo.withColumn("metodo_intento", metodo_expr)

# Selección final de columnas relevantes para Gold
cols_output = (
    ["id", "edad", "sexo", "comuna", "year",
     "nivel_riesgo", "puntaje_riesgo", "metodo_intento",
     "intentos", "pac_hos", "inten_prev"]
    + [c for c in ["gp_psiquia", "psiquiatri", "trab_socia"] if c in df.columns]
)
cols_output = [c for c in cols_output if c in df_riesgo.columns]

(
    df_riesgo.select(cols_output)
    .coalesce(1)
    .write
    .mode("overwrite")
    .parquet(output_gold_riesgo)
)
print("Transformacion 2 guardada: perfil de riesgo individual")

job.commit()
