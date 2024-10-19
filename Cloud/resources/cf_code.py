import boto3
import zipfile
import os

# Initialize clients
lambda_client = boto3.client('lambda', region_name='us-east-1')
api_client = boto3.client('apigateway', region_name='us-east-1')
iam_client = boto3.client('iam')

# Lambda function code as a string
lambda_code = """
import json

def lambda_handler(event, context):
    name = event.get('queryStringParameters', {}).get('name', 'world')
    return {
        'statusCode': 200,
        'body': json.dumps(f"Hello, {name} from Lambda!")
    }
"""

# Create Lambda deployment package
def create_lambda_zip(zip_file_name='lambda_function.zip'):
    with zipfile.ZipFile(zip_file_name, 'w') as z:
        z.writestr('lambda_function.py', lambda_code)

# Upload Lambda function to AWS
def create_lambda_function(lambda_name, zip_file, role_arn):
    with open(zip_file, 'rb') as f:
        zipped_code = f.read()

    response = lambda_client.create_function(
        FunctionName=lambda_name,
        Runtime='python3.9',
        Role=role_arn,
        Handler='lambda_function.lambda_handler',
        Code=dict(ZipFile=zipped_code),
        Timeout=300,
        MemorySize=128,
    )
    return response['FunctionArn']

# Create REST API Gateway
def create_api_gateway(api_name):
    response = api_client.create_rest_api(
        name=api_name,
        description='API Gateway for Lambda integration',
    )
    return response['id']

# Create resource and method in API Gateway
def create_resource_and_method(api_id, lambda_arn):
    # Get the Root Resource ID
    resources = api_client.get_resources(restApiId=api_id)
    root_id = [r['id'] for r in resources['items'] if r['path'] == '/'][0]

    # Create a new resource '/hello'
    new_resource = api_client.create_resource(
        restApiId=api_id,
        parentId=root_id,
        pathPart='hello'
    )
    resource_id = new_resource['id']

    # Create GET method for '/hello' and integrate with Lambda
    api_client.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='GET',
        authorizationType='NONE'
    )

    lambda_uri = f'arn:aws:apigateway:{boto3.session.Session().region_name}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

    api_client.put_integration(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='GET',
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=lambda_uri
    )

    # Deploy the API
    deployment = api_client.create_deployment(
        restApiId=api_id,
        stageName='prod'
    )
    return deployment

# Grant API Gateway permission to invoke Lambda
def add_lambda_permission(lambda_name, api_id, account_id):
    region = boto3.session.Session().region_name
    source_arn = f'arn:aws:execute-api:{region}:{account_id}:{api_id}/*/GET/hello'

    response = lambda_client.add_permission(
        FunctionName=lambda_name,
        StatementId='apigateway-invoke-permission',
        Action='lambda:InvokeFunction',
        Principal='apigateway.amazonaws.com',
        SourceArn=source_arn
    )
    return response

def main():
    # Create Lambda deployment package
    zip_file_name = 'lambda_function.zip'
    create_lambda_zip(zip_file_name)

    # Role ARN: Update with your Lambda IAM role ARN
    role_arn = '<YOUR_ROLE_ARN>'
    
    # Step 1: Create Lambda Function
    lambda_name = 'MyHelloWorldLambda'
    lambda_arn = create_lambda_function(lambda_name, zip_file_name, role_arn)
    print(f"Created Lambda function: {lambda_arn}")

    # Step 2: Create API Gateway
    api_name = 'HelloWorldAPI'
    api_id = create_api_gateway(api_name)
    print(f"Created API Gateway with ID: {api_id}")

    # Step 3: Create Resource and Method in API Gateway
    deployment = create_resource_and_method(api_id, lambda_arn)
    print(f"API Gateway deployed at stage: {deployment['stageName']}")

    # Step 4: Add permission for API Gateway to invoke Lambda
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    permission = add_lambda_permission(lambda_name, api_id, account_id)
    print(f"Added API Gateway invoke permission: {permission}")

    print(f"API Gateway URL: https://{api_id}.execute-api.us-east-1.amazonaws.com/prod/hello")

if __name__ == '__main__':
    main()
