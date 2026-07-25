#!/bin/bash

set -e

echo "🚀 Pushing MedImaging to GitHub"
echo "=================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Install from https://git-scm.com"
    exit 1
fi

# Get GitHub username
read -p "GitHub username: " GITHUB_USER
read -p "GitHub Personal Access Token (or press Enter for SSH): " GITHUB_TOKEN

echo ""
echo "Creating GitHub repo..."
echo "1. Go to: https://github.com/new"
echo "2. Create repo named: medseg-saas"
echo "3. DO NOT initialize with README"
echo "4. Click 'Create repository'"
echo ""
read -p "Press Enter when done creating the repo..."

echo ""
echo "Pushing code to GitHub..."

# Initialize git
git init
git config user.email "noor@medseg.app"
git config user.name "MedImaging"

# Add all files
git add .

# First commit
git commit -m "Initial commit: Medical imaging segmentation SaaS"

# Add remote
if [ -z "$GITHUB_TOKEN" ]; then
    # Use SSH
    echo "Using SSH (make sure you have SSH keys set up)"
    git remote add origin git@github.com:$GITHUB_USER/medseg-saas.git
else
    # Use HTTPS with token
    git remote add origin https://$GITHUB_USER:$GITHUB_TOKEN@github.com/$GITHUB_USER/medseg-saas.git
fi

# Push to main
git branch -M main
git push -u origin main

echo ""
echo "✅ Success!"
echo ""
echo "Your repo: https://github.com/$GITHUB_USER/medseg-saas"
echo ""
echo "Next step: Deploy to Hugging Face Spaces"
echo "1. Go to https://huggingface.co/spaces/new"
echo "2. Name: medseg-saas"
echo "3. Runtime: Docker"
echo "4. Connect your GitHub repo"
echo "5. HF auto-deploys!"
echo ""
