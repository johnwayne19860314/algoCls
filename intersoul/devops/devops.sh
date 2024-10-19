#!/bin/bash
# pleae write a .sh script to automate these steps \# build docker image

# docker build -f ./Dockerfile -t d3executor_qihang:16.9.75.0 .

# D3Helm folder

# **Modify the value.yaml in d3executor Chart.**

# \# In D3Helm folder

# helm package d3executor

# \# Successfully packaged chart and saved it to: /home/larry/code/d3executor/D3Helm/d3executor-16.9.10.tgz



# helm push d3executor-16.9.3000.tgz oci://us-docker.pkg.dev/emerald-ellipse-332519/dev/jjiang

# helm upgrade --install d3executor-jjiang-dt-8244 --set env.executorGUID=f089adaf-54e3-486b-8975-1a3823db9f03 --set service.type=LoadBalancer --set service.useAzureInternalLoadBalancer=true oci://us-docker.pkg.dev/emerald-ellipse-332519/dev/jjiang/d3executor --version 16.9.3000
# Variables
# DOCKER_IMAGE_NAME="d3executor_qihang"
# DOCKER_IMAGE_TAG="16.9.75.0"
# CHART_VERSION="16.9.3000"
# CHART_NAME="d3executor"
# OCI_REGISTRY="oci://us-docker.pkg.dev/emerald-ellipse-332519/dev/jjiang"
# HELM_RELEASE_NAME="d3executor-jjiang-dt-8244"
# EXECUTOR_GUID="f089adaf-54e3-486b-8975-1a3823db9f03"

# # Step 1: Build Docker image
# echo "Building Docker image..."
# docker build -f ./Dockerfile -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} .
# if [ $? -ne 0 ]; then
#     echo "Docker build failed!"
#     exit 1
# fi
# echo "Docker image built successfully!"

# # Step 2: Modify the values.yaml in d3executor Chart
# echo "Modify the values.yaml in the ${CHART_NAME} Chart..."
# # Add the commands or script logic here to modify the values.yaml file.
# # For example, you might use sed to update a specific line or value:
# # sed -i 's/some_value/updated_value/' ./D3Helm/${CHART_NAME}/values.yaml

# # Step 3: Package Helm Chart
# echo "Packaging Helm Chart..."
# cd D3Helm || exit
# helm package ${CHART_NAME}
# if [ $? -ne 0 ]; then
#     echo "Helm package failed!"
#     exit 1
# fi
# echo "Helm Chart packaged successfully!"

# # Step 4: Push Helm Chart to OCI registry
# echo "Pushing Helm Chart to OCI registry..."
# helm push ${CHART_NAME}-${CHART_VERSION}.tgz ${OCI_REGISTRY}
# if [ $? -ne 0 ]; then
#     echo "Helm push failed!"
#     exit 1
# fi
# echo "Helm Chart pushed successfully!"

# # Step 5: Upgrade or install the Helm release
# echo "Upgrading/Installing Helm release..."
# helm upgrade --install ${HELM_RELEASE_NAME} --set env.executorGUID=${EXECUTOR_GUID} --set service.type=LoadBalancer --set service.useAzureInternalLoadBalancer=true ${OCI_REGISTRY}/${CHART_NAME} --version ${CHART_VERSION}
# if [ $? -ne 0 ]; then
#     echo "Helm upgrade/install failed!"
#     exit 1
# fi
# echo "Helm release upgraded/installed successfully!"


#!/bin/bash

# Exit on any error
set -e

# Define version and file names
# IMAGE_TAG="d3executor_qihang:16.9.75.0"
CHART_NAME="postgresql"
# CHART_VERSION="16.9.3000"
# HELM_PACKAGE="${CHART_NAME}-${CHART_VERSION}.tgz"
HELM_REPO="oci://registry-1.docker.io/bitnamicharts"
RELEASE_NAME="pg-release"
#GUID="f089adaf-54e3-486b-8975-1a3823db9f03"
# Build Docker image
# echo "Building Docker image..."
# docker build -f ./Dockerfile -t $IMAGE_TAG .

# # Change directory to the sibling D3Helm folder
# echo "Changing directory to the D3Helm folder..."
# cd ../D3Helm

# # Package Helm chart
# echo "Packaging Helm chart..."
# helm package $CHART_NAME

# # Push Helm chart to repository
# echo "Pushing Helm chart to repository..."
# helm push $HELM_PACKAGE $HELM_REPO

# # Upgrade or install Helm release
# echo "Upgrading or installing Helm release..."
# helm upgrade --install $RELEASE_NAME \
#   $HELM_REPO/$CHART_NAME \
#   --version $CHART_VERSION

# Return to the original directory
# cd -

# echo "Script completed successfully."



helm install kubedb \
   oci://ghcr.io/appscode-charts/kubedb \                    
  --version v2024.9.30 \
  --namespace kubedb --create-namespace \
  --set-file global.license=./kubedb_licence.txt
  --wait --burst-limit=10000 --debug

kubectl get pods --all-namespaces -l "app.kubernetes.io/instance=kubedb"
kubectl get crd -l app.kubernetes.io/name=kubedb

# helm install kubedb oci://ghcr.io/appscode-charts/kubedb \
#   --version v2024.9.30 \
#   --namespace kubedb --create-namespace \
#   --set-file global.license=/path/to/the/license.txt \
#   --wait --burst-limit=10000 --debug


# helm install kubedb oci://ghcr.io/appscode-charts/kubedb \
#   --version v2024.9.30 \
#   --namespace kubedb --create-namespace \
#   --set-file global.license=./kubedb_licence.txt
