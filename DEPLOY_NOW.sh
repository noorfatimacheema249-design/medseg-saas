#!/bin/bash

echo "🚀 MedImaging - Automated Deployment"
echo "===================================="
echo ""

# Step 1: GitHub Setup
echo "Step 1: Create GitHub repo"
echo "1. Go to https://github.com/new"
echo "2. Create repo named: medseg-saas"
echo "3. Clone it locally and copy this folder contents into it"
echo "4. Run these commands in your repo:"
echo ""
echo "  git add ."
echo "  git commit -m 'Initial commit'"
echo "  git push origin main"
echo ""
read -p "Done? Press Enter to continue..."

# Step 2: HF Spaces Setup
echo ""
echo "Step 2: Create Hugging Face Space"
echo "1. Go to https://huggingface.co/spaces/new"
echo "2. Create Space:"
echo "   - Name: medseg-saas"
echo "   - Visibility: Public"
echo "   - Runtime: Docker"
echo "3. Copy your Space URL when created"
read -p "Enter your HF Space URL (e.g., https://huggingface.co/spaces/username/medseg-saas): " HF_SPACE_URL

# Step 3: Setup Deployment
echo ""
echo "Step 3: Setup automatic deployment"
echo "Go to GitHub repo → Settings → Secrets and variables → Actions"
echo "Add these secrets:"
echo ""
echo "  Name: HF_TOKEN"
echo "  Value: (get from https://huggingface.co/settings/tokens)"
echo ""
echo "  Name: HF_USERNAME"  
echo "  Value: your-huggingface-username"
echo ""
read -p "Done? Press Enter..."

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next time you push to GitHub, it auto-deploys to HF Spaces"
echo ""
echo "Your live URL will be:"
echo "$HF_SPACE_URL"
