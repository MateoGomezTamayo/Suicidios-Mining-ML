import sys
from pyspark.context import SparkContext
from pyspark.sql import functions as F
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions

# Glue requiere JOB_NAME como argumento del job
args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext.getOrCreate()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

job = Job(glue_context)
job.init(args["JOB_NAME"], args)

# Dataset real reportado por el usuario
input_path = "s3://datalake-bronze-039781381637/sales/sivigila_intsuicidio.csv"
output_path = "s3://datalake-silver-039781381637/sales/sivigila_intsuicidio/"

# Detecta el separador real de la cabecera para evitar leer todo en una sola columna.
header_line = sc.textFile(input_path, minPartitions=1).first()
delimiters = [";", ",", "|", "\t"]
sep = max(delimiters, key=lambda d: header_line.count(d))
print(f"Separador detectado: '{sep}'")

# 1) Leer Bronze en CSV
# Usa el separador detectado en la cabecera.
df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "false")
    .option("sep", sep)
    .csv(input_path)
)

if len(df.columns) == 1:
    raise ValueError(
        "El archivo se leyo con 1 sola columna. Verifica separador, comillas y formato del CSV en Bronze."
    )

rows_input = df.count()

# 2) Normalizar nombres de columnas (lower + trim + espacios a guion bajo)
for c in df.columns:
    new_c = c.strip().lower().replace(" ", "_")
    if c != new_c:
        df = df.withColumnRenamed(c, new_c)

# 3) Limpieza general en columnas string
# Reglas: trim y marcadores sin valor -> null
invalid_markers = ["", "null", "none", "na", "n/a", "nan", "-", "sin_dato", "no_aplica"]
for c, t in df.dtypes:
    if t == "string":
        cleaned = F.trim(F.col(c))
        df = df.withColumn(
            c,
            F.when(F.lower(cleaned).isin(invalid_markers), F.lit(None)).otherwise(cleaned)
        )

# 4) Limpieza de columnas numéricas comunes (si existen)
for numeric_col in ["amount", "cantidad", "edad", "valor"]:
    if numeric_col in df.columns:
        numeric_value = F.regexp_replace(F.col(numeric_col).cast("string"), ",", ".").cast("double")
        df = df.withColumn(
            numeric_col,
            F.when((numeric_value.isNull()) | (numeric_value < 0), F.lit(None)).otherwise(numeric_value)
        )

# 5) Eliminar filas totalmente nulas
df = df.dropna(how="all")

# 6) Eliminar duplicados
df = df.dropDuplicates()

# 7) Eliminar nulos en columnas críticas si existen
# Para este dataset no forzamos amount; solo columnas que realmente existan.
critical_columns = [c for c in ["id", "edad", "sexo", "year"] if c in df.columns]
if critical_columns:
    df = df.dropna(subset=critical_columns)

rows_output = df.count()
print(f"Registros de entrada: {rows_input}")
print(f"Registros de salida : {rows_output}")
print(f"Registros removidos : {rows_input - rows_output}")

if rows_output == 0:
    raise ValueError("La salida quedo en 0 registros despues de la limpieza. Revisa reglas y columnas criticas.")

# 8) Escribir en Silver en formato Parquet (1 solo archivo de salida)
(
    df.coalesce(1)
    .write
    .mode("overwrite")
    .parquet(output_path)
)

job.commit()
