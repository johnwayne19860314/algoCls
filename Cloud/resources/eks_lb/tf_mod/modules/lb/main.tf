resource "aws_security_group" "load_balancer_sg" {
  name        = "lb_security_group"
  description = "Allow HTTP inbound traffic"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"  # All traffic
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb" "my_lb" {
  name               = var.load_balancer_name
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.load_balancer_sg.id]
  subnets            = var.subnet_ids
}

resource "aws_lb_target_group" "my_target_group" {
  name     = "${var.load_balancer_name}-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 30
    path                = "/"
  }
}

resource "aws_lb_listener" "my_listener" {
  load_balancer_arn = aws_lb.my_lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "forward"
    target_group_arn = aws_lb_target_group.my_target_group.arn
  }
}

variable "load_balancer_name" {
  description = "Load Balancer Name"
}

variable "subnet_ids" {
  description = "List of Subnet IDs"
  type        = list(string)
}

variable "vpc_id" {
  description = "VPC ID where the Load Balancer will be created"
}
