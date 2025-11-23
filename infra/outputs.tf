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
