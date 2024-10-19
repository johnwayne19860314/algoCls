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

variable "load_balancer_name" {
  description = "Load Balancer Name"
  default     = "my-load-balancer"
}
