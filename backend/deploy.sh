#!/bin/bash
set -e

echo "🔧 Deploying Backend..."

# Navigate to backend directory
cd "$(dirname "$0")"

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install -r requirements.txt --upgrade

# Set permissions
chmod +x app.py

# Setup database (if needed)
if [ -f "database_schema.sql" ]; then
    echo "🗄️ Setting up database..."
    # Uncomment if using MySQL via cPanel
    # mysql -u $DB_USER -p$DB_PASS $DB_NAME < database_schema.sql
fi

echo "✅ Backend deployment complete!"
