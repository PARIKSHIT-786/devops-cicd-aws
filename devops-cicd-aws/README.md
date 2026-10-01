# CI/CD Pipeline: Jenkins, Docker, Ansible and Terraform on AWS EC2

A small Flask app delivered through a complete CI/CD pipeline. Every push is tested, built into a Docker image, pushed to Docker Hub, and deployed to an AWS EC2 instance automatically. The EC2 server itself is created with Terraform.

## Architecture

```
Developer --git push--> GitHub --> Jenkins
                                     |  1. Run pytest
                                     |  2. Build Docker image
                                     |  3. Push to Docker Hub
                                     |  4. Run Ansible playbook
                                     v
                               AWS EC2 (Ubuntu 22.04, created by Terraform)
                               Docker container -> port 80 -> Flask/Gunicorn :5000
```

## Tech stack

| Area | Tool |
|---|---|
| App | Python, Flask, Gunicorn, pytest |
| Containers | Docker (non-root user, HEALTHCHECK) |
| CI/CD | Jenkins (declarative pipeline) |
| Config management | Ansible |
| Infrastructure as Code | Terraform |
| Cloud | AWS EC2, Security Groups |

## Repository layout

```
app/            Flask app, tests, requirements
Dockerfile      Container image definition
Jenkinsfile     Pipeline: test, build, push, deploy
ansible/        Deployment playbook and inventory example
terraform/      EC2 instance and security group
```

## How to run it

**Prerequisites:** AWS account (Free Tier), AWS CLI configured, Terraform, a Docker Hub account, an EC2 key pair, and a Jenkins server with Docker, Python 3, and Ansible installed (a local Jenkins in Docker works fine).

1. **Create the server**
   ```bash
   cd terraform
   terraform init
   terraform apply -var="key_name=YOUR_KEY_PAIR" -var="my_ip_cidr=YOUR_IP/32"
   ```
   Note the `public_ip` output.

2. **Set up the inventory**
   ```bash
   cp ansible/inventory.ini.example ansible/inventory.ini
   # replace EC2_PUBLIC_IP with the Terraform output
   ansible-galaxy collection install -r ansible/requirements.yml
   ```

3. **Configure Jenkins**
   - Add credentials: `dockerhub-creds` (username and password/token) and `ec2-ssh-key` (SSH private key, user `ubuntu`).
   - Install the *SSH Agent* plugin.
   - Edit `DOCKERHUB_USER` in the `Jenkinsfile`.
   - Create a Pipeline job pointing at this repo.

4. **Run the pipeline**, then open `http://<EC2_PUBLIC_IP>/`. You should see JSON with the build number as `version`.

5. **Clean up** to avoid charges:
   ```bash
   cd terraform && terraform destroy
   ```

## What I learned / design decisions

- Image tags use the Jenkins build number, so every deployment is traceable and can be rolled back.
- The playbook is idempotent: re-running it only changes what is needed.
- SSH is limited to my IP in the security group, and the container runs as a non-root user.
- The playbook waits on the `/health` endpoint, so a failed deployment fails the pipeline.

## Possible improvements

- Trigger builds automatically with a GitHub webhook.
- Add Prometheus and Grafana monitoring.
- Move to Kubernetes (EKS or minikube) with rolling updates.
- Store Terraform state remotely in S3.
