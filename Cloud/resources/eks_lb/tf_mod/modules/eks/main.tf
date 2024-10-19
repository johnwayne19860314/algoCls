resource "aws_eks_cluster" "my_cluster" {
  name     = var.cluster_name
  role_arn = var.cluster_role_arn

  vpc_config {
    subnet_ids          = var.subnet_ids
    security_group_ids  = var.security_group_ids
  }
}

variable "cluster_name" {
  description = "EKS Cluster Name"
}

variable "cluster_role_arn" {
  description = "IAM Role ARN for EKS"
}

variable "subnet_ids" {
  description = "List of Subnet IDs"
  type        = list(string)
}

variable "security_group_ids" {
  description = "List of Security Group IDs"
  type        = list(string)
}

variable "vpc_id" {
  description = "VPC ID where the EKS cluster will be created"
}
