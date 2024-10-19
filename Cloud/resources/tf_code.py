import subprocess

def deploy_terraform(directory):
    try:
        # Initialize Terraform
        subprocess.run(["terraform", "init"], check=True, cwd=directory)
        
        # Plan the deployment
        subprocess.run(["terraform", "plan"], check=True, cwd=directory)
        
        # Apply the configuration
        subprocess.run(["terraform", "apply", "-auto-approve"], check=True, cwd=directory)
        print("Deployment successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error during deployment: {e}")

# Specify the path where your `main.tf` file is located
deploy_terraform('/path/to/your/terraform/config')

import requests
import json

# Replace these with your actual Terraform Cloud organization and workspace names
organization = "your-org"
workspace = "your-workspace"
api_token = "your-api-token"

# Set up headers with API token
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/vnd.api+json"
}

# Define the URL for creating a run (applying changes)
url = f"https://app.terraform.io/api/v2/organizations/{organization}/workspaces/{workspace}/runs"

# Payload for creating a run
payload = {
    "data": {
        "attributes": {
            "is-destroy": False,
            "message": "Apply infrastructure changes via Python SDK"
        },
        "type": "runs",
        "relationships": {
            "workspace": {
                "data": {
                    "type": "workspaces",
                    "id": workspace
                }
            }
        }
    }
}

# Create a new run (apply plan)
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Print response
if response.status_code == 201:
    print("Run started successfully.")
else:
    print(f"Failed to start run: {response.text}")
