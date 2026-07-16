#!/usr/bin/env python3
import paramiko, json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.137.78.250', username='root', password='Tickingaway997-')
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
