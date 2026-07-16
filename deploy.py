#!/usr/bin/env python3
import paramiko, os

HOST = '8.137.78.250'
USER = 'root'
PASS = 'Tickingaway997-'
BASE = '/opt/apps/mathlearnlab'

def ensure_dir(sftp, path):
    parts = path.strip('/').split('/')
    cur = '/'
    for p in parts:
        cur += p + '/'
        try: sftp.stat(cur)
        except: sftp.mkdir(cur)

def upload_tree(sftp, local_root, remote_root):
    for root, dirs, files in os.walk(local_root):
        rel = os.path.relpath(root, local_root)
        rdir = remote_root if rel == '.' else f'{remote_root}{rel}/'.replace('//','/')
        ensure_dir(sftp, rdir)
        for f in files:
            sftp.put(os.path.join(root, f), os.path.join(rdir, f).replace('\\', '/'))

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS)
sftp = ssh.open_sftp()

print("Uploading static-spa...")
upload_tree(sftp, '/Users/joycezhang/mathlearnlab/server/static-spa/', f'{BASE}/static-spa/')

print("Uploading content (with en/)...")
ssh.exec_command('mkdir -p /opt/apps/mathlearnlab/content')
upload_tree(sftp, '/Users/joycezhang/mathlearnlab/content/', f'{BASE}/content/')

print("Uploading server code...")
import os as _os
_router_src = '/Users/joycezhang/mathlearnlab/server/routers'
router_files = [f for f in _os.listdir(_router_src) if f.endswith('.py')]
for f in router_files:
    sftp.put(f'{_router_src}/{f}', f'{BASE}/server/routers/{f}')
    print(f'  server/routers/{f} ok')
for f in ['config.py', 'main.py']:
    sftp.put(f'/Users/joycezhang/mathlearnlab/server/{f}', f'{BASE}/server/{f}')
    print(f'  server/{f} ok')

sftp.close()

print("Restarting server...")
_, stdout, stderr = ssh.exec_command('systemctl restart mathlearnlab && sleep 3 && systemctl is-active mathlearnlab')
print(stdout.read().decode().strip())

ssh.close()
print("Done!")
