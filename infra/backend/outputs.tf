output "ec2_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_eip.api.public_ip
}

output "api_url" {
  description = "URL of the API endpoint"
  value       = "http://${aws_eip.api.public_ip}:${var.api_port}"
}

output "rds_endpoint" {
  description = "Endpoint of the RDS PostgreSQL instance"
  value       = aws_db_instance.main.endpoint
}

output "rds_address" {
  description = "Address of the RDS PostgreSQL instance (without port)"
  value       = aws_db_instance.main.address
}

output "ssh_command" {
  description = "SSH command to connect to the EC2 instance"
  value       = "ssh -i ${var.ssh_private_key_path} ec2-user@${aws_eip.api.public_ip}"
}
