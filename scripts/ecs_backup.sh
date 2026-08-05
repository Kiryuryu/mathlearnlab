#!/usr/bin/env bash
# MathLearnLab 每日备份脚本
# 备份 data/ 目录 + .env 配置到 /opt/backups/mathlearnlab/，保留最近 14 份
set -euo pipefail

SRC=/opt/apps/mathlearnlab/data
ENV_FILE=/opt/apps/mathlearnlab/.env
BACKUP_DIR=/opt/backups/mathlearnlab
KEEP=14
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# 备份数据目录（排除临时文件）
tar czf "$BACKUP_DIR/data_$DATE.tar.gz" \
  --exclude='data/daily/*' \
  --exclude='data/generated_problems/*' \
  -C /opt/apps/mathlearnlab data

# 备份 .env（含密钥，权限收紧）
if [ -f "$ENV_FILE" ]; then
  cp "$ENV_FILE" "$BACKUP_DIR/env_$DATE"
  chmod 600 "$BACKUP_DIR/env_$DATE"
fi

# 清理过期备份
ls -1t "$BACKUP_DIR"/data_*.tar.gz 2>/dev/null | tail -n +$((KEEP + 1)) | xargs -r rm -f
ls -1t "$BACKUP_DIR"/env_* 2>/dev/null | tail -n +$((KEEP + 1)) | xargs -r rm -f

# 记录日志
echo "$(date '+%F %T') backup OK $(ls -1 "$BACKUP_DIR" | wc -l) files" >> /var/log/mathlearnlab-backup.log

# 磁盘空间告警（备份后剩余空间不足 5GB 时）
AVAIL_GB=$(df -h / | awk 'NR==2 {print int($4)}')
if [ "$AVAIL_GB" -lt 5 ]; then
  echo "$(date '+%F %T') WARN 磁盘剩余仅 ${AVAIL_GB}G" >> /var/log/mathlearnlab-backup.log
fi
