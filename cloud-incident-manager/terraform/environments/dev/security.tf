
resource "random_integer" "app_port" {
  min = 20000
  max = 60000
}

resource "aws_security_group" "app" {
  name        = "${var.project_name}-sg"
  description = "Security group for application EC2 instance"
  vpc_id      = aws_vpc.main.id

  dynamic "ingress" {
    for_each = var.app_ingress_cidr == "" ? [] : [var.app_ingress_cidr]

    content {
      description = "Application access from approved CIDR"
      from_port   = random_integer.app_port.result
      to_port     = random_integer.app_port.result
      protocol    = "tcp"
      cidr_blocks = [ingress.value]
    }
  }

  egress {
    description = "Allow outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-sg"
  }
}

resource "aws_iam_role" "ec2_ssm" {
  name = "${var.project_name}-ssm-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ssm" {
  role       = aws_iam_role.ec2_ssm.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "app" {
  name = "${var.project_name}-instance-profile"
  role = aws_iam_role.ec2_ssm.name
}
