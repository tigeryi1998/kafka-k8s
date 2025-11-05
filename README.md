# Kafka-k8s 

Running Kafka Producer, Consumer in the Kubernetes K8S on Openshift 

Link to the Openshift Web Console: 
https://console.apps.edu.nerc.mghpcc.org/



✅ Create deployments, services (Kafka / Producer / Consumer)

```bash
# openshift cli log in
# https://oauth-openshift.apps.edu.nerc.mghpcc.org/oauth/token/display
oc login --token=<TOKEN> --server=https://api.edu.nerc.mghpcc.org:6443

oc project
# Using project "ds551-2025fall-cb9303" on server "https://api.edu.nerc.mghpcc.org:6443".

# kafka pvc, deployment, svc
# oc apply -f k8s/kafka-data-persistentvolumeclaim.yaml
oc apply -f k8s/kafka-service.yaml
oc apply -f k8s/kafka-deployment.yaml

# build image: consumer producer 
oc apply -f k8s/buildconfig-producer.yaml
oc apply -f k8s/buildconfig-consumer.yaml

# optional: start build (not needed for Git)
oc start-build kafka-producer
oc start-build kafka-consumer

# producer, consumer deployment
oc apply -f k8s/producer-deployment.yaml
oc apply -f k8s/consumer-deployment.yaml
```



✅ View Logs (Kafka / Producer / Consumer)

After deployments are running, you can stream logs to verify activity.

```bash
# list pods
oc get pods

# Replace <pod> with the Kafka pod name
oc logs <kafka-pod> 

# Find producer pod
oc get pods | grep producer

# Stream logs
oc logs <producer-pod> 

# Find consumer pod
oc get pods | grep consumer

# Stream logs
oc logs <consumer-pod> 
```


Scale Down Deployment

```bash
# Scale Kafka down to 0 replicas
oc scale deployment kafka --replicas=0

# Scale Producer down to 0 replicas
oc scale deployment kafka-producer --replicas=0

# Scale Consumer down to 0 replicas
oc scale deployment kafka-consumer --replicas=0
```


Scale Up Deployment

```bash
# Scale Kafka down to 1 replicas
oc scale deployment kafka --replicas=1

# Scale Producer down to 1 replicas
oc scale deployment kafka-producer --replicas=1

# Scale Consumer down to 1 replicas
oc scale deployment kafka-consumer --replicas=1
```



🗑️ Delete All Kafka-Related Resources
```bash
# Delete Deployments
oc delete deployment kafka kafka-producer kafka-consumer

# Delete Services
oc delete service kafka kafka-controller

# Delete BuildConfigs
oc delete bc kafka-producer kafka-consumer

# Optional: delete completed builds + images
oc delete builds --all
oc delete imagestreams kafka-producer kafka-consumer

# If you previously used PVC, delete it (no longer needed)
# oc delete pvc kafka-data
```

Or delete via yaml files
```bash
# Delete via YAML
oc delete -f k8s/consumer-deployment.yaml
oc delete -f k8s/producer-deployment.yaml
oc delete -f k8s/buildconfig-consumer.yaml
oc delete -f k8s/buildconfig-producer.yaml
oc delete -f k8s/kafka-deployment.yaml
oc delete -f k8s/kafka-service.yaml
```

Or delete all (Kafka + producer + consumer)
```bash
oc delete all -l app=kafka
oc delete all -l app=kafka-producer
oc delete all -l app=kafka-consumer
```