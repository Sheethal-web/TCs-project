# Deploying the Smart AI Manager to AWS (Using ECS Express)

*Note: As of April 2026, AWS has deprecated App Runner. We will now use **Amazon ECS Express Mode**, which is the modern, highly scalable replacement!*

---

## Prerequisites
1. You must have your code pushed to GitHub (e.g., `TCs-project`).
2. I have added two new files to your repository: `Dockerfile.backend` and `Dockerfile.ml`. These are required for ECS! **Please commit and push these files to GitHub before starting.**

---

## Phase 1: Deploy the "Python ML Engine" (The Brain)
We will deploy the Python Machine Learning API to **Amazon ECS Express**. ECS reads the `Dockerfile.ml` and handles everything else.

1. Go to your **AWS Console** and search for **ECS** (Elastic Container Service).
2. Click **Create cluster** -> Name it `SmartAI-Cluster` -> Click **Create**.
3. Once the cluster is ready, click into it and click **Create Service** (Make sure you are using the new **ECS Express** UI toggle at the top if prompted).
4. **Source:** Select **GitHub** and authorize your account. Choose `TCs-project`.
5. **Branch:** `main`
6. **Container Build:** 
   * Select **Dockerfile**.
   * Dockerfile path: type `Dockerfile.ml`
7. **Environment:** 
   * Container Port: `8000`
8. Click **Deploy**.

**Wait 5 minutes.** ECS will build the container and provide you with a Load Balancer URL or Public Service URL. 
*Copy this URL! This is your `PYTHON_API_URL`.*

---

## Phase 2: Deploy the "Node.js Backend" (The Orchestrator)
Now we deploy the Node.js server to the exact same cluster.

1. Inside your `SmartAI-Cluster`, click **Create Service** again.
2. **Source:** Select **GitHub** and choose `TCs-project` (`main` branch).
3. **Container Build:**
   * Select **Dockerfile**.
   * Dockerfile path: type `Dockerfile.backend`
4. **Environment:**
   * Container Port: `5000`
5. **Advanced Settings / Environment Variables:**
   * Key: `PYTHON_API_URL`
   * Value: Paste the URL from Phase 1!
6. Click **Deploy**.

**Wait 5 minutes.** ECS will provide you with a second public URL for the backend. 
*Copy this URL! This is your `NODE_BACKEND_URL`.*

---

## Phase 3: Deploy the "React Dashboard" (The Frontend)
We will continue to use **AWS Amplify** for the frontend, as it is still the best tool for React websites.

1. In the AWS Console, search for **AWS Amplify**.
2. Click **Host web app** (or Create new app).
3. Connect your GitHub and select `TCs-project`.
4. **Environment Variables (Advanced Settings):**
   * Key: `VITE_API_URL`
   * Value: Paste your `NODE_BACKEND_URL` from Phase 2!
5. Click **Save and deploy**.

**Wait 3 minutes.** Amplify will give you a live website link. Click it. Your dashboard is now live on the internet!

---

## Phase 4: Connect the Physical Raspberry Pi
1. Open `ml_models/rpi_camera_client.py` on your Raspberry Pi.
2. Scroll to the bottom: `AWS_CLOUD_URL = "http://localhost:5000"`
3. Change it to your `NODE_BACKEND_URL` from Phase 2.
   *(Example: `AWS_CLOUD_URL = "http://your-ecs-loadbalancer-url.us-east-1.elb.amazonaws.com"`)*
4. Run the script on the Pi: `python rpi_camera_client.py`

You are now fully deployed on modern AWS infrastructure!
