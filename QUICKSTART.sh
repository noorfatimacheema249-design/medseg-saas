#!/bin/bash

echo "🚀 MedImaging Segmentation - Quick Start"
echo "========================================"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Install from https://docker.com"
    exit 1
fi

echo "✓ Docker found"

# Check Node
if ! command -v node &> /dev/null; then
    echo "⚠️  Node not found. Frontend won't work locally."
fi

# Build
echo ""
echo "Building Docker image..."
cd docker
docker-compose up --build

echo ""
echo "✓ Done! Your app is running at:"
echo "  🌐 Frontend: http://localhost:3000"
echo "  🔧 API: http://localhost:8000"
echo "  📊 API Docs: http://localhost:8000/docs"
