#!/usr/bin/env python3
"""Check remote API. Credentials from env vars: DEPLOY_HOST/DEPLOY_USER/DEPLOY_PASS"""
import os, paramiko, json

HOST = os.environ.get('DEPLOY_HOST', '8.137.78.250')
USER = os.environ.get('DEPLOY_USER', 'root')
PASS = os.environ.get('DEPLOY_PASS', '')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS)

_, stdout, stderr = ssh.exec_command('curl -s http://127.0.0.1:8000/api/museum/exhibits')
data = json.loads(stdout.read().decode())
lim = data['exhibits']['limits']
print('Keys:', list(lim.keys()))
print('Has en:', 'en' in lim)
print('Has big_question_en:', 'big_question_en' in lim)
if 'en' in lim:
    print('en:', lim['en'])

ssh.close()
