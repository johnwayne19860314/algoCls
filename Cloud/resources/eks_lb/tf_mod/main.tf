-- terraform init
terraform plan -var "cluster_name=my-eks-cluster" -var "cluster_role_arn=arn:aws:iam::123456789012:role/EKS-Cluster-Role" -var "subnet_ids=[\"subnet-abc123\",\"subnet-def456\"]" -var "security_group_ids=[\"sg-abc123\",\"sg-def456\"]" -var "vpc_id=vpc-abc123"
terraform apply -var "cluster_name=my-eks-cluster" -var "cluster_role_arn=arn:aws:iam::123456789012:role/EKS-Cluster-Role" -var "subnet_ids=[\"subnet-abc123\",\"subnet-def456\"]" -var "security_group_ids=[\"sg-abc123\",\"sg-def456\"]" -var "vpc_id=vpc-abc123"

provider "aws" {
  region = "us-west-2"  # Change to your desired region
}

module "eks" {
  source            = "./modules/eks"
  cluster_name      = var.cluster_name
  cluster_role_arn  = var.cluster_role_arn
  subnet_ids        = var.subnet_ids
  security_group_ids = var.security_group_ids
  vpc_id            = var.vpc_id
}

module "load_balancer" {
  source              = "./modules/load_balancer"
  load_balancer_name  = var.load_balancer_name
  subnet_ids          = var.subnet_ids
  vpc_id              = var.vpc_id
  security_group_ids  = var.security_group_ids
}
