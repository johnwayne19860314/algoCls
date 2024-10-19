import boto3
import time

def create_eks_cluster(cluster_name, role_arn, subnet_ids, security_group_ids):
    eks_client = boto3.client('eks')

    response = eks_client.create_cluster(
        name=cluster_name,
        version='1.21',
        roleArn=role_arn,
        resourcesVpcConfig={
            'subnetIds': subnet_ids,
            'securityGroupIds': security_group_ids,
            'endpointPublicAccess': True,
        }
    )

    # Wait for the cluster to be active
    waiter = eks_client.get_waiter('cluster_active')
    waiter.wait(name=cluster_name)

    return response


def create_load_balancer(load_balancer_name):
    elbv2_client = boto3.client('elbv2')

    # Create an Application Load Balancer
    lb_response = elbv2_client.create_load_balancer(
        Name=load_balancer_name,
        Subnets=[
            'subnet-abc123',  # Replace with your subnet IDs
            'subnet-def456',
        ],
        SecurityGroups=[
            'sg-abc123',  # Replace with your security group IDs
        ],
        Scheme='internet-facing',
        Tags=[
            {
                'Key': 'Name',
                'Value': load_balancer_name
            },
        ],
        Type='application',
    )

    return lb_response


def create_target_group(load_balancer_name):
    elbv2_client = boto3.client('elbv2')

    # Create a target group
    target_group_response = elbv2_client.create_target_group(
        Name=f"{load_balancer_name}-target-group",
        Protocol='HTTP',
        Port=80,
        VpcId='vpc-abc123',  # Replace with your VPC ID
        HealthCheckProtocol='HTTP',
        HealthCheckPath='/',
        HealthCheckIntervalSeconds=30,
        HealthCheckTimeoutSeconds=5,
        HealthyThresholdCount=5,
        UnhealthyThresholdCount=2,
    )

    return target_group_response


def create_listener(load_balancer_arn, target_group_arn):
    elbv2_client = boto3.client('elbv2')

    # Create a listener
    listener_response = elbv2_client.create_listener(
        LoadBalancerArn=load_balancer_arn,
        Port=80,
        Protocol='HTTP',
        DefaultActions=[
            {
                'Type': 'forward',
                'TargetGroupArn': target_group_arn,
            },
        ],
    )

    return listener_response


def register_targets(target_group_arn, instance_ids):
    elbv2_client = boto3.client('elbv2')

    # Register the EKS service in the target group
    response = elbv2_client.register_targets(
        TargetGroupArn=target_group_arn,
        Targets=[
            {
                'Id': instance_id,  # Replace with your EKS instances or service endpoints
                'Port': 80  # Change this if your service runs on a different port
            }
            for instance_id in instance_ids
        ]
    )

    return response


def main():
    cluster_name = 'my-eks-cluster'
    load_balancer_name = 'my-load-balancer'
    role_arn = 'arn:aws:iam::123456789012:role/EKS-Cluster-Role'  # Replace with your IAM role ARN
    subnet_ids = ['subnet-abc123', 'subnet-def456']  # Replace with your subnet IDs
    security_group_ids = ['sg-abc123']  # Replace with your security group IDs

    # Step 1: Create EKS Cluster
    eks_response = create_eks_cluster(cluster_name, role_arn, subnet_ids, security_group_ids)
    print("EKS Cluster Created:", eks_response)

    # Step 2: Create Load Balancer
    lb_response = create_load_balancer(load_balancer_name)
    print("Load Balancer Created:", lb_response)

    # Step 3: Create Target Group
    target_group_response = create_target_group(load_balancer_name)
    print("Target Group Created:", target_group_response)

    # Step 4: Create Listener
    load_balancer_arn = lb_response['LoadBalancers'][0]['LoadBalancerArn']
    target_group_arn = target_group_response['TargetGroups'][0]['TargetGroupArn']
    listener_response = create_listener(load_balancer_arn, target_group_arn)
    print("Listener Created:", listener_response)

    # Step 5: Register Targets (EKS Instances or Services)
    instance_ids = ['i-abc123', 'i-def456']  # Replace with your EKS instance IDs or service endpoints
    register_response = register_targets(target_group_arn, instance_ids)
    print("Targets Registered:", register_response)


if __name__ == "__main__":
    main()
