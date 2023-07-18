import os
import numpy as np

from pathlib import Path
from sys import platform
from src.fileIO import load_json
from src.GUI import prompt_for_path


def get_directory_paths(root_path):
    '''
    Get target data path and results path from info dictionary file.
    Args:
        root_path: <string> path to root directory
    Returns:
        data_path: <string> path to data directory
        bg_path: <string> path to background directory
        results_path: <string> path to results directory
        info: <dict> information dictionary (info.json)
    '''
    info = load_json(file_path=Path(f'{root_path}/info.json'))
    directory_paths = {}
    for key, value in info.items():
        if 'Path' in key:
            directory_paths.update({key: Path(f'{value}')})
    return info, directory_paths


def get_files_paths(directory_path,
                    file_string):
    '''
    Get target file paths for target files in a target directory.
    Args:
        directory_path: <string> path to data directory
        file_string: <string> file extension (e.g. .csv)
    Returns:
        file_paths: <string> path to files
    '''
    directory_list = sorted(os.listdir(directory_path))
    return [
        Path(f'{directory_path}/{file}')
        for file in directory_list if file_string in file]


def get_parent_directory(file_path):
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


def thickness_sample_information(file_path):
    '''
    Pull sample parameters from file name string for various processes.
    Args:
        file_path: <string> path to file
    Returns:
        sample_parameters: <dict>
    '''
    parent_directory = get_parent_directory(file_path=file_path)
    file_name = get_filename(file_path=file_path)
    file_split = file_name.split('_')
    return {
        "Parent Directory": parent_directory,
        f'{parent_directory} File Name': file_name,
        f'{parent_directory} File Path': f'{file_path}',
        f'{parent_directory} Primary String': ('_').join(file_split[0:2]),
        f'{parent_directory} Secondary String': ('_').join(file_split[2:])}


def sample_information(file_path):
    '''
    Pull sample parameters based on which type of file is being analysed.
    Args:
        file_path: <string> path to file
    Returns:
        sample_parameters: <dict>
    '''
    parent_directory = get_parent_directory(file_path=file_path)
    if parent_directory == 'AFM' or parent_directory == 'Dektak':
        sample_parameters = thickness_sample_information(
            file_path=file_path)
    else:
        sample_parameters = {}
    return sample_parameters


def get_all_batches(file_paths):
    '''
    Find all sample batches in series of file paths and append file paths to
    batch names for loop processing.
    Args:
        file_paths: <array> array of target file paths
    Returns:
        parent: <string> parent directory string
        batches: <dict>
            Batch inidicators: respective file paths for all samples in batch
    '''
    batches = {}
    for file in file_paths:
        sample_parameters = sample_information(file_path=file)
        parent = sample_parameters['Parent Directory']
        key = f'{parent} Primary String'
        if sample_parameters[key] in batches.keys():
            batches[f'{sample_parameters[key]}'].append(file)
        else:
            batches.update({f'{sample_parameters[key]}': [file]})
    return parent, batches


def update_batch_dictionary(parent,
                            batch_name,
                            file_paths):
    '''
    Update batch results dictionary.
    Args:
        parent: <string> parent directory identifier
        batch_name: <string> batch name identifier
        file_paths: <array> list of target file paths
    Returns:
        batch_dictionary: <dict>
            Batch Name
            File Names
            File Paths
            Secondary Strings
    '''
    batch_dictionary = {
        f'{parent} Batch Name': batch_name,
        f'{parent} File Name': [],
        f'{parent} File Path': [],
        f'{parent} Secondary String': []}
    for file in file_paths:
        sample_parameters = sample_information(file_path=file)
        for key, value in sample_parameters.items():
            if key in batch_dictionary.keys():
                batch_dictionary[key].append(value)
    return batch_dictionary
