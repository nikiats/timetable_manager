#!/bin/bash

docker build -t nikiatsik/timetable_manager:latest .

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

kubectl get pods

minikube service django-service --url