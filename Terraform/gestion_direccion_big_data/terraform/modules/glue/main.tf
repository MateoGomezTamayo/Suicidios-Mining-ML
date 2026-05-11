resource "aws_glue_job" "sivigila_etl" {
  name     = "${var.project}-${var.env}-sivigila-etl"
  role_arn = var.glue_role_arn

  command {
    script_location = var.script_location
    python_version  = "3"
  }


  default_arguments = {
    "--input_path"  = "s3://${var.bronze_bucket}/sivigila_intsuicidio.csv"
    "--output_path" = "s3://${var.silver_bucket}/sivigila/"
    "--TempDir"     = "s3://${var.temp_bucket}/temp/"
  }


  worker_type       = "G.1X"
  number_of_workers = 2

  glue_version = "5.0"

  timeout = 10

  tags = var.tags
}

resource "aws_glue_job" "sivigila_gold_etl" {
  name     = "${var.project}-${var.env}-sivigila-gold-etl"
  role_arn = var.glue_role_arn

  command {
    script_location = var.script_location_gold
    python_version  = "3"
  }

  default_arguments = {
    "--input_path"          = "s3://${var.silver_bucket}/sivigila/"
    "--output_gold_resumen" = "s3://${var.gold_bucket}/sivigila_resumen_comuna/"
    "--output_gold_riesgo"  = "s3://${var.gold_bucket}/sivigila_perfil_riesgo/"
    "--TempDir"             = "s3://${var.temp_bucket}/temp/"
  }

  worker_type       = "G.1X"
  number_of_workers = 2

  glue_version = "5.0"

  timeout = 15

  tags = var.tags
}