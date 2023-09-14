import sys
from pathlib import Path
import shutil
import re
import os

DIRECTORY_NAME = {
    'JPEG': "Images",
    'JPG': "Images",
    'PNG': "Images",
    'SVG': "Images",
    'AVI': "Video", 
    'MP4': "Video", 
    'MOV': "Video", 
    'MKV': "Video",
    'DOC': "Documents", 
    'DOCX': "Documents",
    'TXT': "Documents", 
    'PDF': "Documents", 
    'XLSX': "Documents", 
    'PPTX': "Documents",
    'MP3': "Audio",
    'OGG': "Audio", 
    'WAV': "Audio", 
    'AMR': "Audio",
    'M4A': "Audio",
    'ZIP': "Archives",
    'GZ': "Archives", 
    'TAR': "Archives"
}

def read_folder(path: Path, destination_folder: Path) -> None:
    
    for el in path.iterdir():
        if Path(el).is_dir():
            if el.name not in ('Archives', 'Video', 'Audio', 'Documents', 'Images', 'Others'):
                read_folder(Path(el), destination_folder)
        else:
            fullname = path / el.name
            handle_file(fullname, path, destination_folder)

def handle_file(file: Path, path: Path, destination_folder: Path) -> None:
    
    file_name = file.name.rsplit('.',1)[0]
    # ext = file.suffix[1:]
    ext = file.name.rsplit('.',1)[1]
         
    if not ext:  
        target_folder = destination_folder / 'Others'
        transfer_file(file, target_folder)
    else:
        name = file_name + '.' + ext
        file = path / name
        try:
            target_folder = destination_folder / DIRECTORY_NAME[ext.upper()]
            transfer_file(file, target_folder)
        except KeyError:
            target_folder = destination_folder / 'Others'
            transfer_file(file, target_folder)

def normalize(element: str) -> str:
    
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    element_trans = element.translate(TRANS)
    element_trans = re.sub(r'\W^\.', '_', element_trans)    
    return element_trans

def transfer_file(file: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    ext = file.suffix[1:].upper()
    if ext in DIRECTORY_NAME and DIRECTORY_NAME[ext] == 'Archives':
        handle_archive(file, target_folder)
    else:
        file.replace(target_folder / normalize(file.name))
       

def rename_files_and_folders(path: Path) -> None:
    
    for el in path.iterdir():
        if el.is_dir():
            path = el.replace(path / normalize(el.name))
            rename_files_and_folders(path)
        else:
            el.replace(path / normalize(el.name))
            

def handle_archive(file: Path, target_folder: Path) -> None:
    
    archive_name = normalize(file.name.replace(file.suffix,''))
    folder_for_file = target_folder / archive_name
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(file, folder_for_file)
        rename_files_and_folders(folder_for_file)
    except shutil.ReadError:
        print('It is not archive')
        folder_for_file.rmdir()
    file.unlink()


def handle_empty_folders(path: Path) -> None:
    for cur_dir, subdirs, files in os.walk(path, topdown=False):
                # print(cur_dir, subdirs, files)
                for subdir in subdirs:
                    if not os.listdir(os.path.join(cur_dir, subdir)) and not subdir in ('Archives', 'Video', 'Audio', 'Documents', 'Images', 'Others'):
                        # print(f'removing {subdir}')
                        os.rmdir(os.path.join(cur_dir, subdir))
    if not os.listdir(cur_dir) and not Path(cur_dir).name in ('Archives', 'Video', 'Audio', 'Documents', 'Images', 'Others'):
        # print(f'removing {cur_dir}')
        os.rmdir(cur_dir)
