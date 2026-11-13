
resource "aws_instance" "app" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public.id
  associate_public_ip_address = true
  key_name                    = aws_key_pair.deployer.key_name

  vpc_security_group_ids = [
    aws_security_group.app.id
  ]

  iam_instance_profile = aws_iam_instance_profile.app.name

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  root_block_device {
    volume_size           = var.root_volume_size
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }

  user_data = <<-EOF
    #!/bin/bash
    set -eux

    apt-get update

    DEBIAN_FRONTEND=noninteractive apt-get install -y \
      git \
      docker.io \
      python3 \
      python3-pip \
      python3-venv

    systemctl enable docker
    systemctl start docker

    usermod -aG docker ubuntu
  EOF

  user_data_replace_on_change = true

  tags = {
    Name = "${var.project_name}-dev-ec2"
  }

  depends_on = [
    aws_iam_role_policy_attachment.ssm,
    aws_route_table_association.public
  ]
}
