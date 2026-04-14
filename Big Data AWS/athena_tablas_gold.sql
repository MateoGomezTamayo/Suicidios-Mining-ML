-- =========================================================
-- ATHENA DDL + CONSULTAS - Pipeline SIVIGILA
-- IMPORTANTE: Ejecutar CADA bloque por separado en Athena.
--             Athena solo permite UNA sentencia por ejecucion.
-- =========================================================


-- ─────────────────────────────────────────────────────────
-- PASO 1A: Crear tabla gold_sales_metrics
-- >> Seleccionar solo este bloque y ejecutar
-- ─────────────────────────────────────────────────────────
CREATE EXTERNAL TABLE IF NOT EXISTS gold_sales_metrics (
    city        STRING,
    total_sales DOUBLE,
    num_orders  INT
)
STORED AS PARQUET
LOCATION 's3://datalake-gold-039781381637/sales_metrics/'


-- ─────────────────────────────────────────────────────────
-- PASO 1B: Consultar gold_sales_metrics
-- >> Seleccionar solo este bloque y ejecutar
-- ─────────────────────────────────────────────────────────
SELECT *
FROM gold_sales_metrics
LIMIT 10


-- ─────────────────────────────────────────────────────────
-- PASO 2A: Crear tabla sivigila_resumen_comuna
-- >> Seleccionar solo este bloque y ejecutar
-- ─────────────────────────────────────────────────────────
CREATE EXTERNAL TABLE IF NOT EXISTS sivigila_resumen_comuna (
    comuna                STRING,
    year                  STRING,
    total_casos           BIGINT,
    total_hospitalizados  BIGINT,
    pct_hospitalizados    DOUBLE,
    edad_promedio         DOUBLE,
    casos_masculino       BIGINT,
    casos_femenino        BIGINT
)
STORED AS PARQUET
LOCATION 's3://datalake-gold-039781381637/sales/sivigila_resumen_comuna/'


-- ─────────────────────────────────────────────────────────
-- PASO 2B: Consultar sivigila_resumen_comuna
-- >> Seleccionar solo este bloque y ejecutar
-- ─────────────────────────────────────────────────────────
SELECT *
FROM sivigila_resumen_comuna
LIMIT 10


-- ─────────────────────────────────────────────────────────
-- PASO 3A: Crear tabla sivigila_perfil_riesgo
-- >> Seleccionar solo este bloque y ejecutar
-- ─────────────────────────────────────────────────────────
CREATE EXTERNAL TABLE IF NOT EXISTS sivigila_perfil_riesgo (
    id              STRING,
    edad            DOUBLE,
    sexo            STRING,
    comuna          STRING,
    year            STRING,
    nivel_riesgo    STRING,
    puntaje_riesgo  INT,
    metodo_intento  STRING,
    intentos        STRING,
    pac_hos         STRING,
    inten_prev      STRING,
    gp_psiquia      STRING,
    psiquiatri      STRING,
    trab_socia      STRING
)
STORED AS PARQUET
LOCATION 's3://datalake-gold-039781381637/sales/sivigila_perfil_riesgo/'


-- ─────────────────────────────────────────────────────────
-- PASO 3B: Consultar sivigila_perfil_riesgo
-- >> Seleccionar solo este bloque y ejecutar
-- ─────────────────────────────────────────────────────────
SELECT *
FROM sivigila_perfil_riesgo
LIMIT 10
