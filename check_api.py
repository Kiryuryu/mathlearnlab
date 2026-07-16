#!/usr/bin/env python3
import paramiko, json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.137.78.250', username='root', password='Tickingaway997-')

_, stdout, stderr = ssh.exec_command('curl -s http://127.0.0.1:8000/api/museum/exhibits')
data = json.loads(stdout.read().decode())
lim = data['exhibits']['limits']
print('Keys:', list(lim.keys()))
print('Has en:', 'en' in lim)
print('Has big_question_en:', 'big_question_en' in lim)
if 'en' in lim:
    print('en:', lim['en'])

ssh.close()
