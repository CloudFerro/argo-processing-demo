## Demo material for CloudFerro "Earth Observation meets Kubernetes" webinar on 22 march 2022.

For detailed walk-through refer to the webinar. Note that efore running the `eoworkflow-volumes.yaml` workflow, apply the `executor` role and respective rolebinding.
Also, apply the `secrets.yaml` with your actual S3 credentials filled in. Commands for applying these artifacts:
```
kubectl apply -f secrets.yaml -n argo
kubectl apply -f argo-executor-role.yaml -n argo
kubectl create rolebinding executorrolebinding --role executor --serviceaccount argo:argo -n argo
```