import argparse
from pathlib import Path
import sys
from .ai import ai,AiConfig,get_prompt
from rich.progress import track
from rich import print
BAK_PREFIX = ".h2-backup"

class StreamLinePrint:
    def __init__(self):
        self.line = ''
    def add(self,token):
        self.line+=token
        if ('\n' in token):
            print(self.line,end='')
            self.line = ''

def create_backup_folder(base_folder: str, single_backup: bool) -> Path:
    """Create a sequential or single backup folder based on user input."""
    base_backup = Path(BAK_PREFIX+base_folder)
    
    if single_backup:
        # If the user wants only a single backup folder, return the base folder
        return base_backup
    
    # Find the next available numbered folder (e.g., folder.h2-backup.0, folder.h2-backup.1, etc.)
    version = 0
    while (backup_folder := Path(f"{base_backup}.{version}")).exists():
        version += 1
    
    return backup_folder

def process_files(folder: str, ext: str,lang_name:str,single_backup: bool,doc_level:int,only_doc:bool,config:AiConfig):
    path = Path(folder)
    
    # Validate that the folder is indeed a directory
    if not path.is_dir():
        print(f"Error: '{folder}' is not a valid directory.")
        sys.exit(1)  # Exit the program with an error code

    # Create backup directory
    backup = create_backup_folder(folder,single_backup)
    backup.mkdir(exist_ok=True)
    files = list(path.rglob("*" + ext))
    if not files:
        print(f'Error: the glob `{path}/**.{ext}` does not match anything')
        sys.exit(1)

    for p in track(files,transient=True,description="Converting"):
        source_code = p.read_text()

        if (p == backup or backup in p.parents or p.name.startswith(BAK_PREFIX)):
            continue

        backup_file = backup.joinpath(p.relative_to(path))
        backup_file.parent.mkdir(parents=True, exist_ok=True)
        backup_file.write_text(source_code)

        print('----', p.name, '----')
        try:
            h1_code = (ai(source_code, lang_name ,p.relative_to(path),get_prompt(lang_name,doc_level=doc_level,only_doc=only_doc),config,StreamLinePrint().add))
        except ValueError as e:
            print('\nError: cannot get code on',p.name)
            error = f'// Error: cannot get code on file: "{p}".AI Message: \n"{e.args[0]}"'
            h1_code = "⍝ "+error # thats APL comment symbol. guaranteed error in every decent language.
        # print(h1_code)
        p.write_text(h1_code)

def main():
    parser = argparse.ArgumentParser(description='Process and backup files with a specific extension and AI configuration.')
    
    # Positional arguments for folder and file extension
    parser.add_argument('folder', type=str, help='The folder to process.')
    parser.add_argument('ext', type=str, help='The file extension to look for (e.g., "dart").')
    
    # Optional arguments for AiConfig
    parser.add_argument('--model', type=str, default='llama3.1', help='AI model to use (default: llama3.1).')
    parser.add_argument('--base-url', type=str, default='http://localhost:11434/v1', help='Base URL for the AI service (default: ollama endpoint [http://localhost:11434/v1] ).')
    parser.add_argument('--api-key', type=str, default='ollama', help='API key for the AI service (default: ollama).')
    parser.add_argument('--single-backup', action='store_true', help='Use a single backup folder without numbering (default is to create sequential backups).')
    parser.add_argument('-n','--lang-name', type=str, default='', help='The name name of the language in markdown (e.g. python)')
    parser.add_argument(
    "--doc-level", 
    "--lvl",
    type=int, 
    choices=[0, 1, 2, 3, 4],
    default=1,
    help="0: No docs, 1: Very minimal, 2: Minimal, 3: Moderate, 4: Detailed. (Default:1)"
)
    parser.add_argument('--only-doc',"--doc", action='store_true', help='Only write documentation,without improving the code quality.')

    args = parser.parse_args()

    # Create AiConfig object based on CLI input
    config = AiConfig(model=args.model, base_url=args.base_url, api_key=args.api_key)

    # Process files in the folder with the given extension and AiConfig
    process_files(folder=args.folder, ext=args.ext, lang_name=args.lang_name or args.ext.capitalize(),single_backup=args.single_backup,doc_level=args.doc_level,only_doc=args.only_doc,config=config)
