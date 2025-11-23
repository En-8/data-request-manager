provider "aws" {
  region  = var.aws_region
}

module "backend" {
  source = "./backend"

  project_name         = var.project_name
  db_password          = var.db_password
  aws_region           = var.aws_region
  ssh_public_key       = var.ssh_public_key
  ssh_private_key_path = var.ssh_private_key_path
}
