from pathlib import Path
import re
import shutil
import sys


# file_parser

JPEG_IMAGES = []
PNG_IMAGES = []
JPG_IMAGES = []
SVG_IMAGES = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPTX_DOCUMENTS = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
ARCHIVES = []

REGISTER_EXTENSIONS = {'JPEG': JPEG_IMAGES,
                       'PNG': PNG_IMAGES,
                       'JPG': JPG_IMAGES,
                       'SVG': SVG_IMAGES,
                       'AVI': AVI_VIDEO,
                       'MP4': MP4_VIDEO,
                       'MOV': MOV_VIDEO,
                       'MKV': MKV_VIDEO,
                       'DOC': DOC_DOCUMENTS,
                       'DOCX': DOCX_DOCUMENTS,
                       'TXT': TXT_DOCUMENTS,
                       'PDF': PDF_DOCUMENTS,
                       'XLSX': XLSX_DOCUMENTS,
                       'PPTX': PPTX_DOCUMENTS,
                       'MP3': MP3_AUDIO,
                       'OGG': OGG_AUDIO,
                       'WAV': WAV_AUDIO,
                       'AMR': AMR_AUDIO,
                       'ZIP': ARCHIVES,
                       'GZ': ARCHIVES,
                       'TAR': ARCHIVES}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN_EXTENSIONS = set()


def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()


def scan(folder: Path):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue

        extension = get_extension(item.name)
        full_name = folder / item.name
        if not extension:
            pass
        else:
            try:
                ext_reg = REGISTER_EXTENSIONS[extension]
                ext_reg.append(full_name)
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN_EXTENSIONS.add(extension)


# normalize

CYRILLIC_SYMBOLS = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'

LATIN_SYMBOLS = ('a', 'b', 'v', 'h', 'g', 'd', 'e', 'ye', 'zh', 'z', 'y', 'i', 'yi', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'kh', 'ts', 'ch', 'sh', 'shch', '', 'yu', 'ya')

TRANSLITERATION = {}

for cyrillic, latin in zip(CYRILLIC_SYMBOLS, LATIN_SYMBOLS):

    TRANSLITERATION[ord(cyrillic)] = latin
    TRANSLITERATION[ord(cyrillic.upper())] = latin.upper()


def normalize(name: str) -> str:

    normalized_name = re.sub(r'\W', '_', name.translate(TRANSLITERATION))

    return normalized_name


# main

def handle_media(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    file_name.replace(target_folder / (normalize(file_name.stem) + file_name.suffix))


def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()


def main(folder: Path):
    scan(folder)
    for file in JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')
    for file in AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI')
    for file in MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4')
    for file in MOV_VIDEO:
        handle_media(file, folder / 'video' / 'MOV')
    for file in MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV')
    for file in DOC_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'DOC')
    for file in DOCX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'DOCX')
    for file in TXT_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'TXT')
    for file in PDF_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'PDF')
    for file in XLSX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'XLSX')
    for file in PPTX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'PPTX')
    for file in MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3')
    for file in OGG_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG')
    for file in WAV_AUDIO:
        handle_media(file, folder / 'audio' / 'WAV')
    for file in AMR_AUDIO:
        handle_media(file, folder / 'audio' / 'AMR')
    for file in ARCHIVES:
        handle_archive(file, folder / 'archives')

    for folder in FOLDERS[::-1]:
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')


def start():
    if sys.argv[1]:
        folder_process = Path(sys.argv[1])
        main(folder_process)
