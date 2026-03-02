#!/bin/bash
# Deploy script for Deepfake Voice Detection to Vercel
# Usage: ./deploy.sh

echo "======================================"
echo "Vercel Deployment Script"
echo "======================================"
echo ""

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "Vercel CLI is not installed."
    echo "Installing Vercel CLI globally..."
    npm install -g vercel
fi

echo "Starting deployment to Vercel..."
echo ""

# Deploy to Vercel
vercel --prod

echo ""
echo "======================================"
echo "Deployment complete!"
echo "======================================"
