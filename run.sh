#!/bin/bash

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

kubectl get pods

minikube service timetable-manager --url