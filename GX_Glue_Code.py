import sys
from pyspark.context import SparkContext
from pyspark.sql import functions as F
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions

# -----------------------------------
# 🔧 Inicializar Glue
# -----------------------------------
args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# -----------------------------------
# Leer datos (S3)
# -----------------------------------
raw_df = (
    spark.read
    .option("header", True)
    .option("sep", ";")
    .csv("s3://datalake-bronze-039781381637/sales/sivigila_intsuicidio.csv")
)

df = (
    raw_df
    .withColumn("id", F.col("id").cast("int"))
    .withColumn("edad", F.col("edad").cast("int"))
    .withColumn("year", F.col("year").cast("int"))
    .withColumn("sexo", F.upper(F.trim(F.col("sexo"))))
    .withColumn("evento", F.trim(F.col("evento")))
    .withColumn("tip_cas", F.trim(F.col("tip_cas")))
)

# -----------------------------------
# Validaciones de expectativas (nativas Spark)
# -----------------------------------
total_rows = df.count()
expectation_results = []


def add_expectation(name, is_success):
    expectation_results.append({"expectation": name, "success": bool(is_success)})


def ratio(valid_count, all_count):
    if all_count == 0:
        return 0.0
    return float(valid_count) / float(all_count)


# 1) El dataset debe contener registros
add_expectation("row_count_greater_than_zero", total_rows >= 1)

# 2) id no nulo
id_not_null_count = df.filter(F.col("id").isNotNull()).count()
add_expectation("id_not_null_100", ratio(id_not_null_count, total_rows) >= 1.0)

# 3) id unico
distinct_id_count = df.select("id").distinct().count()
add_expectation("id_unique", distinct_id_count == total_rows)

# 4) edad no nula (>= 99%)
edad_not_null_count = df.filter(F.col("edad").isNotNull()).count()
add_expectation("edad_not_null_99pct", ratio(edad_not_null_count, total_rows) >= 0.99)

# 5) edad en rango [0,120] (>= 99%)
edad_valid_count = df.filter(F.col("edad").between(0, 120)).count()
add_expectation("edad_between_0_120_99pct", ratio(edad_valid_count, total_rows) >= 0.99)

# 6) sexo en {F,M} (>= 99%)
sexo_valid_count = df.filter(F.col("sexo").isin("F", "M")).count()
add_expectation("sexo_in_set_F_M_99pct", ratio(sexo_valid_count, total_rows) >= 0.99)

# 7) year no nulo (100%)
year_not_null_count = df.filter(F.col("year").isNotNull()).count()
add_expectation("year_not_null_100", ratio(year_not_null_count, total_rows) >= 1.0)

# 8) year en rango [2010,2030] (100%)
year_valid_count = df.filter(F.col("year").between(2010, 2030)).count()
add_expectation("year_between_2010_2030_100", ratio(year_valid_count, total_rows) >= 1.0)

# 9) evento esperado (>= 99%)
evento_valid_count = df.filter(F.col("evento") == "INTENTO DE SUICIDIO").count()
add_expectation("evento_intento_suicidio_99pct", ratio(evento_valid_count, total_rows) >= 0.99)

# 10) tip_cas en {1,2,3,4,5} (>= 99%)
tip_valid_count = df.filter(F.col("tip_cas").isin("1", "2", "3", "4", "5")).count()
add_expectation("tip_cas_in_set_99pct", ratio(tip_valid_count, total_rows) >= 0.99)

successful_expectations = sum(1 for e in expectation_results if e["success"])
all_success = successful_expectations == 10

print("===== RESULTADOS EXPECTATIVAS DQ =====")
for result in expectation_results:
    print(f"{result['expectation']}: {result['success']}")

print(
    f"Expectativas evaluadas: 10 | "
    f"Exitosas: {successful_expectations} | "
    f"Success global: {all_success}"
)

# -----------------------------------
# Control de fallo (MUY IMPORTANTE)
# -----------------------------------
if not all_success:
    failed = [e["expectation"] for e in expectation_results if not e["success"]]
    raise Exception(f"Data Quality FAILED: no se cumplieron todas las expectativas. Fallaron: {failed}")

job.commit()