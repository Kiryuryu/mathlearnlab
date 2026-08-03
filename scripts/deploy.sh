#!/bin/bash
# MathLearnLab deploy script — run ON THE SERVER after code is pushed to git.
# Pulls latest code, installs backend deps, restarts services.
# Usage (on ECS): bash scripts/deploy.sh
set -e

APP_DIR="/opt/apps/mathlearnlab"
cd "$APP_DIR"

echo "=== MathLearnLab Deploy (server-side) ==="
echo "[1/4] Pulling latest code..."
git pull origin main

echo "[2/4] Installing Python dependencies..."
source venv/bin/activate
pip install -r requirements.txt -q

echo "[3/4] Restarting FastAPI..."
sudo systemctl restart mathlearnlab

echo "[4/4] Reloading Nginx..."
sudo cp nginx.conf /etc/nginx/conf.d/mathlearnlab.conf
sudo nginx -t && sudo systemctl reload nginx

echo "=== Deploy complete! ==="
sudo systemctl status mathlearnlab --no-pager | head -5

# Note: The Vue SPA is built locally (frontend/ -> server/static-spa) and uploaded
# via scripts/deploy_full.sh. This script handles backend code + nginx only.
