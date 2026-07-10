#!/bin/bash
# MathLearnLab deploy script for Alibaba Cloud ECS
# Usage: bash scripts/deploy.sh

set -e

APP_DIR="/opt/apps/mathlearnlab"
cd "$APP_DIR"

echo "=== MathLearnLab Deploy ==="
echo "[1/5] Pulling latest code..."
git pull origin main

echo "[2/5] Installing Python dependencies..."
source venv/bin/activate
pip install -r requirements.txt -q

echo "[3/5] Building Flutter Web..."
cd client
flutter pub get
flutter build web --release
cd ..

echo "[4/5] Restarting FastAPI..."
sudo systemctl restart mathlearnlab

echo "[5/5] Reloading Nginx..."
sudo cp nginx.conf /etc/nginx/conf.d/mathlearnlab.conf
sudo nginx -t && sudo systemctl reload nginx

echo "=== Deploy complete! ==="
sudo systemctl status mathlearnlab --no-pager
