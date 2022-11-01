import os

from pathlib import Path
from sys import platform
from src.fileIO import load_json
from src.GUI import prompt_for_path


def check_platform():
    '''
    Check operating system.
    Args:
        None
    Returns:
        operating_system: <string> "Windows", "Linux", or "Mac"
    '''
    if platform == 'linux' or platform == 'linux2':
        operating_system = 'Linux'
    elif platform == 'darwin':
        operating_system = 'Mac'
    elif platform == 'win32':
        operating_system = 'Windows'
    return operating_system


def extractfile(dir_path,
                file_string):
    '''
    Pull file from directory path.
    Args:
        dir_path: <string> path to file
        file_string: <string> string contained within file name
    Returns:
        array: <array> array of selected files
    '''
    directory_list = sorted(os.listdir(dir_path))
    return [file for file in directory_list if file_string in file]


def directory_paths(root_path):
    '''
    Get target data path and results path from info dictionary file.
    Args:
        root_path: <string> path to root directory
    Returns:
        data_path: <string> path to data directory
        results_path: <string> path to results directory
    '''
    info = load_json(file_path=Path(f'{root_path}/info.json'))
    data_path = Path(f'{root_path}{info["Data Path"]}')
    results_path = Path(f'{root_path}{info["Results Path"]}')
    return data_path, results_path


def get_files_paths(root_path,
                    file_string):
    '''
    Get target files depending on operating system.
    Args:
        root_path: <string> path to root folder
        file_string: <string> file extension (e.g. .csv)
    Returns:
        file_paths: <string> path to files
    '''
    operating_system = check_platform()
    if operating_system == 'Linux' or operating_system == 'Mac':
        directory_path = directory_paths(root_path=root_path)
        file_list = extractfile(
            dir_path=directory_path,
            file_string=file_string)
        file_paths = [
            Path(directory_path).joinpath(file)
            for file in file_list]
    elif operating_system == 'Windows':
        file_paths = prompt_for_path(
            default=root_path,
            title='Select Target File(s)',
            file_path=True,
            file_type=[(f'{file_string}', f'*{file_string}')])
    return file_paths


def parent_directory(file_path):
    '''
    Find parent directory name of target file.
    Args:
        file_path: <string> path to file
    Returns:
        parent_directory: <string> parent directory name (not path)
    '''
    dirpath = os.path.dirname(file_path)
    dirpathsplit = dirpath.split('\\')
    parent_directory = dirpathsplit[-1]
    return parent_directory


def get_filename(file_path):
    '''
    Splits file path to remove directory path and file extensions.
    Args:
        file_path: <string> path to file
    Returns:
        file_name: <string> file name without path or extensions
    '''
    return os.path.splitext(os.path.basename(file_path))[0]


def sample_information(file_path):
    '''
    Pull sample information from file name string.
    Args:
        file_path: <string> path to file
    Returns:
        sample_parameters: <dict>
            File Name
            File Path
            Sample Name
            File Type [AFM/Dektak]
    '''
    file_name = get_filename(file_path=file_path)
    parent = parent_directory(file_path=file_path)
    file_split = file_name.split('_')
    return {
        "File Name": file_name,
        "File Path": f'{file_path}',
        "Sample Name": file_split[0],
        "File Type": parent}
