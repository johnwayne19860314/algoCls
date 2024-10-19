# You'll be prompted to provide your **AWS Access Key**, **Secret Key**, **region**, and **output format**.
aws configure
# Run the following command to retrieve the EKS cluster kubeconfig:**
# This command retrieves the kubeconfig details for your EKS cluster and merges it into your local `~/.kube/config` file, allowing `kubectl` to use it.
aws eks update-kubeconfig --region us-west-2 --name my-cluster
  

# get name of master pod of acid-minimal-cluster
export PGMASTER=$(kubectl get pods -o jsonpath={.items..metadata.name} -l application=spilo,cluster-name=acid-minimal-cluster,spilo-role=master -n default)
# set up port forward
kubectl port-forward $PGMASTER 6432:5432 -n default
# Open another CLI and connect to the database using e.g. the psql client.
# When connecting with a manifest role like `foo_user` user, read its password
# from the K8s secret which was generated when creating `acid-minimal-cluster`.
# As non-encrypted connections are rejected by default set SSL mode to `require`:
# username as postgres
export PGPASSWORD=$(kubectl get secret postgres.acid-minimal-cluster.credentials.postgresql.acid.zalan.do -o 'jsonpath={.data.password}' | base64 -d)
export PGSSLMODE=require
# You can now access the web interface by port forwarding the UI pod (mind the
# label selector) and enter `localhost:8081` in your browser:
kubectl port-forward svc/postgres-operator-ui 8081:80



#A default user named elastic is created by default with the password stored in a Kubernetes secret:
PASSWORD=$(kubectl get secret quickstart-es-elastic-user -o go-template='{{.data.elastic | base64decode}}')
echo $PASSWORD
# 9009D8N86bBt2Utme0uoM8mH
#From your local workstation, use the following command in a separate terminal:
kubectl port-forward service/quickstart-es-http 9200
curl -u "elastic:$PASSWORD" -k "https://localhost:9200"

kubectl port-forward service/quickstart-kb-http 5601
# 9009D8N86bBt2Utme0uoM8mH  Login as the elastic user. 
kubectl get secret quickstart-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode; echo
# open browser with https://localhost:5601 username: elastic   pw:9009D8N86bBt2Utme0uoM8mH
