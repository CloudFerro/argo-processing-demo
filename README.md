## Demo material for CloudFerro "Earth Observation meets Kubernetes" webinar on 22 march 2022.

For detailed walk-through refer to the webinar. 
With `eoworkflow-volumes.yaml` and `eoworkflow-emptydir.yaml`, apply `secrets.yaml` with your actual S3 credentials filled in. 
Additionally with `eoworkflow-volumes.yaml` workflow, apply the `executor` role and respective rolebinding.

Commands to apply these configurations:
```
kubectl apply -f secrets.yaml -n argo
kubectl apply -f argo-executor-role.yaml -n argo
kubectl create rolebinding executorrolebinding --role executor --serviceaccount argo:argo -n argo
```