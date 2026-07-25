# Deployment Guide

## Hugging Face Spaces (Fastest - 5 minutes)

### Step 1: Create Space
1. Go to https://huggingface.co/spaces/new
2. Create a new Space
3. Select "Docker" as the runtime
4. Name it: `medseg-saas`

### Step 2: Connect Repository
1. Clone this repo locally
2. Add HF as a remote:
```bash
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/medseg-saas
git push hf main
```

### Step 3: HF Spaces will automatically:
- Detect the `Dockerfile`
- Build the image
- Deploy at: `https://your-username-medseg-saas.hf.space`

**That's it!** Your app is live.

---

## AWS with EC2 (Production)

### Prerequisites
- AWS account
- EC2 instance (g4dn.xlarge recommended for GPU)
- Ubuntu 22.04 LTS AMI

### Steps

```bash
# SSH into instance
ssh -i key.pem ubuntu@your-instance-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clone repo
git clone https://github.com/yourusername/medseg-saas
cd medseg-saas

# Build & run
docker build -f docker/Dockerfile -t medseg .
docker run -d -p 8000:8000 --gpus all medseg

# Install nginx for reverse proxy
sudo apt install nginx -y
# Configure nginx to proxy to localhost:8000
```

---

## Local with Ngrok (Testing)

Make your local machine accessible online:

```bash
# Install ngrok
curl https://ngrok-agent.s3.amazonaws.com/ngrok-v3-stable-linux-amd64.zip -o ngrok.zip
unzip ngrok.zip

# Run locally
docker-compose up

# In another terminal, expose to internet
./ngrok http 8000
# Get public URL like: https://abc123.ngrok.io
```

---

## Environment Variables

Create `.env` file:

```
REACT_APP_API_URL=https://your-api-domain.com
MAX_FILE_SIZE=500  # MB
MODELS=liver,lung,spleen
```

---

## Health Checks

Monitor your deployment:

```bash
# Check if running
curl https://your-domain/health

# Check models available
curl https://your-domain/models

# Test segmentation
curl -X POST https://your-domain/segment \
  -F "file=@test.dcm" \
  -F "model_name=liver"
```

---

## Scaling

### For high volume (1000+ segmentations/day):

1. **Use GPU instance** (g4dn.2xlarge or larger)
2. **Add request queue** (Redis/Celery)
3. **Load balance** (nginx/HAProxy)
4. **Cache results** (similar images)

### Example setup:
```
Nginx (load balancer)
  ↓
[FastAPI Worker 1] + GPU 1
[FastAPI Worker 2] + GPU 2
[FastAPI Worker 3] + GPU 3
  ↓
Redis Queue
  ↓
Medical Images Storage (S3/GCS)
```

---

## Cost Estimates

| Platform | Instance Type | Monthly Cost |
|----------|---|---|
| HF Spaces | Free tier | $0 (limited) |
| AWS EC2 | g4dn.xlarge | $500/month |
| AWS EC2 | g4dn.2xlarge | $1000/month |
| Google Cloud | GPU VM | $400-800/month |

---

## Troubleshooting

**Issue**: CUDA out of memory
- Solution: Reduce batch size in `main.py` (sw_batch_size=2)

**Issue**: Long inference time
- Solution: Use GPU instance, not CPU

**Issue**: DICOM loading fails
- Solution: Ensure pydicom version matches requirements.txt

**Issue**: Frontend can't reach API
- Solution: Set CORS headers and check firewall
