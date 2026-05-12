#!/usr/bin/env python3
"""
openmetadata_lineage.py
=======================
Registra en OpenMetadata el linaje completo del pipeline SIVIGILA:

    Bronze S3 (CSV)
        |  [Glue: datalake-dev-sivigila-etl]
        v
    Silver S3 (Parquet)
        |  [Athena external table sobre Silver]
        v
    Athena: sivigila_silver_parquet
        |  [Glue: datalake-dev-sivigila-gold-etl]
        v
    Gold S3 (Parquet - resumen_comuna / perfil_riesgo)

Uso local (con OpenMetadata corriendo en Docker):
    python openmetadata_lineage.py

Uso con instancia remota:
    python openmetadata_lineage.py --host https://mi-om.empresa.com --token <JWT>

Uso con usuario/contraseña personalizada:
    python openmetadata_lineage.py --host http://localhost:8585 \\
        --email admin@open-metadata.org --password admin
"""

import argparse
import json
import sys
import time

import requests

# ─────────────────────────────────────────────────────────────────────────────
# Configuración del pipeline (coincide con variables del workflow de CI)
# ─────────────────────────────────────────────────────────────────────────────
ACCOUNT_ID    = "039781381637"
REGION        = "us-east-1"

BRONZE_BUCKET = f"datalake-dev-raw-{ACCOUNT_ID}"
SILVER_BUCKET = f"datalake-dev-silver-{ACCOUNT_ID}"
GOLD_BUCKET   = f"datalake-dev-gold-{ACCOUNT_ID}"

JOB_BRONZE_SILVER = "datalake-dev-sivigila-etl"
JOB_SILVER_GOLD   = "datalake-dev-sivigila-gold-etl"

STORAGE_SERVICE_NAME = "S3-Datalake-AWS"
ATHENA_SERVICE_NAME  = "Athena-Datalake-AWS"
ATHENA_DB_NAME       = "sivigila_db"
ATHENA_SCHEMA_NAME   = "default"


# ─────────────────────────────────────────────────────────────────────────────
# Cliente OpenMetadata (REST API)
# ─────────────────────────────────────────────────────────────────────────────
class OpenMetadataClient:
    def __init__(self, host: str, email: str, password: str, token: str = None):
        self.host = host.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept":       "application/json",
        })
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
            print(f"[AUTH] Usando token JWT proporcionado")
        else:
            self._login(email, password)

    def _login(self, email: str, password: str) -> None:
        resp = self.session.post(
            f"{self.host}/api/v1/users/login",
            json={"email": email, "password": password},
            timeout=30,
        )
        if not resp.ok:
            raise RuntimeError(
                f"Login fallido ({resp.status_code}): {resp.text[:200]}"
            )
        token = resp.json()["accessToken"]
        self.session.headers["Authorization"] = f"Bearer {token}"
        print(f"[AUTH] Login exitoso como {email}")

    def _put(self, path: str, payload: dict) -> dict:
        resp = self.session.put(
            f"{self.host}{path}",
            json=payload,
            timeout=30,
        )
        if not resp.ok:
            raise RuntimeError(
                f"PUT {path} -> {resp.status_code}: {resp.text[:400]}"
            )
        return resp.json()

    def _get_by_fqn(self, entity_path: str, fqn: str) -> dict | None:
        """Obtiene una entidad por su FQN; retorna None si no existe."""
        resp = self.session.get(
            f"{self.host}/api/v1/{entity_path}/name/{fqn}",
            timeout=30,
        )
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()

    # ── Servicios ─────────────────────────────────────────────────────────────

    def upsert_storage_service(self, name: str, description: str) -> dict:
        payload = {
            "name":        name,
            "description": description,
            "serviceType": "S3",
            "connection": {
                "config": {
                    "type":      "S3",
                    "awsConfig": {"awsRegion": REGION},
                }
            },
        }
        entity = self._put("/api/v1/services/storageServices", payload)
        print(f"  [STORAGE-SVC] '{name}'  id={entity['id']}")
        return entity

    def upsert_database_service(self, name: str, description: str) -> dict:
        payload = {
            "name":        name,
            "description": description,
            "serviceType": "Athena",
            "connection": {
                "config": {
                    "type":         "Athena",
                    "awsConfig":    {"awsRegion": REGION},
                    "s3StagingDir": f"s3://{GOLD_BUCKET}/athena-results/",
                    "workgroup":    "primary",
                }
            },
        }
        entity = self._put("/api/v1/services/databaseServices", payload)
        print(f"  [DB-SVC] '{name}'  id={entity['id']}")
        return entity

    # ── Contenedores S3 ───────────────────────────────────────────────────────

    def upsert_container(
        self,
        service_fqn: str,
        name: str,
        description: str,
        s3_path: str,
    ) -> dict:
        payload = {
            "name":        name,
            "description": description,
            "service":     service_fqn,
            "fullPath":    s3_path,
        }
        entity = self._put("/api/v1/containers", payload)
        print(f"  [CONTAINER] '{name}'  id={entity['id']}")
        return entity

    # ── Entidades Athena ──────────────────────────────────────────────────────

    def upsert_database(self, service_fqn: str, name: str, description: str) -> dict:
        payload = {
            "name":        name,
            "description": description,
            "service":     service_fqn,
        }
        entity = self._put("/api/v1/databases", payload)
        print(f"  [DATABASE] '{name}'  id={entity['id']}")
        return entity

    def upsert_schema(self, database_fqn: str, name: str) -> dict:
        payload = {
            "name":     name,
            "database": database_fqn,
        }
        entity = self._put("/api/v1/databaseSchemas", payload)
        print(f"  [SCHEMA] '{name}'  id={entity['id']}")
        return entity

    def upsert_table(
        self,
        schema_fqn:  str,
        name:        str,
        description: str,
        columns:     list[dict],
        location:    str,
    ) -> dict:
        payload = {
            "name":           name,
            "description":    description,
            "tableType":      "External",
            "databaseSchema": schema_fqn,
            "columns":        columns,
            "tableConstraints": [],
            "location":       location,
        }
        entity = self._put("/api/v1/tables", payload)
        print(f"  [TABLE] '{name}'  id={entity['id']}")
        return entity

    # ── Linaje ────────────────────────────────────────────────────────────────

    def add_lineage(
        self,
        from_id:   str,
        from_type: str,
        from_name: str,
        to_id:     str,
        to_type:   str,
        to_name:   str,
        description: str = "",
    ) -> None:
        payload = {
            "edge": {
                "fromEntity": {"id": from_id, "type": from_type},
                "toEntity":   {"id": to_id,   "type": to_type},
                "lineageDetails": {
                    "description":  description,
                    "columnsLineage": [],
                },
            }
        }
        self._put("/api/v1/lineage", payload)
        print(f"  [LINEAGE] {from_name} ({from_type}) --> {to_name} ({to_type})")


# ─────────────────────────────────────────────────────────────────────────────
# Definición de columnas (Athena Silver table)
# ─────────────────────────────────────────────────────────────────────────────
SILVER_COLUMNS = [
    {"name": "cod_ase",        "dataType": "STRING",  "description": "Codigo asegurador"},
    {"name": "tipo_id",        "dataType": "STRING",  "description": "Tipo de identificacion"},
    {"name": "id",             "dataType": "STRING",  "description": "Identificador anonimizado del paciente"},
    {"name": "fec_not",        "dataType": "STRING",  "description": "Fecha de notificacion"},
    {"name": "age",            "dataType": "STRING",  "description": "Grupo etario"},
    {"name": "edad",           "dataType": "DOUBLE",  "description": "Edad del paciente (anios)"},
    {"name": "sexo",           "dataType": "STRING",  "description": "Sexo: 1=masculino, 2=femenino"},
    {"name": "comuna",         "dataType": "STRING",  "description": "Codigo de comuna de residencia"},
    {"name": "year",           "dataType": "STRING",  "description": "Anio de notificacion"},
    {"name": "pac_hos",        "dataType": "STRING",  "description": "Paciente hospitalizado (1=Si, 0=No)"},
    {"name": "inten_prev",     "dataType": "STRING",  "description": "Intento previo de suicidio"},
    {"name": "gp_psiquia",     "dataType": "STRING",  "description": "Grupo psiquiatrico"},
    {"name": "psiquiatri",     "dataType": "STRING",  "description": "Seguimiento psiquiatrico"},
    {"name": "trab_socia",     "dataType": "STRING",  "description": "Trabajo social"},
    {"name": "metodo_intento", "dataType": "STRING",  "description": "Metodo del intento"},
    {"name": "nivel_riesgo",   "dataType": "STRING",  "description": "Nivel de riesgo clasificado"},
    {"name": "puntaje_riesgo", "dataType": "INT",     "description": "Puntaje de riesgo calculado"},
]


# ─────────────────────────────────────────────────────────────────────────────
# Flujo principal
# ─────────────────────────────────────────────────────────────────────────────
def main(host: str, email: str, password: str, token: str) -> int:
    print("=" * 65)
    print("  REGISTRO DE LINAJE SIVIGILA EN OPENMETADATA")
    print(f"  Host: {host}")
    print("=" * 65)

    try:
        client = OpenMetadataClient(host, email, password, token)
    except Exception as exc:
        print(f"\n[ERROR] No se pudo conectar a OpenMetadata: {exc}")
        print("  Verifica que OpenMetadata este corriendo:")
        print("    cd openmetadata && docker compose up -d")
        return 1

    # ── 1. Servicio S3 ────────────────────────────────────────────────────────
    print("\n[1/4] Registrando servicio S3 y buckets...")
    svc_s3 = client.upsert_storage_service(
        name=STORAGE_SERVICE_NAME,
        description="Servicio S3 AWS - Datalake pipeline SIVIGILA",
    )
    svc_s3_fqn = svc_s3["fullyQualifiedName"]

    bronze = client.upsert_container(
        service_fqn=svc_s3_fqn,
        name=BRONZE_BUCKET,
        description=(
            "Bronze layer — datos crudos SIVIGILA en CSV. "
            "Fuente: SIVIGILA (intentos de suicidio, Antioquia)."
        ),
        s3_path=f"s3://{BRONZE_BUCKET}",
    )

    silver = client.upsert_container(
        service_fqn=svc_s3_fqn,
        name=SILVER_BUCKET,
        description=(
            "Silver layer — datos SIVIGILA limpios y normalizados en Parquet. "
            f"Producido por Glue job '{JOB_BRONZE_SILVER}'."
        ),
        s3_path=f"s3://{SILVER_BUCKET}/sivigila/",
    )

    gold = client.upsert_container(
        service_fqn=svc_s3_fqn,
        name=GOLD_BUCKET,
        description=(
            "Gold layer — tablas agregadas SIVIGILA en Parquet: "
            "resumen_comuna y perfil_riesgo. "
            f"Producido por Glue job '{JOB_SILVER_GOLD}'."
        ),
        s3_path=f"s3://{GOLD_BUCKET}",
    )

    # ── 2. Servicio Athena + tabla Silver ─────────────────────────────────────
    print("\n[2/4] Registrando servicio Athena y tabla Silver...")
    svc_athena = client.upsert_database_service(
        name=ATHENA_SERVICE_NAME,
        description="Amazon Athena sobre datalake SIVIGILA (us-east-1)",
    )
    svc_athena_fqn = svc_athena["fullyQualifiedName"]

    db = client.upsert_database(
        service_fqn=svc_athena_fqn,
        name=ATHENA_DB_NAME,
        description="Base de datos Athena para datos SIVIGILA",
    )
    db_fqn = db["fullyQualifiedName"]

    schema = client.upsert_schema(
        database_fqn=db_fqn,
        name=ATHENA_SCHEMA_NAME,
    )
    schema_fqn = schema["fullyQualifiedName"]

    table_silver = client.upsert_table(
        schema_fqn=schema_fqn,
        name="sivigila_silver_parquet",
        description=(
            "Tabla Athena externa sobre la capa Silver del datalake. "
            "Lee datos Parquet normalizados desde "
            f"s3://{SILVER_BUCKET}/sivigila/. "
            "Permite análisis exploratorio sobre datos limpios antes del Gold."
        ),
        columns=SILVER_COLUMNS,
        location=f"s3://{SILVER_BUCKET}/sivigila/",
    )

    # ── 3. Linaje ──────────────────────────────────────────────────────────────
    print("\n[3/4] Creando aristas de linaje...")

    # Bronze → Silver  (Glue ETL Bronze-Silver)
    client.add_lineage(
        from_id=bronze["id"],   from_type="container", from_name=BRONZE_BUCKET,
        to_id=silver["id"],     to_type="container",   to_name=SILVER_BUCKET,
        description=(
            f"Glue job '{JOB_BRONZE_SILVER}': "
            "lee CSV desde Bronze, normaliza columnas, "
            "limpia nulos/duplicados y escribe Parquet en Silver."
        ),
    )

    # Silver → Athena Silver table  (tabla externa)
    client.add_lineage(
        from_id=silver["id"],        from_type="container", from_name=SILVER_BUCKET,
        to_id=table_silver["id"],    to_type="table",       to_name="sivigila_silver_parquet",
        description=(
            "Athena tabla externa: apunta directamente a "
            f"s3://{SILVER_BUCKET}/sivigila/. "
            "No hay transformación; Athena lee el Parquet de Silver para análisis ad-hoc."
        ),
    )

    # Athena Silver table → Gold  (Glue ETL Silver-Gold)
    client.add_lineage(
        from_id=table_silver["id"],  from_type="table",     from_name="sivigila_silver_parquet",
        to_id=gold["id"],            to_type="container",   to_name=GOLD_BUCKET,
        description=(
            f"Glue job '{JOB_SILVER_GOLD}': "
            "agrega datos Silver en dos tablas Gold — "
            "sivigila_resumen_comuna (epidemiología por zona/año) y "
            "sivigila_perfil_riesgo (clasificación de riesgo por paciente)."
        ),
    )

    # ── 4. Resumen ─────────────────────────────────────────────────────────────
    print("\n[4/4] Linaje registrado exitosamente.")
    print("=" * 65)
    print("  ENTIDADES CREADAS:")
    print(f"    Storage Service : {STORAGE_SERVICE_NAME}")
    print(f"    Container       : {BRONZE_BUCKET}  (Bronze)")
    print(f"    Container       : {SILVER_BUCKET}   (Silver)")
    print(f"    Container       : {GOLD_BUCKET}     (Gold)")
    print(f"    DB Service      : {ATHENA_SERVICE_NAME}")
    print(f"    Table           : {schema_fqn}.sivigila_silver_parquet")
    print()
    print("  LINAJE:")
    print(f"    {BRONZE_BUCKET}")
    print(f"      --> [{JOB_BRONZE_SILVER}]")
    print(f"    {SILVER_BUCKET}")
    print(f"      --> [Athena external table]")
    print(f"    {ATHENA_DB_NAME}.{ATHENA_SCHEMA_NAME}.sivigila_silver_parquet")
    print(f"      --> [{JOB_SILVER_GOLD}]")
    print(f"    {GOLD_BUCKET}")
    print()
    print(f"  Visualizar en: {host}/explore/lineage")
    print("=" * 65)
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# Punto de entrada
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Registra linaje de datos SIVIGILA en OpenMetadata"
    )
    parser.add_argument(
        "--host",     default="http://localhost:8585",
        help="URL base de OpenMetadata (default: http://localhost:8585)"
    )
    parser.add_argument(
        "--email",    default="admin@open-metadata.org",
        help="Email de usuario OpenMetadata"
    )
    parser.add_argument(
        "--password", default="admin",
        help="Contraseña del usuario"
    )
    parser.add_argument(
        "--token",    default=None,
        help="JWT Bearer token (alternativa a email/password)"
    )
    args = parser.parse_args()
    sys.exit(main(args.host, args.email, args.password, args.token))
