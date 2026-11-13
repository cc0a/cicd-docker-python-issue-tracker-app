variable "aws_region" {
  description = "AWS region for the development environment"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used in resource naming"
  type        = string
  default     = "cloud-incident-manager"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.small"
}

variable "app_ingress_cidr" {
  description = "Optional IPv4 CIDR allowed to access the app on port 8000. Leave empty to keep it private."
  type        = string
  default     = ""
}

variable "root_volume_size" {
  description = "EC2 root volume size in GiB"
  type        = number
  default     = 20
}

variable "ssh_ingress_cidr" {
  description = "IPv4 CIDR allowed to SSH into the EC2 instance"
  type        = string
}
