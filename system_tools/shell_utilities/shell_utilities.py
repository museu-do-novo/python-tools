"""
linux_commands.py - A Python implementation of common Linux/Unix commands
"""

import os
import shutil
import urllib.request
import fnmatch
import tarfile
import psutil
import subprocess
import time
import getpass
import platform
from pathlib import Path

def pwd():
    """Print working directory (like 'pwd')"""
    return os.getcwd()

def clear():
    """Clear the terminal screen (like 'clear')"""
    os.system('cls' if os.name == 'nt' else 'clear')

def cd(path):
    """Change directory (like 'cd')"""
    os.chdir(path)

def ls(path='.', all_files=False, long_format=False):
    """List directory contents (like 'ls')
    
    Args:
        path: Directory path (default: current directory)
        all_files: Show hidden files (like -a flag)
        long_format: Return detailed info (like -l flag)
    """
    items = os.listdir(path)
    if not all_files:
        items = [i for i in items if not i.startswith('.')]
    if long_format:
        return [(item, os.stat(os.path.join(path, item))) for item in items]
    return items

def mkdir(path, parents=False, mode=0o777):
    """Create directory (like 'mkdir')
    
    Args:
        path: Directory path to create
        parents: Create parent directories as needed (like -p flag)
        mode: Permission mode (default: 0o777)
    """
    if parents:
        os.makedirs(path, exist_ok=True, mode=mode)
    else:
        os.mkdir(path, mode=mode)

def rm(path, recursive=False, force=False):
    """Remove files/directories (like 'rm')
    
    Args:
        path: Path to remove
        recursive: Remove directories recursively (like -r flag)
        force: Ignore errors if file doesn't exist (like -f flag)
    """
    try:
        if os.path.isdir(path):
            shutil.rmtree(path) if recursive else os.rmdir(path)
        else:
            os.remove(path)
    except Exception:
        if not force:
            raise

def cp(src, dst, recursive=False, preserve_metadata=False):
    """Copy files/directories (like 'cp')
    
    Args:
        src: Source path
        dst: Destination path
        recursive: Copy directories recursively (like -r flag)
        preserve_metadata: Preserve file metadata (like -p flag)
    """
    if os.path.isdir(src):
        if not recursive:
            raise IsADirectoryError(f"{src} is a directory (use recursive=True)")
        shutil.copytree(src, dst, copy_function=shutil.copy2 if preserve_metadata else shutil.copy)
    else:
        shutil.copy2(src, dst) if preserve_metadata else shutil.copy(src, dst)

def mv(src, dst):
    """Move/rename files (like 'mv')"""
    shutil.move(src, dst)

def touch(path):
    """Create empty file or update timestamp (like 'touch')"""
    Path(path).touch()

def cat(file_path):
    """Display file contents (like 'cat')"""
    with open(file_path) as f:
        return f.read()

def head(file_path, lines=10):
    """Display first lines of file (like 'head')"""
    with open(file_path) as f:
        return [next(f).rstrip() for _ in range(lines)]

def tail(file_path, lines=10):
    """Display last lines of file (like 'tail')"""
    with open(file_path) as f:
        return f.readlines()[-lines:]

def echo(text, newline=True):
    """Print text (like 'echo')"""
    print(text, end='\n' if newline else '')

def sleep(seconds):
    """Pause execution (like 'sleep')"""
    time.sleep(seconds)

def find(path='.', name=None, type_filter=None):
    """Search for files (like 'find')
    
    Args:
        path: Starting directory (default: current directory)
        name: Filename pattern to match
        type_filter: Filter by type ('d' for directory, 'f' for file)
    """
    matches = []
    for root, dirs, files in os.walk(path):
        items = dirs if type_filter == 'd' else files if type_filter == 'f' else dirs + files
        for item in items:
            if name is None or fnmatch.fnmatch(item, name):
                matches.append(os.path.join(root, item))
    return matches

def grep(path, pattern):
    """Search text in files (like 'grep')
    
    Args:
        path: File path to search
        pattern: Regular expression pattern to search for
    """
    import re
    matches = []
    with open(path) as f:
        for i, line in enumerate(f, 1):
            if re.search(pattern, line):
                matches.append((i, line.strip()))
    return matches

def chmod(path, mode):
    """Change file permissions (like 'chmod')"""
    os.chmod(path, mode)

def chown(path, user=None, group=None):
    """Change file owner/group (like 'chown')"""
    import pwd, grp
    uid = pwd.getpwnam(user).pw_uid if user else -1
    gid = grp.getgrnam(group).gr_gid if group else -1
    os.chown(path, uid, gid)

def ln(src, dst, symbolic=True):
    """Create links (like 'ln')
    
    Args:
        src: Source path
        dst: Destination path
        symbolic: Create symbolic link (default) or hard link
    """
    os.symlink(src, dst) if symbolic else os.link(src, dst)

def wget(url, output=None):
    """Download file from URL (like 'wget')
    
    Args:
        url: URL to download
        output: Output filename (default: basename from URL)
    """
    if output is None:
        output = os.path.basename(url)
    urllib.request.urlretrieve(url, output)
    return output

def tar_create(archive_name, source_path):
    """Create tar archive (like 'tar -czf')"""
    with tarfile.open(archive_name, "w:gz") as tar:
        tar.add(source_path, arcname=os.path.basename(source_path))

def tar_extract(archive_name, extract_path='.'):
    """Extract tar archive (like 'tar -xzf')"""
    with tarfile.open(archive_name, "r:gz") as tar:
        tar.extractall(path=extract_path)

def df():
    """Show disk usage (like 'df')"""
    return [{
        'device': p.device,
        'mount': p.mountpoint,
        'fs_type': p.fstype,
        'total': shutil.disk_usage(p.mountpoint).total,
        'used': shutil.disk_usage(p.mountpoint).used,
        'free': shutil.disk_usage(p.mountpoint).free
    } for p in psutil.disk_partitions()]

def du(path='.'):
    """Show file space usage (like 'du')"""
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total += os.path.getsize(fp)
    return total

def ps():
    """List processes (like 'ps')"""
    return [{'pid': p.pid, 'name': p.name(), 'status': p.status()} for p in psutil.process_iter()]

def kill(pid, sig=15):
    """Kill process (like 'kill')"""
    os.kill(pid, sig)

def whoami():
    """Show current user (like 'whoami')"""
    return getpass.getuser()

def env():
    """Show environment variables (like 'env')"""
    return dict(os.environ)

def uname():
    """Show system information (like 'uname -a')"""
    return {
        'system': platform.system(),
        'node': platform.node(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor()
    }

def which(cmd):
    """Locate command (like 'which')"""
    for path in os.environ["PATH"].split(os.pathsep):
        full_path = os.path.join(path, cmd)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path
    return None

def ping(host, count=4):
    """Ping host (like 'ping -c')"""
    result = subprocess.run(['ping', '-c', str(count), host], capture_output=True, text=True)
    return result.stdout


"""
mega_utilities.py - Simplified interface for MEGA.nz commands via Python
Requires: mega.py (pip install mega.py)
"""

from mega import Mega
import os

_mega_session = None

def mega_login(email=None, password=None):
    """Login to MEGA (anonymously or with account)"""
    global _mega_session
    mega = Mega()
    if email and password:
        _mega_session = mega.login(email, password)
    else:
        _mega_session = mega.login()
    return True

def mega_logout():
    """End current session (not required in mega.py)"""
    global _mega_session
    _mega_session = None

def mega_upload(filepath):
    """Upload file to MEGA account"""
    if not _mega_session:
        raise Exception("Not authenticated. Use mega_login() first.")
    return _mega_session.upload(filepath)

def mega_get_link(file_dict):
    """Get shareable download link for a file"""
    if not _mega_session:
        raise Exception("Not authenticated.")
    return _mega_session.get_upload_link(file_dict)

def mega_list_files():
    """List all files in MEGA account"""
    if not _mega_session:
        raise Exception("Not authenticated.")
    files = _mega_session.get_files()
    return [{
        'name': f['name'],
        'size': f['s'],
        'created': f['c'],
        'id': file_id
    } for file_id, f in files.items()]

def mega_download_url(url, dest_filename=None):
    """Download public file from MEGA URL"""
    if not _mega_session:
        mega_login()
    _mega_session.download_url(url, dest_filename)

def mega_download_file(file_dict, dest_path='.'):
    """Download file from logged-in account"""
    if not _mega_session:
        raise Exception("Not authenticated.")
    _mega_session.download(file_dict, dest_path)

def mega_delete(file_id):
    """Delete file from MEGA account"""
    if not _mega_session:
        raise Exception("Not authenticated.")
    _mega_session.destroy(file_id)