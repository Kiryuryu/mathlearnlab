#!/bin/bash
# ECS deploy script — run on local machine to build the Vue SPA and push backend + frontend to ECS.
# Credentials from env vars (never commit secrets): DEPLOY_HOST / DEPLOY_USER / DEPLOY_PASS
set -e

HOST="${DEPLOY_HOST:-8.137.78.250}"
USER="${DEPLOY_USER:-root}"
PASS="${DEPLOY_PASS:?DEPLOY_PASS env var is required}"
SSH_HOST="${USER}@${HOST}"
APP_DIR="/opt/apps/mathlearnlab"

echo "=== Deploying MathLearnLab to ECS ==="

# 0. Build Vue frontend
echo "[0/4] Building Vue SPA..."
( cd frontend && npm run build )

# 1. Copy backend + frontend build
echo "[1/4] Copying files..."
expect <<EOF > /dev/null
set timeout 60
spawn scp -o StrictHostKeyChecking=no -r server/models server/routers server/services server/middleware.py server/config.py server/content_data.py server/main.py server/static-spa requirements.txt ${SSH_HOST}:${APP_DIR}/
expect "password:" { send "${PASS}\r" }
expect eof
EOF

# 2. Install deps, clear pycache & restart
echo "[2/4] Installing deps & restarting API..."
expect <<EOF
set timeout 180
spawn ssh -o StrictHostKeyChecking=no ${SSH_HOST} {find ${APP_DIR}/server -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null; source ${APP_DIR}/venv/bin/activate && pip install -r ${APP_DIR}/requirements.txt -q 2>&1 | tail -2 && systemctl restart mathlearnlab && sleep 3 && systemctl status mathlearnlab --no-pager | head -5}
expect "password:" { send "${PASS}\r" }
expect eof
EOF

# NOTE: nginx config (/etc/nginx/conf.d/mathlearnlab-ssl.conf) is managed manually,
# not uploaded here, to avoid clobbering the live SSL/CSP config with a stale local file.

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
curl -s https://${HOST}/api/health && echo ""
curl -s -o /dev/null -w "Site: %{http_code}\n" https://${HOST}/

echo "=== Deploy complete! ==="
