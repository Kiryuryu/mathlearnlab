#!/usr/bin/env python3
"""Check remote server config. Credentials from env vars: DEPLOY_HOST/DEPLOY_USER/DEPLOY_PASS"""
import os, paramiko, json

HOST = os.environ.get('DEPLOY_HOST', '8.137.78.250')
USER = os.environ.get('DEPLOY_USER', 'root')
PASS = os.environ.get('DEPLOY_PASS', '')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS)
sftp = ssh.open_sftp()

# Upload a remote script
remote_script = '/tmp/check_config.py'
local_script = '/tmp/remote_check.py'
with open(local_script, 'w') as f:
    f.write("""import json, sys
sys.path.insert(0, '/opt/apps/mathlearnlab')
from server.config import settings
lim = settings.exhibits['limits']
print('en' in lim)
if 'en' in lim:
    print('en:', lim['en'])
print('big_question_en' in lim)
print('Keys:', list(lim.keys()))
""")
sftp.put(local_script, remote_script)
sftp.close()

_, stdout, stderr = ssh.exec_command('cd /opt/apps/mathlearnlab && /opt/apps/mathlearnlab/venv/bin/python3 /tmp/check_config.py')
print(stdout.read().decode()[:1000])
err = stderr.read().decode()[:500]
if err: print('ERR:', err)
ssh.close()
