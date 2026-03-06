#!/bin/bash
set -e

echo "🎨 Deploying Frontend..."

# Navigate to frontend directory
cd "$(dirname "$0")"

# Install dependencies
echo "📦 Installing Node packages..."
npm install

# Build production build
echo "🔨 Building React app..."
npm run build

# Copy build to public_html
echo "📤 Copying build to public_html..."
mkdir -p ~/public_html
cp -r build/* ~/public_html/

echo "✅ Frontend deployment complete!"
