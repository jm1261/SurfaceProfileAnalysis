import os


def get_filename(file_path):
    """
    Get the file name of a file without the directory path or file extension.

    Split file path and remove directory path and file extensions.

    Parameters
    ----------
    file_path: string
        Path to file.
    
    Returns
    -------
    file_name: string
        File name without path or extension.
    
    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    >>> file_path = "/Path/To/File/File1.txt"
    >>> file_name = get_filename(file_path=file_path)
    >>> file_name
    "File1"

    """
    return os.path.splitext(os.path.basename(file_path))[0]
