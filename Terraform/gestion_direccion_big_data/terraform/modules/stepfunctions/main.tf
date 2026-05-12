# Rol IAM para que Step Functions pueda invocar Glue
resource "aws_iam_role" "sfn_role" {
  name = "${var.project}-${var.env}-sfn-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "states.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })

  tags = var.tags
}

resource "aws_iam_policy" "sfn_glue_policy" {
  name = "${var.project}-${var.env}-sfn-glue-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "glue:StartJobRun",
          "glue:GetJobRun",
          "glue:GetJobRuns",
          "glue:BatchStopJobRun"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogDelivery",
          "logs:PutLogEvents",
          "logs:DescribeLogGroups",
          "logs:DescribeResourcePolicies"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "sfn_glue_attach" {
  role       = aws_iam_role.sfn_role.name
  policy_arn = aws_iam_policy.sfn_glue_policy.arn
}

# State Machine SIVIGILA pipeline
resource "aws_sfn_state_machine" "sivigila_pipeline" {
  name     = "${var.project}-${var.env}-sivigila-pipeline"
  role_arn = aws_iam_role.sfn_role.arn
  type     = "STANDARD"

  definition = jsonencode({
    Comment = "Pipeline DQ -> Bronze -> Silver -> Gold con Glue para dataset SIVIGILA"
    StartAt = "dataQualityJob"
    States = {
      dataQualityJob = {
        Type     = "Task"
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Parameters = {
          JobName = "gx_data_quality_sivigila"
        }
        ResultPath = "$.dataQualityResult"
        Retry = [{
          ErrorEquals     = ["Glue.AWSGlueException", "States.TaskFailed"]
          IntervalSeconds = 30
          MaxAttempts     = 2
          BackoffRate     = 2
        }]
        Catch = [{
          ErrorEquals = ["States.ALL"]
          Next        = "bronzeToSilverJob"
          ResultPath  = "$.dataQualityError"
          Comment     = "Calidad opcional: si falla o no existe, continua el pipeline"
        }]
        Next = "validateDataQualityResult"
      }

      validateDataQualityResult = {
        Type = "Choice"
        Choices = [{
          Variable     = "$.dataQualityResult.JobRunState"
          StringEquals = "SUCCEEDED"
          Next         = "bronzeToSilverJob"
        }]
        Default = "bronzeToSilverJob"
      }

      bronzeToSilverJob = {
        Type     = "Task"
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Parameters = {
          JobName   = var.glue_job_bronze_silver
          Arguments = {
            "--input_path"  = "s3://${var.bronze_bucket}/sivigila_intsuicidio.csv"
            "--output_path" = "s3://${var.silver_bucket}/sivigila/"
          }
        }
        ResultPath = "$.bronzeToSilverResult"
        Retry = [{
          ErrorEquals     = ["Glue.AWSGlueException", "States.TaskFailed"]
          IntervalSeconds = 30
          MaxAttempts     = 2
          BackoffRate     = 2
        }]
        Catch = [{
          ErrorEquals = ["States.ALL"]
          Next        = "JobFailed"
          ResultPath  = "$.error"
        }]
        Next = "silverToGoldJob"
      }

      silverToGoldJob = {
        Type     = "Task"
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Parameters = {
          JobName   = var.glue_job_silver_gold
          Arguments = {
            "--input_path"          = "s3://${var.silver_bucket}/sivigila/"
            "--output_gold_resumen" = "s3://${var.gold_bucket}/sivigila_resumen_comuna/"
            "--output_gold_riesgo"  = "s3://${var.gold_bucket}/sivigila_perfil_riesgo/"
          }
        }
        ResultPath = "$.silverToGoldResult"
        Retry = [{
          ErrorEquals     = ["Glue.AWSGlueException", "States.TaskFailed"]
          IntervalSeconds = 30
          MaxAttempts     = 2
          BackoffRate     = 2
        }]
        Catch = [{
          ErrorEquals = ["States.ALL"]
          Next        = "JobFailed"
          ResultPath  = "$.error"
        }]
        Next = "PipelineSuccess"
      }

      PipelineSuccess = {
        Type    = "Succeed"
        Comment = "Pipeline completado: Bronze -> Silver -> Gold"
      }

      JobFailed = {
        Type  = "Fail"
        Error = "GlueJobFailed"
        Cause = "Uno de los jobs de Glue fallo. Revisar CloudWatch Logs del grupo /aws-glue/jobs."
      }
    }
  })

  tags = var.tags
}
