variable "project" {
  type = string
}

variable "env" {
  type = string
}

variable "bronze_bucket" {
  type = string
}

variable "silver_bucket" {
  type = string
}

variable "gold_bucket" {
  type = string
}

variable "glue_job_bronze_silver" {
  type = string
}

variable "glue_job_silver_gold" {
  type = string
}

variable "tags" {
  type    = map(string)
  default = {}
}
