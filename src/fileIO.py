import json
import numpy as np


def load_json(file_path):
    '''
    Extract user variables from json dictionary.
    Args:
        file_path: <string> path to file
    Returns:
        dictionary: <dict> use variables dictionary
    '''
    with open(file_path, 'r') as file:
        return json.load(file)


def read_dektak_file(file_path):
    '''
    Load Bruker Dektak csv file. Reads output file, looks for Lateral, Position
    line, ignores other parameters in file.
    Args:
        file_path: <string> path to input file
    Returns:
        lateral: <array> lateral position array (x-array) [mm]
        profile: <array> surface profile array (y-array) [nm]
    '''
    with open(file_path) as infile:
        lines = infile.readlines()
        for index, line in enumerate(lines):
            if 'Lateral' in line:
                lateral, profile = np.genfromtxt(
                    fname=file_path,
                    delimiter=',',
                    skip_header=index + 1,
                    usecols=(0, 1),
                    unpack=True)
                lateral /= 1000  # convert to mm
                profile /= 10  # convert to nm
    return lateral, profile


def read_afm_file(file_path):
    '''
    Read Bruker AFM csv or txt file.
    Args:
        file_path: <string> path to input file
    Returns:
        lateral: <array> lateral position array (x-array) [mm]
        profile: <array> surface profile array (y-array) [nm]
    '''
    lateral, profile = np.genfromtxt(
        fname=file_path,
        delimiter=',',
        skip_header=1,
        unpack=True)
    lateral /= 1000  # convert to mm
    return lateral, profile


def read_thickness_file(parent_directory,
                        file_path):
    '''
    Reads either dektak or AFM file, depending on parent directory name. Must
    ensure thickness measurements are within a directory called AFM or Dektak.
    Args:
        parent_directory: <string> parent directory identifier
        file_path: <string> path to file
    Returns:
        lateral: <array> lateral position array (x-array) [mm]
        profile: <array> surface profile array (y-array) [nm]
    '''
    if parent_directory == 'AFM':
        lateral, profile = read_afm_file(
            file_path=file_path)
    elif parent_directory == 'Dektak':
        lateral, profile = read_dektak_file(
            file_path=file_path)
    else:
        lateral = []
        profile = []
    return lateral, profile


def convert(o):
    '''
    Check type of data string
    '''
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError


def save_json_dicts(out_path,
                    dictionary):
    '''
    Save dictionary to json file.
    Args:
        out_path: <string> path to file, including file name and extension
        dictionary: <dict> python dictionary to save out
    Returns:
        None
    '''
    with open(out_path, 'w') as outfile:
        json.dump(
            dictionary,
            outfile,
            indent=2,
            default=convert)
        outfile.write('\n')
