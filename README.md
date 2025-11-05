# Kafka-k8s 

Running Kafka Producer, Consumer in the Kubernetes K8S on Openshift 

Link to the Openshift Web Console: 
https://console.apps.edu.nerc.mghpcc.org/


```bash
# openshift cli log in
oc login 
oc project

# kafka pvc, deployment, svc
oc apply -f k8s/kafka-data-persistentvolumeclaim.yaml
oc apply -f k8s/kafka-deployment.yaml
oc apply -f k8s/kafka-service.yaml

# build consumer producer image
oc apply -f k8s/buildconfig-producer.yaml
oc apply -f k8s/buildconfig-consumer.yaml

# optional: start build
oc start-build kafka-producer
oc start-build kafka-consumer

# producer, consumer deployment
oc apply -f k8s/producer-deployment.yaml
oc apply -f k8s/consumer-deployment.yaml
```