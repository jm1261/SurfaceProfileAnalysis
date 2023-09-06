import json
import numpy as np


def load_json(file_path):
    """
    Loads .json file types.

    Use json python library to load a .json file.

    Parameters
    ----------
    file_path : string
        Path to file.

    Returns
    -------
    json file : dictionary
        .json dictionary file.

    See Also
    --------
    read_dektak_file
    read_afm_file
    read_thickness_file
    save_json_dicts

    Notes
    -----
    json files are typically dictionaries, as such the function is intended for
    use with dictionaries stored in .json file types.

    Examples
    --------
    my_dictionary = load_json(file_path="/Path/To/File")

    """
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
    try:
        lateral, profile = np.genfromtxt(
            fname=file_path,
            delimiter=',',
            skip_header=1,
            unpack=True)
    except:
        lateral, profile = np.genfromtxt(
            fname=file_path,
            delimiter='\t',
            skip_header=1,
            unpack=True)
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
    """
    Check data type.

    Check type of data string.

    Parameters
    ----------
    o : string
        String to check.

    Returns
    -------
    TypeError : Boolean
        TypeError if string is not suitable.


    See Also
    --------
    None.

    Notes
    -----
    None.

    Examples
    --------
    None.

    """
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError


def save_json_dicts(out_path,
                    dictionary):
    """
    Save .json file types.

    Use json python library to save a dictionary to a .json file.

    Parameters
    ----------
    out_path : string
        Path to file.
    dictionary : dictionary
        Dictionary to save.
    
    Returns
    -------
    None

    See Also
    --------
    load_json

    Notes
    -----
    json files are typically dictionaries, as such the function is intended for
    use with dictionaries stored in .json file types.

    Examples
    --------
    save_json_dicts(
        out_path="/Path/To/File",
        dictionary=my_dictionary)

    """
    with open(out_path, 'w') as outfile:
        json.dump(
            dictionary,
            outfile,
            indent=2,
            default=convert)
        outfile.write('\n')
