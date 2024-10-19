import boto3
import zipfile
import os

# Boto3 clients
cf_client = boto3.client('cloudformation', region_name='us-east-1')
lambda_client = boto3.client('lambda', region_name='us-east-1')
api_client = boto3.client('apigateway', region_name='us-east-1')

# Lambda function code
lambda_code = """
import json

def lambda_handler(event, context):
    name = event.get('queryStringParameters', {}).get('name', 'world')
    return {
        'statusCode': 200,
        'body': json.dumps(f"Hello, {name} from Lambda!")
    }
"""

# Write the lambda function to a .zip file
def create_lambda_zip(file_name='lambda_function.zip'):
    with zipfile.ZipFile(file_name, 'w') as z:
        z.writestr('lambda_function.py', lambda_code)

# Function to create and deploy CloudFormation stack
def deploy_cloudformation_stack():
    # Define the CloudFormation template
    template_body = """
    AWSTemplateFormatVersion: '2010-09-09'
    Resources:
      MyLambdaFunction:
        Type: AWS::Lambda::Function
        Properties:
          Handler: lambda_function.lambda_handler
          Role: arn:aws:iam::<YOUR_ROLE_ARN>
          Runtime: python3.9
          Code:
            S3Bucket: <YOUR_S3_BUCKET>
            S3Key: lambda_function.zip
          MemorySize: 128
          Timeout: 3

      ApiGateway:
        Type: AWS::ApiGateway::RestApi
        Properties:
          Name: LambdaAPIGateway
          
      ApiResource:
        Type: AWS::ApiGateway::Resource
        Properties: 
          ParentId:
            Fn::GetAtt:
              - ApiGateway
              - RootResourceId
          PathPart: "hello"
          RestApiId: 
            Ref: "ApiGateway"
        
      ApiMethod:
        Type: AWS::ApiGateway::Method
        Properties:
          RestApiId: 
            Ref: "ApiGateway"
          ResourceId:
            Ref: "ApiResource"
          HttpMethod: "GET"
          AuthorizationType: "NONE"
          Integration:
            IntegrationHttpMethod: "POST"
            Type: "AWS_PROXY"
            Uri:
              Fn::Sub: 
                arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${MyLambdaFunction.Arn}/invocations
    """

    # Create CloudFormation stack
    stack_name = "LambdaAPIStack"
    response = cf_client.create_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Capabilities=['CAPABILITY_IAM']
    )
    print(f"Creating stack {stack_name}: {response['StackId']}")

# Upload lambda code to S3 and deploy stack
create_lambda_zip()  # Prepare Lambda code package
deploy_cloudformation_stack()  # Deploy stack using CloudFormation
