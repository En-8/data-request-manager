output "ec2_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = module.backend.ec2_public_ip
}

output "api_url" {
  description = "URL of the API endpoint"
  value       = module.backend.api_url
}

output "rds_endpoint" {
  description = "Endpoint of the RDS PostgreSQL instance"
  value       = module.backend.rds_endpoint
}

output "ssh_command" {
  description = "SSH command to connect to the EC2 instance"
  value       = module.backend.ssh_command
}

output "frontend_url" {
  description = "URL of the frontend website"
  value       = module.ui.website_endpoint
}

output "frontend_bucket" {
  description = "Name of the S3 bucket for frontend assets"
  value       = module.ui.bucket_name
}
