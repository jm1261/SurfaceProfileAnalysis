import src.fileIO as io
import src.filepaths as fp
import src.analysis as anal
import src.datalevelling as dl

from pathlib import Path


def step_widths(file_paths : list,
                out_path : str,
                batch_dictionary : dict) -> dict:
    """
    """
    feature_widths = []
    for file in file_paths:
        file_name = fp.get_filename(file_path=file)
        feature_results = anal.calculate_dektak_widths(
            file_path=file,
            file_name=file_name,
            out_path=Path(f'{out_path}/{file_name}_Width.png'),
            plot_dict=batch_dictionary)
        batch_dictionary.update(feature_results)
        feature_widths.append(feature_results[f'{file_name} Width'])
    width_results = anal.average_step_and_error(x=feature_widths)
    results_dictionary = dict(
        batch_dictionary,
        **width_results)
    return results_dictionary


def step_height(file_paths : list,
                out_path : str,
                batch_dictionary : dict) -> dict:
    """
    Calculate the step height of a feature for the Bruker Dektak.

    Level surface profile and calculate individual step height for multiple
    measurements on the same sample/batch of samples. Take an average.

    Parameters
    ----------
    file_paths: list
        List of files to process as paths.
    out_path: string
        Path to save.
    batch_dictionary: dictionary
        Batch dictionary containing batch name, file names, and data path. It
        should also contain the plotting dictionary.
    
    Returns
    -------
    results_dictionary: dictionary
        Step heights and errors for individual 
    See Also
    --------
    Notes
    -----
    Example
    -------
    """
    film_thicknesses = []
    for file in file_paths:
        file_name = fp.get_filename(file_path=file)
        step_results = anal.calculate_dektak_thicks(
            file_path=file,
            file_name=file_name,
            plot_dict=batch_dictionary,
            out_path=Path(f'{out_path}/{file_name}_Height.png'))
        batch_dictionary.update(step_results)
        film_thicknesses.append(step_results[f'{file_name} Thickness'])
    thickness_results = anal.average_step_and_error(x=film_thicknesses)
    results_dictionary = dict(
        batch_dictionary,
        **thickness_results)
    return results_dictionary


if __name__ == '__main__':
    '''
    Root setup for Notebooks repository as root directory. Remove '..' to run
    from file_path=Path() in dektak_dict load.
    '''
    root = Path().absolute()
    dektak_dict = io.load_json(
        file_path=Path(
            f'{root}/SurfaceProfileAnalysis/dektak_dictionary.json'))
    batch_name = dektak_dict["batch_name"]
    files = dektak_dict["data_files"]
    data_path = dektak_dict["data_path"]
    file_paths = [Path(f'{data_path}/{file}') for file in files]
    if dektak_dict["process"] == "height":
        results_dictionary = step_height(
            file_paths=file_paths,
            out_path=data_path,
            batch_dictionary=dektak_dict)
    elif dektak_dict["process"] == "width":
        results_dictionary = step_widths(
            file_paths=file_paths,
            out_path=data_path,
            batch_dictionary=dektak_dict)
    io.save_json_dicts(
        out_path=Path(f'{data_path}/{batch_name}_Height.json'),
        dictionary=results_dictionary)
