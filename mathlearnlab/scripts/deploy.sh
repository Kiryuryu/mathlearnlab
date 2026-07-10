#!/bin/bash
# MathLearnLab deploy script for Alibaba Cloud ECS
# Usage: bash scripts/deploy.sh

set -e

APP_DIR="/opt/apps/mathlearnlab"
cd "$APP_DIR"

echo "=== MathLearnLab Deploy ==="
echo "[1/4] Pulling latest code..."
git pull origin main

echo "[2/4] Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt -q

echo "[3/4] Converting notebooks..."
python scripts/convert_notebooks.py

echo "[4/4] Restarting service..."
sudo systemctl restart mathlearnlab

echo "=== Deploy complete! ==="
sudo systemctl status mathlearnlab --no-pager
