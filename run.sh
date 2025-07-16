#!/bin/bash

# сборка образа и применение конфигураций

minikube start

eval $(minikube -p minikube docker-env)

minikube image build -t timetable_manager .

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# смотрим адрес для доступа к веб приложению

kubectl get pods

kubectl get services

minikube ip
