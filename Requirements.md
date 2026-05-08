# Homework #3 - Simple DL Workflow in Kubeflow

## 1. Objective
Develop Container and Kubernetes artifacts to perform Deep Learning (DL) training and DL inference hosting in GKE (Google Kubernetes Engine). This work demands a self-driven deep dive into Kubernetes and Kubeflow concepts and components.

## 2. Architecture Aspects & Requirements
### Application Containers
* **Training:** Requires a training program, a container definition file (`Dockerfile`), and a training job YAML file.
* **Inference:** Requires an inference program, a `Dockerfile`, a service YAML file, and a deployment YAML file.
* **Model Storage:** Both training and inference programs must be able to store and load the trained model persistently.

### User Interaction & Serving
* Host a URL to allow interaction with the User.
* Give any input to the inference engine (e.g., a number, a space bar, an image file, or an image ID in the data set) to demonstrate that the inference is happening in an interactive/controlled manner.

### Persistent Storage (PVC) - Optional
* If required, after creating your cluster, you can create a PVC resource via: `GCP -> Kubernetes Engine -> Storage -> Persistent storage volume`.

## 3. The Abstracted Workflow
* **Training Phase:** `Training Data` -> `Training Code` -> `Model`
    * *Artifacts Required:* `Dockerfile`, `K8s-yaml` (Job, Volume)
* **Inference Phase:** `Inference Code` -> `Web-serving`
    * *Artifacts Required:* `Dockerfile`, `K8s-yaml` (Deployment, Volume, Service)
    * *I/O Workflow:* Takes `Inference Input` and produces `Inference Output`

## 4. Submission Deliverables
* `Dockerfile`
* `K8S yaml` files
* Instructions on how to build and run the service on K8S clusters on GCP-GKE.
* Screen captures demonstrating how the application runs.
* Documentation of your work and a report on your experiences (e.g., *What Kubernetes controllers did you use for training and inference and why?*).

## 5. Grading Rubric (Total Score: 100)

| Category | Partial Score | Deduction Rules |
| :--- | :--- | :--- |
| **Created k8s cluster** | 40 | Deduct 4 for not providing a reasonable amount of proof of work. |
| **Training in k8s** | 30 | Deduct 2 for missing any of the steps: dockerfile, docker push, train-yaml, model saving. |
| **Inferencing in k8s** | 25 | Deduct 2 for missing any of the steps: PVC creation and preparation, code augmentation, dockerfile, infer-yaml, infer-test. |
| **Writing** | 5 | Up to 2 point deduction if there is a lack of attention to have readers to follow. |

## 6. Example: Adding a GPU to a K8S Cluster
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox
    command: ['sh', '-c', 'echo Hello Kubernetes! && sleep 36']
    resources:
      limits:
        [nvidia.com/gpu](https://nvidia.com/gpu): 1
  nodeSelector:
    [cloud.google.com/gke-accelerator](https://cloud.google.com/gke-accelerator): nvidia-tesla-t4


## 7. Example References
Check k8s-master folder for example code.