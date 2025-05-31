import os

# Configurações
RootDir = "~"  # Será expandido para o diretório home
Ext = input("Extenssion: ")
ListFileName = "FilesFound.txt"

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')
    
def expand_user_path(path):
    """Expande o caminho com ~ para o diretório home completo"""
    return os.path.expanduser(path)

def find_files(rootdir, ext):
    """Encontra todos os arquivos com a extensão especificada"""
    file_list = []
    rootdir = expand_user_path(rootdir)
    
    try:
        for root, _, files in os.walk(rootdir):
            for file in files:
                if file.lower().endswith(ext.lower()):  # Case insensitive
                    filepath = os.path.join(root, file)
                    file_list.append(filepath)
                    clear()
                    print(f"{filepath}")  # Feedback para o usuário
    except PermissionError:
        print(f"Permission denied: {root}")
    except Exception as e:
        print(f"Error: {e}")
    
    return file_list

def save_file_list(filelist, output_file):
    """Salva a lista de arquivos em um arquivo de texto"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(filelist))
        print(f"\nList saved: {os.path.abspath(output_file)}")  # Alterado aqui
    except IOError as e:
        print(f"Saving list failed: {e}")

if __name__ == "__main__":
    clear()
    print(f"Searching {Ext} in {expand_user_path(RootDir)}...\n")
    
    found_files = find_files(RootDir, Ext)
    save_file_list(found_files, ListFileName)
    
    print(f"\nFile count: {len(found_files)}")
