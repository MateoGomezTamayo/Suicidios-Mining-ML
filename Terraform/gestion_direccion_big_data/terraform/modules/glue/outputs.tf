output "glue_job_bronze_silver_name" {
  value = aws_glue_job.sivigila_etl.name
}

output "glue_job_silver_gold_name" {
  value = aws_glue_job.sivigila_gold_etl.name
}
