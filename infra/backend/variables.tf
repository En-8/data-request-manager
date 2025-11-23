variable "project_name" {
  description = "Name of the project, used for resource naming"
  type        = string
}

variable "db_password" {
  description = "Password for the RDS PostgreSQL database"
  type        = string
  sensitive   = true
}

variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
}

variable "db_username" {
  description = "Username for the RDS PostgreSQL database"
  type        = string
  default     = "postgres"
}

variable "db_name" {
  description = "Name of the database to create"
  type        = string
  default     = "data_request_manager"
}

variable "api_port" {
  description = "Port the FastAPI application listens on"
  type        = number
  default     = 8000
}

variable "ssh_public_key" {
  description = "SSH public key for EC2 instance access"
  type        = string
}

variable "ssh_private_key_path" {
  description = "Path to SSH private key for Ansible"
  type        = string
}
