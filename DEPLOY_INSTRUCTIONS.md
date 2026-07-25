# Deploy in 10 Minutes

## Option 1: Hugging Face Spaces (EASIEST - 10 minutes, FREE)

### Step 1: Create GitHub Repo
```bash
cd medseg-saas
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/medseg-saas.git
git push -u origin main
```

### Step 2: Create HF Space
1. Go to https://huggingface.co/spaces/new
2. Create space:
   - Name: `medseg-saas`
   - Visibility: Public
   - Runtime: **Docker**
3. Click Create Space

### Step 3: Connect Repo
1. In your HF Space, go to Files → Connect Repository
2. Paste your GitHub repo URL
3. HF auto-detects Dockerfile and deploys

### Step 4: Get URL
Your live app: `https://YOUR_USERNAME-medseg-saas.hf.space`

**That's it. Your app is live.**

---

## Option 2: AWS EC2 (PRODUCTION - 30 minutes, $500/month)

```bash
# 1. Create EC2 instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type g4dn.xlarge \
  --region us-east-1 \
  --key-name YOUR_KEY

# 2. SSH into instance
ssh -i YOUR_KEY.pem ubuntu@YOUR_INSTANCE_IP

# 3. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 4. Clone and run
git clone https://github.com/YOUR_USERNAME/medseg-saas
cd medseg-saas
docker build -f docker/Dockerfile -t medseg .
docker run -d -p 8000:8000 --gpus all medseg

# 5. Access at http://YOUR_INSTANCE_IP:8000
```

---

## Option 3: Local + Ngrok (TESTING ONLY - 5 minutes, FREE)

```bash
# Terminal 1
cd medseg-saas
docker-compose up

# Terminal 2
ngrok http 8000

# Get public URL and share
```

---

## Verify Deployment

```bash
curl https://your-deployed-url/health
# Should return: {"status":"healthy", ...}
```

---

## Your Live URL

After deployment, you'll have a URL like:
- HF: `https://username-medseg-saas.hf.space`
- AWS: `http://your-instance-ip:8000`

Update `landing.html` with this URL and share everywhere.

