To set up metrics monitoring using **Prometheus** and **Grafana**, follow this step-by-step guide. This setup is widely used for monitoring applications running on Kubernetes clusters or standalone systems by collecting, querying, and visualizing metrics.

### Overview
- **Prometheus**: An open-source monitoring system that scrapes and stores time-series data.
- **Grafana**: A visualization tool that connects to Prometheus (or other data sources) to create dashboards and graphs.

### Steps to Set Up Prometheus and Grafana for Metrics

#### 1. **Install Prometheus**

##### a. Standalone Installation
If you’re not using Kubernetes, download and configure Prometheus manually.

1. **Download Prometheus**:
   Go to the [Prometheus download page](https://prometheus.io/download/) and choose the appropriate binary for your system.

   Example for Linux:
   ```bash
   wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
   tar -xvf prometheus-2.45.0.linux-amd64.tar.gz
   cd prometheus-2.45.0.linux-amd64
   ```

2. **Run Prometheus**:
   You can start Prometheus using the default configuration for testing:

   ```bash
   ./prometheus --config.file=prometheus.yml
   ```

   Prometheus will be accessible on `http://localhost:9090`.

##### b. Installation in Kubernetes (via Helm)
If you are running Kubernetes, it's easier to install Prometheus using **Helm**.

1. **Add Prometheus Helm repository**:
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update
   ```

2. **Install Prometheus**:
   ```bash
   helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace
   ```

This installs Prometheus into the `monitoring` namespace of your Kubernetes cluster.

#### 2. **Install Grafana**

##### a. Standalone Installation

1. **Download Grafana**:
   Download the appropriate binary from the [Grafana download page](https://grafana.com/grafana/download).

   Example for Linux:
   ```bash
   wget https://dl.grafana.com/oss/release/grafana-10.1.0.linux-amd64.tar.gz
   tar -zxvf grafana-10.1.0.linux-amd64.tar.gz
   cd grafana-10.1.0
   ```

2. **Start Grafana**:
   ```bash
   ./bin/grafana-server web
   ```

   Grafana will be accessible on `http://localhost:3000`.

##### b. Installation in Kubernetes (via Helm)

1. **Add Grafana Helm repository**:
   ```bash
   helm repo add grafana https://grafana.github.io/helm-charts
   helm repo update
   ```

2. **Install Grafana**:
   ```bash
   helm install grafana grafana/grafana --namespace monitoring
   ```

   This installs Grafana into the `monitoring` namespace.

3. **Get the admin password**:
   Retrieve the default admin password for Grafana by running:
   ```bash
   kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
   ```

4. **Access Grafana**:
   You can port-forward to access the Grafana UI:
   ```bash
   kubectl port-forward svc/grafana 3000:80 --namespace monitoring
   ```

   Open `http://localhost:3000` in your browser and log in with the username `admin` and the password retrieved above.

#### 3. **Connect Prometheus to Grafana**

1. **Log into Grafana**:
   Go to `http://localhost:3000` (or the port where Grafana is running).

2. **Add Prometheus as a Data Source**:
   - Navigate to **Settings** → **Data Sources** → **Add data source**.
   - Select **Prometheus** from the list of available data sources.
   - In the `HTTP` section, set the URL to the Prometheus server, for example: `http://localhost:9090` (or the appropriate service address in Kubernetes).
   - Click **Save & Test** to verify the connection.

#### 4. **Set Up Dashboards in Grafana**

1. **Import Pre-built Dashboards**:
   Grafana has a large collection of pre-built dashboards for various applications. You can import these from [Grafana Dashboards](https://grafana.com/grafana/dashboards/).

   - Go to **Dashboard** → **Manage** → **Import**.
   - Enter the dashboard ID (found on the dashboard page). For example, for a general Prometheus dashboard, the ID could be `3662`.
   - Click **Load** and then select the Prometheus data source.

2. **Create Custom Dashboards**:
   If you want to build custom dashboards, you can:
   - Navigate to **Dashboards** → **New Dashboard**.
   - Add different panels (graphs, gauges, tables) and select queries to pull data from Prometheus.
   - Example query to monitor CPU usage:
     ```prometheus
     node_cpu_seconds_total{mode="idle"}
     ```

3. **Save the Dashboard**: Once you’ve added all the panels and configured queries, save your dashboard for future use.

#### 5. **Monitor Metrics**

- Use Grafana to visualize various metrics scraped by Prometheus.
- You can monitor CPU usage, memory, network I/O, and more using Prometheus’ built-in metrics or custom application metrics if you've instrumented your application using Prometheus libraries.

#### 6. **Set Up Alerts (Optional)**

You can configure Prometheus and Grafana to set up alerting based on your metrics.

- In Prometheus, configure `alertmanager` and set alert rules.
- In Grafana, create alert conditions on your panels.

### Example Alert in Prometheus:

1. Add the alert rule to your Prometheus configuration:
   ```yaml
   groups:
     - name: example-alert
       rules:
         - alert: HighCPUUsage
           expr: node_cpu_seconds_total{mode="idle"} < 100
           for: 5m
           labels:
             severity: critical
           annotations:
             summary: "High CPU usage detected"
             description: "CPU usage is above threshold on instance {{ $labels.instance }}"
   ```

2. Set up the Alertmanager to send notifications to email, Slack, or other integrations.

### Summary:

1. Install Prometheus to scrape and store metrics.
2. Install Grafana to visualize the metrics.
3. Connect Prometheus to Grafana.
4. Create or import dashboards to visualize your data.
5. Optionally, set up alerts to get notified about critical system conditions.

This setup allows you to monitor and visualize metrics for your systems and applications, offering insights into system performance and health.

NAME: grafana
LAST DEPLOYED: Fri Oct 18 11:41:41 2024
NAMESPACE: monitoring
STATUS: deployed
REVISION: 1
NOTES:
1. Get your 'admin' user password by running:

   kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

   0xD7cRzN2Z9ik2POUFgkncVtZtagHki0WRrtR5y6


2. The Grafana server can be accessed via port 80 on the following DNS name from within your cluster:

   grafana.monitoring.svc.cluster.local

   Get the Grafana URL to visit by running these commands in the same shell:
     export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}")
     kubectl --namespace monitoring port-forward $POD_NAME 3000

3. Login with the password from step 1 and the username: admin
#################################################################################
######   WARNING: Persistence is disabled!!! You will lose your data when   #####
######            the Grafana pod is terminated.                            #####
#################################################################################

helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace

WARNING: Kubernetes configuration file is group-readable. This is insecure. Location: /Users/john/.kube/config
WARNING: Kubernetes configuration file is world-readable. This is insecure. Location: /Users/john/.kube/config
NAME: prometheus
LAST DEPLOYED: Fri Oct 18 11:50:42 2024
NAMESPACE: monitoring
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
The Prometheus server can be accessed via port 80 on the following DNS name from within your cluster:
prometheus-server.monitoring.svc.cluster.local


Get the Prometheus server URL by running these commands in the same shell:
  export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=prometheus,app.kubernetes.io/instance=prometheus" -o jsonpath="{.items[0].metadata.name}")
  kubectl --namespace monitoring port-forward $POD_NAME 9090


The Prometheus alertmanager can be accessed via port 9093 on the following DNS name from within your cluster:
prometheus-alertmanager.monitoring.svc.cluster.local


Get the Alertmanager URL by running these commands in the same shell:
  export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=alertmanager,app.kubernetes.io/instance=prometheus" -o jsonpath="{.items[0].metadata.name}")
  kubectl --namespace monitoring port-forward $POD_NAME 9093
#################################################################################
######   WARNING: Pod Security Policy has been disabled by default since    #####
######            it deprecated after k8s 1.25+. use                        #####
######            (index .Values "prometheus-node-exporter" "rbac"          #####
###### .          "pspEnabled") with (index .Values                         #####
######            "prometheus-node-exporter" "rbac" "pspAnnotations")       #####
######            in case you still need it.                                #####
#################################################################################


The Prometheus PushGateway can be accessed via port 9091 on the following DNS name from within your cluster:
prometheus-prometheus-pushgateway.monitoring.svc.cluster.local


Get the PushGateway URL by running these commands in the same shell:
  export POD_NAME=$(kubectl get pods --namespace monitoring -l "app=prometheus-pushgateway,component=pushgateway" -o jsonpath="{.items[0].metadata.name}")
  kubectl --namespace monitoring port-forward $POD_NAME 9091

For more information on running Prometheus, visit:
https://prometheus.io/

To update the **storage class** for Prometheus when using **Helm**, you need to modify the `values.yaml` file or use the `--set` flag during the `helm install` or `helm upgrade` command. Here's a step-by-step guide to configuring and updating the storage class for Prometheus using Helm.

### Steps to Update Storage Class for Prometheus

#### 1. **Check Prometheus Storage Configuration**

Prometheus, when deployed using the **prometheus-community** Helm chart, stores persistent data using Persistent Volume Claims (PVCs). These PVCs are associated with a specific **storage class**.

You can update the storage class by configuring the following settings in Prometheus's `values.yaml`:

- `server.persistentVolume.storageClass`: This controls the storage class for Prometheus server.
- `alertmanager.persistentVolume.storageClass`: This controls the storage class for Alertmanager, if you're using it.

#### 2. **Modify values.yaml**

If you have a `values.yaml` file for your Prometheus installation, update the storage class by modifying the corresponding section.

Example of modifying `values.yaml`:

```yaml
server:
  persistentVolume:
    enabled: true
    storageClass: "gp2" # <-- Update this to your desired storage class
    size: 10Gi
    accessModes:
      - ReadWriteOnce

alertmanager:
  persistentVolume:
    enabled: true
    storageClass: "gp2" # <-- Update this for Alertmanager as well if needed
    size: 2Gi
    accessModes:
      - ReadWriteOnce
```

Here, replace `"gp2"` with the actual storage class you want to use (e.g., `gp2`, `standard`, `ebs-sc`).

#### 3. **Install or Upgrade Prometheus with Helm**

If you already have Prometheus installed and want to upgrade the storage class, you can use the following Helm commands:

##### a. **Install Prometheus with updated storage class**

If you are installing Prometheus for the first time and have created a `values.yaml` file:

```bash
helm install prometheus prometheus-community/prometheus \
  --namespace monitoring --create-namespace \
  -f values.yaml
```

##### b. **Upgrade Prometheus with updated storage class**

If Prometheus is already installed, and you want to update the storage class, use the following command:

```bash
helm upgrade prometheus prometheus-community/prometheus \
  --namespace monitoring \
  -f values.yaml
```

#### 4. **Using `--set` Flag to Update Storage Class**

If you don't want to use a `values.yaml` file, you can pass the storage class directly in the `helm install` or `helm upgrade` command with the `--set` flag.

```bash
helm install prometheus prometheus-community/prometheus \
  --namespace monitoring --create-namespace \
  --set server.persistentVolume.storageClass="gp2" \
  --set alertmanager.persistentVolume.storageClass="gp2"
```

For upgrading an existing release:

```bash
helm upgrade prometheus prometheus-community/prometheus \
  --namespace monitoring \
  --set server.persistentVolume.storageClass="gp2" \
  --set alertmanager.persistentVolume.storageClass="gp2"
```
helm upgrade prometheus prometheus-community/prometheus \
  --namespace monitoring \
  --set alertmanager.persistentVolume.storageClass="gp2"
Replace `gp2` with the appropriate storage class for your cluster.

#### 5. **Verify the Storage Class**

After installing or upgrading, verify that the PVCs created for Prometheus are using the correct storage class:

```bash
kubectl get pvc -n monitoring
```

Check the `STORAGECLASS` column to ensure it reflects the storage class you specified.

### Summary

- To update the storage class for Prometheus, modify the `server.persistentVolume.storageClass` and `alertmanager.persistentVolume.storageClass` in the `values.yaml` file or use the `--set` flag during the `helm install` or `helm upgrade` process.
- Ensure that Prometheus is deployed or updated with the correct storage configuration.
- Verify that the PVCs reflect the new storage class using `kubectl get pvc`.

This approach allows you to configure Prometheus with a different storage class suited to your environment, whether you're using AWS EBS, GCE PD, or other storage solutions.

The error message you're seeing, `dial tcp [::1]:9090: connect: connection refused`, indicates that a connection to the Prometheus API running on `localhost:9090` failed. This could happen for several reasons. Below are some possible causes and steps to resolve this issue.

### Possible Causes and Fixes

#### 1. **Prometheus is Not Running**
Prometheus may not be running or may not have started correctly. You can check the status of the Prometheus pods in your cluster:

```bash
kubectl get pods -n monitoring
```

Look for the Prometheus pod and check if it is running.

If the Prometheus pod is not running or is in an error state, check the logs for more information:

```bash
kubectl logs prometheus-server-0 -n monitoring
```

Replace `prometheus-server-0` with the actual pod name if it's different.

#### 2. **Prometheus Server is Listening on a Different Address**
By default, Prometheus listens on port `9090` on `localhost`. However, the server may be running on a different host or IP, especially if it's deployed in a Kubernetes cluster.

To find the correct endpoint for Prometheus, use:

```bash
kubectl get svc -n monitoring
```

This will list the services running in the `monitoring` namespace. Look for the `prometheus-server` or similar service, and check the `CLUSTER-IP` and `PORT(S)` columns.

If Prometheus is not running on `localhost`, you'll need to use the correct address when querying the API, for example:

```bash
http://<prometheus-service-ip>:9090/api/v1/query
```

You can also forward the port to your local machine using `kubectl port-forward`:

```bash
kubectl port-forward svc/prometheus-server 9090:9090 -n monitoring
```

This will allow you to access Prometheus at `http://localhost:9090`.

#### 3. **Prometheus Pod Restart or Crash**
If Prometheus restarted or crashed, there might be issues with configuration, persistent storage, or resource limits. Check if the pod has restarted recently:

```bash
kubectl describe pod prometheus-server-0 -n monitoring
```

Look for any events indicating a crash or a restart, such as resource limits being exceeded or an out-of-memory error.

#### 4. **Firewall or Network Issue**
If Prometheus is running on a different node or network, there could be network policies or firewalls preventing access to port `9090`. Make sure that Prometheus is accessible from your machine or from the service/pod querying the API.

#### 5. **Prometheus Configuration Issue**
If Prometheus is running but cannot respond to API requests, there may be an issue with the Prometheus configuration.

Check the Prometheus configuration file (typically `prometheus.yml`) to ensure that it’s set up correctly and includes all required targets and scraping rules.

#### 6. **Verify Prometheus Endpoint**
Make sure Prometheus is accessible by directly querying the `/api/v1/status` endpoint to test whether Prometheus is responding:

```bash
curl http://localhost:9090/api/v1/status
```

If Prometheus is up, this should return status information. If not, you'll get a connection error, confirming that Prometheus is down or unreachable.

### Troubleshooting Steps

1. **Check Prometheus pod status**: `kubectl get pods -n monitoring`
2. **Check Prometheus logs**: `kubectl logs prometheus-server-0 -n monitoring`
3. **Check Prometheus service IP/port**: `kubectl get svc -n monitoring`
4. **Port-forward to localhost**: `kubectl port-forward svc/prometheus-server 9090:9090 -n monitoring`
5. **Verify connection**: `curl http://localhost:9090/api/v1/status`

### Summary
- Ensure that Prometheus is running by checking the pods in your `monitoring` namespace.
- Check if Prometheus is listening on a different IP or port, and use that address for API requests.
- Verify the service configuration and that network access is available.
- Look at the Prometheus logs to diagnose crashes or restarts.
  
These steps should help you diagnose and resolve the issue with Prometheus refusing connections.