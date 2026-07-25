#!/bin/bash

# One-command AWS deployment
# Prerequisites: AWS account, Docker, jq

set -e

echo "🚀 Deploying to AWS EC2..."
echo ""

# Configuration
INSTANCE_TYPE="g4dn.xlarge"
KEY_NAME="medseg-key"
REGION="us-east-1"

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Install from https://aws.amazon.com/cli/"
    exit 1
fi

# Create key pair
echo "Creating SSH key..."
aws ec2 create-key-pair --key-name $KEY_NAME --region $REGION --query 'KeyMaterial' --output text > $KEY_NAME.pem
chmod 400 $KEY_NAME.pem

# Launch instance
echo "Launching EC2 instance..."
INSTANCE_ID=$(aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type $INSTANCE_TYPE \
  --key-name $KEY_NAME \
  --region $REGION \
  --query 'Instances[0].InstanceId' \
  --output text)

echo "Instance ID: $INSTANCE_ID"
echo "Waiting for instance to start..."
sleep 30

# Get public IP
IP=$(aws ec2 describe-instances \
  --instance-ids $INSTANCE_ID \
  --region $REGION \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)

echo "Instance IP: $IP"
echo ""
echo "SSH into instance:"
echo "  ssh -i $KEY_NAME.pem ubuntu@$IP"
echo ""
echo "Then run:"
echo "  curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh"
echo "  git clone https://github.com/yourname/medseg-saas"
echo "  cd medseg-saas"
echo "  docker build -f docker/Dockerfile -t medseg ."
echo "  docker run -d -p 8000:8000 --gpus all medseg"
echo ""
echo "Your app will be at: http://$IP:8000"
