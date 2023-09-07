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


def read_dektak_file(file_path : str) -> list:
    """
    Loads Bruker Dektak csv file.

    Reads output file to return lateral (mm) and profile (nm) data.

    Parameters
    ----------
    file_path: string
        Path to file.
    
    Returns
    -------
    lateral, profile: list
        Lateral position of the tip in mm, surface profile in nm.
    
    See Also
    --------
    numpy genfromtxt
    read_afm_file

    Notes
    -----
    Uses the 'Lateral' column header in the Dektak csv file to find the start
    point of the Dektak profile measurement data. Skips any data levelling, mark
    position, or calculated step height data from the header of the file which
    may be present due to the Dektak software. Converts lateral position to mm
    and profile to nm.

    Example
    -------
    None

    """
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


def read_afm_file(file_path : str) -> list:
    """
    Loads Bruker AFM csv file.

    Reads output file to return lateral (mm) and profile (nm) data.

    Parameters
    ----------
    file_path: string
        Path to file.
    
    Returns
    -------
    lateral, profile: list
        Lateral position of the tip in mm, surface profile in nm.
    
    See Also
    --------
    numpy genfromtxt
    read_dektak_file

    Notes
    -----
    Can distinguish between delimiters depending on the AFM save parameters.

    Example
    -------
    None

    """
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


def read_thickness_file(file_type : str,
                        file_path : str) -> list:
    """
    Reads either Dektak or AFM file.
    
    Reads lateral and profile data from Bruker Dektak or AFM file types.

    Parameters
    ----------
    file_type, file_path: string
        "AFM" or "Dektak", path to file.
    
    Returns
    -------
    lateral, profile: list
        Lateral position in mm, profile in nm. (x, y data).
    
    See Also
    --------
    read_afm_file
    read_dektak_file

    Notes
    -----
    Uses the file_type key to access different loading functions for the Bruker
    AFM and Dektak surface profilometers.

    Example
    -------
    None

    """
    if file_type == 'AFM':
        lateral, profile = read_afm_file(
            file_path=file_path)
    elif file_type == 'Dektak':
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


def save_json_dicts(out_path : str,
                    dictionary : dict) -> None:
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
