#!/usr/bin/env python3
"""Deploy MathLearnLab to the ECS server via SFTP/SSH.

Used by GitHub Actions (CI) and for local deploys. Credentials come from
environment variables only — never hardcode secrets in this file:

    DEPLOY_HOST   (default 8.137.78.250)
    DEPLOY_USER   (default root)
    DEPLOY_SSH_KEY — path to an SSH private key (preferred) or the key
                     contents themselves
    DEPLOY_PASS   — password fallback (local deploys only)

Synchronizes the FULL server tree (routers/services/models/middleware),
content/, static-spa/ and requirements, then restarts the systemd service.
"""

import io
import os
import tempfile
from pathlib import Path

import paramiko

HOST = os.environ.get('DEPLOY_HOST', '8.137.78.250')
USER = os.environ.get('DEPLOY_USER', 'root')
BASE = '/opt/apps/mathlearnlab'
LOCAL = Path(__file__).resolve().parent.parent
SKIP_DIRS = {'__pycache__', '.pytest_cache', 'node_modules'}


def _load_key(text: str):
    for cls in (paramiko.Ed25519Key, paramiko.RSAKey, paramiko.ECDSAKey):
        try:
            return cls.from_private_key(io.StringIO(text))
        except Exception:
            continue
    return None


def _connect():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    kwargs = dict(hostname=HOST, username=USER, timeout=30)
    key_src = os.environ.get('DEPLOY_SSH_KEY', '')
    if key_src:
        text = Path(key_src).read_text() if Path(key_src).exists() else key_src
        pkey = _load_key(text)
        if pkey is None:
            raise RuntimeError("DEPLOY_SSH_KEY provided but could not be parsed")
        kwargs['pkey'] = pkey
    elif os.environ.get('DEPLOY_PASS'):
        kwargs['password'] = os.environ['DEPLOY_PASS']
    else:
        raise RuntimeError("Set DEPLOY_SSH_KEY or DEPLOY_PASS")
    ssh.connect(**kwargs)
    return ssh


def ensure_dir(sftp, path):
    parts = path.strip('/').split('/')
    cur = '/'
    for p in parts:
        if not p:
            continue
        cur += p + '/'
        try:
            sftp.stat(cur)
        except Exception:
            sftp.mkdir(cur)


def upload_tree(sftp, local_root, remote_root, skip_dirs=()):
    for root, dirs, files in os.walk(local_root):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        rel = os.path.relpath(root, local_root)
        rdir = remote_root if rel == '.' else f'{remote_root}/{rel}'.replace('//', '/')
        ensure_dir(sftp, rdir)
        for f in files:
            if f.endswith(('.pyc', '.pyo')):
                continue
            sftp.put(os.path.join(root, f), os.path.join(rdir, f).replace('\\', '/'))


def main():
    ssh = _connect()
    sftp = ssh.open_sftp()

    print("Uploading static-spa (frontend build)...")
    upload_tree(sftp, str(LOCAL / 'server' / 'static-spa'), f'{BASE}/static-spa/')

    print("Uploading content (with en/)...")
    ssh.exec_command(f'mkdir -p {BASE}/content')
    upload_tree(sftp, str(LOCAL / 'content'), f'{BASE}/content/')

    print("Uploading server code (full tree)...")
    ssh.exec_command(f'mkdir -p {BASE}/server')
    upload_tree(sftp, str(LOCAL / 'server'), f'{BASE}/server/', skip_dirs=SKIP_DIRS)

    print("Uploading requirements...")
    for f in ['requirements.txt', 'requirements-prod.txt', 'requirements-dev.txt', '.env.example']:
        p = LOCAL / f
        if p.exists():
            sftp.put(str(p), f'{BASE}/{f}')
            print(f'  {f} ok')

    sftp.close()

    print("Ensuring ADMIN_SECRET on remote .env...")
    _, stdout, _ = ssh.exec_command(f'cat {BASE}/.env')
    if 'ADMIN_SECRET=' in stdout.read().decode():
        print("  ADMIN_SECRET already present.")
    else:
        admin_secret = os.urandom(32).hex()
        ssh.exec_command(f'echo "ADMIN_SECRET={admin_secret}" >> {BASE}/.env')
        print("  ADMIN_SECRET was missing — generated and appended to remote .env.")
        print(f"  >>> SAVE THIS VALUE for /admin login: {admin_secret}")

    print("Restarting server...")
    _, stdout, stderr = ssh.exec_command(
        f'find {BASE}/server -name __pycache__ -type d -exec rm -rf {{}} + 2>/dev/null; '
        'systemctl restart mathlearnlab && sleep 3 && systemctl is-active mathlearnlab'
    )
    print(stdout.read().decode().strip())
    err = stderr.read().decode().strip()
    if err:
        print("stderr:", err)

    ssh.close()
    print("Done!")


if __name__ == '__main__':
    main()
