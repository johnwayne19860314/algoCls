## 10-09

1, create microk8s with 2 cpu and 4G memory in local computer 

2, build and deploy keda in microk8s

3, install Lens tool to observe the k8s cluster

4, install the  prometheus in the k8s cluster

5, install grafana with prometheus for observability

6, create a web service -- nginx -- for testing the load

7, expose the nginx pods as a service 

8, port mapping with prometheus/grafana/nginx service to access them locally

9, run vegeta tool for load testing. try to observe the scalability of nginx pod

10, create keda scaleObject with prometheus as a trigger and deploy to the k8s

## 10-08

microk8s enable prometheus

Infer repository core for addon prometheus

DEPRECATION WARNING: 'prometheus' is deprecated and will soon be removed. Please use 'observability' instead.



Infer repository core for addon observability

Addon core/dns is already enabled

Addon core/helm3 is already enabled

Enabling default storage class.

WARNING: Hostpath storage is not suitable for production environments.

​     A hostpath volume can grow beyond the size limit set in the volume claim manifest.



deployment.apps/hostpath-provisioner created

storageclass.storage.k8s.io/microk8s-hostpath created

serviceaccount/microk8s-hostpath created

clusterrole.rbac.authorization.k8s.io/microk8s-hostpath created

clusterrolebinding.rbac.authorization.k8s.io/microk8s-hostpath created

Storage will be available soon.

Enabling observability

Release "kube-prom-stack" does not exist. Installing it now.

NAME: kube-prom-stack

LAST DEPLOYED: Tue Oct 8 14:55:12 2024

NAMESPACE: observability

STATUS: deployed

REVISION: 1

NOTES:

kube-prometheus-stack has been installed. Check its status by running:

 kubectl --namespace observability get pods -l "release=kube-prom-stack"



Visit https://github.com/prometheus-operator/kube-prometheus for instructions on how to create & configure Alertmanager and Prometheus instances using the Operator.

Release "loki" does not exist. Installing it now.

NAME: loki

LAST DEPLOYED: Tue Oct 8 14:55:48 2024

NAMESPACE: observability

STATUS: deployed

REVISION: 1

NOTES:

The Loki stack has been deployed to your cluster. Loki can now be added as a datasource in Grafana.



See http://docs.grafana.org/features/datasources/loki/ for more detail.

Release "tempo" does not exist. Installing it now.

NAME: tempo

LAST DEPLOYED: Tue Oct 8 14:55:52 2024

NAMESPACE: observability

STATUS: deployed

REVISION: 1

TEST SUITE: None



Note: the observability stack is setup to monitor only the current nodes of the MicroK8s cluster.

For any nodes joining the cluster at a later stage this addon will need to be set up again.



Observability has been enabled (user/pass: admin/prom-operator)









## 10-07

weekly sheet

Total hours.

​	 12 weeks each week 10 hours

by end of Friday

Dev/read/research

Oct. -- Dec.

Metrics : Prothumes

Task

1: try predictKube for freeAccess

2, setup protheses with leda to monitor the metrics

3, setup a web service and use locust to loadstress service and monitor the metrics in protheses



## 10-06

apt-get install build-essential
apt install make
wget https://go.dev/dl/go1.20.linux-arm64.tar.gz
tar -C /usr/local -zxvf go1.20.linux-arm64.tar.gz
cat >> /etc/profile <<EOF

export GOROOT=/usr/local/go
export PATH=$PATH:$GOROOT/bin
EOF
source /etc/profile  && go version



pural paperwork for RA

/go/src/github.com/johnwayne19860314/keda

