Description:

Steps to run (on local):

Prerequisites: Docker, minikube, kubectl installed

1. Build the main Django app
`docker build . -t luungoc2005/mobile-wallet-test`

2. Deploy onto minikube
`kubectl apply -f ./k8s/local/django`
`kubectl apply -f ./k8s/local/postgres`