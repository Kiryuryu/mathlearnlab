#!/bin/bash
# ECS deploy script — run on local machine to update ECS
# Credentials from env vars (never commit secrets): DEPLOY_HOST / DEPLOY_USER / DEPLOY_PASS
set -e

HOST="${DEPLOY_HOST:-8.137.78.250}"
USER="${DEPLOY_USER:-root}"
PASS="${DEPLOY_PASS:?DEPLOY_PASS env var is required}"
SSH_HOST="${USER}@${HOST}"
APP_DIR="/opt/apps/mathlearnlab"

echo "=== Deploying MathLearnLab to ECS ==="

# 1. Copy files
echo "[1/4] Copying server files..."
expect <<EOF > /dev/null
set timeout 60
spawn scp -o StrictHostKeyChecking=no -r server/models server/routers server/services server/main.py server/config.py requirements.txt ${SSH_HOST}:${APP_DIR}/server/
expect "password:" { send "${PASS}\r" }
expect eof
EOF

expect <<EOF > /dev/null
set timeout 60
spawn scp -o StrictHostKeyChecking=no -r client/build/web ${SSH_HOST}:${APP_DIR}/client/build/
expect "password:" { send "${PASS}\r" }
expect eof
EOF

expect <<EOF > /dev/null
set timeout 30
spawn scp -o StrictHostKeyChecking=no nginx.conf ${SSH_HOST}:/etc/nginx/conf.d/mathlearnlab.conf
expect "password:" { send "${PASS}\r" }
expect eof
EOF

expect <<EOF > /dev/null
set timeout 30
spawn scp -o StrictHostKeyChecking=no requirements.txt ${SSH_HOST}:${APP_DIR}/requirements.txt
expect "password:" { send "${PASS}\r" }
expect eof
EOF

# 2. Install deps & restart
echo "[2/4] Installing deps & restarting API..."
expect <<EOF
set timeout 180
spawn ssh -o StrictHostKeyChecking=no ${SSH_HOST} {source ${APP_DIR}/venv/bin/activate && pip install python-jose -q 2>&1 | tail -2 && echo PIP_OK && systemctl restart mathlearnlab && sleep 3 && systemctl status mathlearnlab --no-pager}
expect "password:" { send "${PASS}\r" }
expect eof
EOF

# 3. Reload nginx
echo "[3/4] Reloading nginx..."
expect <<EOF
set timeout 30
spawn ssh -o StrictHostKeyChecking=no ${SSH_HOST} {nginx -t && systemctl reload nginx && echo NGINX_OK}
expect "password:" { send "${PASS}\r" }
expect eof
EOF

# 4. Verify
echo "[4/4] Verifying..."
curl -s http://${HOST}/api/health && echo ""
curl -s -o /dev/null -w "Flutter Web: %{http_code}\n" http://${HOST}/

echo "=== Deploy complete! ==="
