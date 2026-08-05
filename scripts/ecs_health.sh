#!/usr/bin/env bash
# MathLearnLab 健康监控脚本
# 检查：服务进程、API 健康、磁盘、内存。任一异常则写日志 + 尝试邮件告警。
set -uo pipefail

LOG=/var/log/mathlearnlab-health.log
PROBLEMS=""

check() {
  local name="$1" status="$2"
  echo "$(date '+%F %T') $name: $status" >> "$LOG"
  case "$status" in
    OK*) ;;
    *) PROBLEMS="${PROBLEMS}${name}: ${status}; " ;;
  esac
}
# 1. 服务 active
if systemctl is-active --quiet mathlearnlab; then
  check "service" "OK"
else
  check "service" "DOWN"
fi

# 2. API 健康
if curl -sf -m 10 http://127.0.0.1:8000/api/health > /dev/null 2>&1; then
  check "api" "OK"
else
  check "api" "FAIL"
fi

# 3. 磁盘（阈值 20%，即约 8GB 剩余）
USED_PCT=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
if [ "${USED_PCT:-100}" -lt 80 ]; then
  check "disk" "OK (${USED_PCT}%)"
else
  check "disk" "HIGH ${USED_PCT}%"
fi

# 4. 内存（available < 200MB 视为告警）
AVAIL_MB=$(free -m | awk 'NR==2 {print $7}')
if [ "${AVAIL_MB:-0}" -gt 200 ]; then
  check "memory" "OK (${AVAIL_MB}MB free)"
else
  check "memory" "LOW ${AVAIL_MB}MB free"
fi

# 5. 最近的备份存在（近 2 天内）
LATEST_BACKUP=$(ls -1t /opt/backups/mathlearnlab/data_*.tar.gz 2>/dev/null | head -1)
if [ -n "$LATEST_BACKUP" ] && [ "$(find "$LATEST_BACKUP" -mtime -2)" ]; then
  check "backup" "OK"
else
  check "backup" "MISSING"
fi

# 告警：写邮件脚本（若 SMTP 配置可用）
if [ -n "$PROBLEMS" ]; then
  MESSAGE="MathLearnLab 健康告警 @ $(date '+%F %T')

以下项目异常：
  $PROBLEMS

请登录服务器检查：ssh root@8.137.78.250
查看日志：journalctl -u mathlearnlab -n 100"
  if [ -f /opt/apps/mathlearnlab/.env ] && grep -q '^SMTP_HOST=' /opt/apps/mathlearnlab/.env; then
    python3 - <<PYEOF
import os, smtplib, re
from email.mime.text import MIMEText
env = {}
for line in open('/opt/apps/mathlearnlab/.env'):
    if '=' in line and not line.startswith('#'):
        k, v = line.strip().split('=', 1)
        env[k] = v.strip().strip('"\'')
host, user, pwd, to = env.get('SMTP_HOST'), env.get('SMTP_USER'), env.get('SMTP_PASS'), env.get('ADMIN_EMAIL')
if host and user and to:
    try:
        msg = MIMEText("""$MESSAGE""", 'plain', 'utf-8')
        msg['Subject'] = '[MathLearnLab] 服务异常告警'
        msg['From'] = user; msg['To'] = to
        s = smtplib.SMTP_SSL(host, 465, timeout=10)
        s.login(user, pwd); s.sendmail(user, [to], msg.as_string()); s.quit()
    except Exception as e:
        print('SMTP fail:', e)
PYEOF
  fi
  echo "$(date '+%F %T') ALERT: $PROBLEMS" >> "$LOG"
fi
