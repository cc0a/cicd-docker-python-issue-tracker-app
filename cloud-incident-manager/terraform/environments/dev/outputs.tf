output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.app.id
}

output "instance_public_ip" {
  description = "EC2 public IP address"
  value       = aws_instance.app.public_ip
}

output "instance_public_dns" {
  description = "EC2 public DNS name"
  value       = aws_instance.app.public_dns
}

output "vpc_id" {
  description = "Development VPC ID"
  value       = aws_vpc.main.id
}

output "subnet_id" {
  description = "Development subnet ID"
  value       = aws_subnet.public.id
}

output "ubuntu_ami" {
  description = "Ubuntu AMI selected by Terraform"
  value       = data.aws_ami.ubuntu.id
}

output "app_port" {
  description = "Random application port"
  value       = random_integer.app_port.result
}

output "ssh_command" {
  description = "SSH command for connecting to EC2"
  value       = "ssh -i /home/snow/.ssh/id_rsa ubuntu@${aws_instance.app.public_ip}"
}