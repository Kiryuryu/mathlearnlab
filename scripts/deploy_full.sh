#!/bin/bash
# ECS deploy script — run on local machine to update ECS
set -e

HOST="root@8.137.78.250"
PASS="Tickingaway997-"
APP_DIR="/opt/apps/mathlearnlab"

echo "=== Deploying MathLearnLab to ECS ==="

# 1. Copy files
echo "[1/4] Copying server files..."
expect <<'EOF' > /dev/null
set timeout 60
spawn scp -o StrictHostKeyChecking=no -r server/models server/routers server/services server/main.py server/config.py requirements.txt root@8.137.78.250:/opt/apps/mathlearnlab/server/
expect "password:" { send "Tickingaway997-\r" }
expect eof
EOF

expect <<'EOF' > /dev/null
set timeout 60
spawn scp -o StrictHostKeyChecking=no -r client/build/web root@8.137.78.250:/opt/apps/mathlearnlab/client/build/
expect "password:" { send "Tickingaway997-\r" }
expect eof
EOF

expect <<'EOF' > /dev/null
set timeout 30
spawn scp -o StrictHostKeyChecking=no nginx.conf root@8.137.78.250:/etc/nginx/conf.d/mathlearnlab.conf
expect "password:" { send "Tickingaway997-\r" }
expect eof
EOF

expect <<'EOF' > /dev/null
set timeout 30
spawn scp -o StrictHostKeyChecking=no requirements.txt root@8.137.78.250:/opt/apps/mathlearnlab/requirements.txt
expect "password:" { send "Tickingaway997-\r" }
expect eof
EOF

# 2. Install deps & restart
echo "[2/4] Installing deps & restarting API..."
expect <<'EOF'
set timeout 180
spawn ssh -o StrictHostKeyChecking=no root@8.137.78.250 {source /opt/apps/mathlearnlab/venv/bin/activate && pip install python-jose -q 2>&1 | tail -2 && echo PIP_OK && systemctl restart mathlearnlab && sleep 3 && systemctl status mathlearnlab --no-pager}
expect "password:" { send "Tickingaway997-\r" }
expect eof
EOF

# 3. Reload nginx
echo "[3/4] Reloading nginx..."
expect <<'EOF'
set timeout 30
spawn ssh -o StrictHostKeyChecking=no root@8.137.78.250 {nginx -t && systemctl reload nginx && echo NGINX_OK}
expect "password:" { send "Tickingaway997-\r" }
expect eof
EOF

# 4. Verify
echo "[4/4] Verifying..."
curl -s http://8.137.78.250/api/health && echo ""
curl -s -o /dev/null -w "Flutter Web: %{http_code}\n" http://8.137.78.250/

echo "=== Deploy complete! ==="
