provider "aws" {
  region = "us-west-2"  # Change to your desired region
}

variable "eks_cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
}

variable "pod_name" {
  description = "Name of the EKS pod"
  type        = string
}

resource "aws_cloudwatch_metric_alarm" "cpu_alarm" {
  alarm_name                = "${var.pod_name}-cpu-alarm"
  alarm_description         = "Alarm for EKS Pod CPU usage exceeding 80%"
  namespace                 = "AWS/EKS"
  metric_name               = "CPUUtilization"
  statistic                 = "Average"
  period                    = 60
  evaluation_periods        = 1
  threshold                 = 80
  comparison_operator       = "GreaterThanThreshold"
  dimensions                = {
    ClusterName = var.eks_cluster_name
    PodName     = var.pod_name
  }
  alarm_actions             = []  # Add SNS topic ARN or other actions if needed
}

resource "aws_cloudwatch_metric_alarm" "memory_alarm" {
  alarm_name                = "${var.pod_name}-memory-alarm"
  alarm_description         = "Alarm for EKS Pod Memory usage exceeding 80%"
  namespace                 = "AWS/EKS"
  metric_name               = "MemoryUtilization"
  statistic                 = "Average"
  period                    = 60
  evaluation_periods        = 1
  threshold                 = 80
  comparison_operator       = "GreaterThanThreshold"
  dimensions                = {
    ClusterName = var.eks_cluster_name
    PodName     = var.pod_name
  }
  alarm_actions             = []  # Add SNS topic ARN or other actions if needed
}

output "cpu_alarm_name" {
  value = aws_cloudwatch_metric_alarm.cpu_alarm.alarm_name
}

output "memory_alarm_name" {
  value = aws_cloudwatch_metric_alarm.memory_alarm.alarm_name
}
