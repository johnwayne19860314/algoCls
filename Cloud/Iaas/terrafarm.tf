// terraform init/apply

provider "aws" {
  region = "us-east-1"
}

resource "aws_security_group" "allow_http" {
  name        = "allow_http"
  description = "Allow HTTP inbound traffic"
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "my_instance" {
  ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 AMI
  instance_type = "t2.micro"
  
  vpc_security_group_ids = [aws_security_group.allow_http.id]

  key_name = "my-keypair"  # Replace with your own keypair
}

output "instance_public_ip" {
  value = aws_instance.my_instance.public_ip
}
