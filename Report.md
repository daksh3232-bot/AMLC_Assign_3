# Homework #3 - Simple DL Workflow in GKE
**Student Name:** [Your Name]
**Project ID:** `coms6998-amlc-da3232`

## 1. Objective
The goal of this project was to develop a complete Deep Learning workflow on Google Kubernetes Engine (GKE), encompassing containerization, persistent storage management, GPU-accelerated training, and interactive web serving.

## 2. Technical Architecture & Decisions

### Kubernetes Controllers Used
*   **Training (Kubernetes Job):** I used a `Job` controller for the training phase. 
    *   *Why?* Training is a "run-to-completion" task. Unlike a web server, it has a clear end state. A `Job` ensures that the pod runs until the training script finishes successfully and then stops, releasing the GPU resources.
*   **Inference (Kubernetes Deployment):** I used a `Deployment` controller for the inference hosting.
    *   *Why?* Inference requires a "long-running" service that is always available to handle user requests. A `Deployment` provides features like self-healing (restarting the pod if it crashes) and easy scaling.
*   **Networking (Kubernetes Service - LoadBalancer):** A `Service` of type `LoadBalancer` was used to expose the inference engine to the public internet via a Google Cloud Load Balancer.

### Storage Strategy
I utilized a **Persistent Volume Claim (PVC)** with a `ReadWriteOnce` access mode. This allowed the Training Job to write the trained model (`model.pth`) to a persistent disk, which was then mounted by the Inference Deployment. This decoupled the training and inference phases, ensuring the model persisted even after the training pod was deleted.

### Infrastructure & Security
Due to project-level security constraints (Org Policy: `compute.vmExternalIpAccess`), the cluster was provisioned as a **Private GKE Cluster** with internal-only IPs for the nodes. This ensured compliance with security requirements while still allowing the Load Balancer to provide an external endpoint for user interaction.

---

## 3. How to Build and Run

### Prerequisites
*   A GCP project with GKE, Artifact Registry, and Compute Engine APIs enabled.
*   A development VM with Docker, `gcloud` SDK, and `kubectl` installed.

### Step 1: Build and Push Images
```bash
# Build images
docker build -t asia-east1-docker.pkg.dev/[PROJECT_ID]/ml-images/mnist-train:latest -f Dockerfile.train .
docker build -t asia-east1-docker.pkg.dev/[PROJECT_ID]/ml-images/mnist-inference:latest -f Dockerfile.inference .

# Push to Artifact Registry
docker push asia-east1-docker.pkg.dev/[PROJECT_ID]/ml-images/mnist-train:latest
docker push asia-east1-docker.pkg.dev/[PROJECT_ID]/ml-images/mnist-inference:latest
```

### Step 2: Create the Infrastructure
```bash
gcloud container clusters create mnist-cluster \
    --num-nodes=1 \
    --machine-type=n1-standard-4 \
    --accelerator=type=nvidia-tesla-t4,count=1,gpu-driver-version=default \
    --zone=asia-east1-c \
    --enable-private-nodes \
    --master-ipv4-cidr=172.16.0.48/28 \
    --enable-ip-alias
```

### Step 3: Deploy to Kubernetes
```bash
# 1. Setup storage
kubectl apply -f pvc.yaml

# 2. Run Training
kubectl apply -f train-job.yaml

# 3. Launch Inference (after training completes)
kubectl apply -f inference-deployment.yaml
kubectl apply -f inference-service.yaml
```

---

## 4. Experience and Reflection
Setting up a GPU-accelerated workflow on GKE provided deep insights into the orchestration of specialized hardware. The primary challenges included managing GPU quotas and navigating strict Organization Policies regarding external IP addresses. Using a private cluster combined with a Load Balancer proved to be an effective architecture for balancing security and accessibility. The transition from a local development environment to a distributed Kubernetes environment highlighted the importance of robust containerization and shared persistent storage in ML pipelines.
