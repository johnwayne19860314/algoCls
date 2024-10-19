import boto3

def create_cloudwatch_alarm(alarm_name, metric_name, threshold, comparison_operator, namespace, dimensions):
    cloudwatch = boto3.client('cloudwatch')

    response = cloudwatch.put_metric_alarm(
        AlarmName=alarm_name,
        ComparisonOperator=comparison_operator,
        EvaluationPeriods=1,
        MetricName=metric_name,
        Namespace=namespace,
        Period=60,
        Statistic='Average',
        Threshold=threshold,
        ActionsEnabled=True,
        AlarmDescription=f"Alarm for {metric_name} exceeding {threshold}",
        Dimensions=dimensions,
        Unit='Percent'
    )

    print(f"Created alarm: {alarm_name}, Response: {response}")


# Parameters
eks_cluster_name = 'your-eks-cluster-name'
namespace = 'kube-system'  # Typically the namespace for kube-system pods
cpu_alarm_name = 'EKS-CPU-High'
memory_alarm_name = 'EKS-Memory-High'

# Dimensions for the metrics
dimensions_cpu = [
    {
        'Name': 'ClusterName',
        'Value': eks_cluster_name
    },
    {
        'Name': 'PodName',
        'Value': 'your-pod-name'  # Replace with your pod name
    }
]

dimensions_memory = dimensions_cpu.copy()  # Same dimensions for memory

# Create alarms for CPU and Memory usage
create_cloudwatch_alarm(cpu_alarm_name, 'CPUUtilization', 80, 'GreaterThanThreshold', 'AWS/EKS', dimensions_cpu)
create_cloudwatch_alarm(memory_alarm_name, 'MemoryUtilization', 80, 'GreaterThanThreshold', 'AWS/EKS', dimensions_memory)
