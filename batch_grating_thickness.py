import src.fileIO as io
import src.filepaths as fp
import src.analysis as anal

from pathlib import Path


def batch_grating_thickness(parent_directory,
                            batch_name,
                            file_paths,
                            directory_paths,
                            plot_files):
    '''
    Calculate sample batch grating thicknesses, and error, from individual files
    within batch.
    Args:
        parent_directory: <string> parent directory identifier
        batch_name: <string> batch name string
        file_paths: <array> array of target file paths
        directory_paths: <dict> dictionary containing required paths
        plot_files: <string> "True" or "False" for plotting output
    Returns:
        results_dictionary: <dict>
            Batch Name
            File Name
            File Path
            Sample Name
            Grating Period
            Individual grating thicknesses and errors
            Individual regions of interest
            Individual trim indices
    '''
    batch_dictionary = fp.update_batch_dictionary(
        parent=parent_directory,
        batch_name=batch_name,
        file_paths=file_paths)
    for file in file_paths:
        sample_parameters = fp.sample_information(file_path=file)
        lateral, profile = io.read_thickness_file(
            parent_directory=parent_directory,
            file_path=file)
        out_string = sample_parameters[f'{parent_directory} Secondary String']
        thickness_results = anal.calculate_grating_thickness(
            x_array=lateral,
            y_array=profile,
            file_name=sample_parameters[f'{parent_directory} File Name'],
            sample_name=sample_parameters[
                f'{parent_directory} Secondary String'],
            plot_files=plot_files,
            out_path=Path(
                f'{directory_paths["Results Path"]}'
                f'/{batch_name}_{out_string}_GratingThickness.png'))
        batch_dictionary.update(thickness_results)
    return batch_dictionary


if __name__ == '__main__':

    ''' Organisation '''
    root = Path().absolute()
    info, directory_paths = fp.get_directory_paths(root_path=root)
    file_paths = fp.get_files_paths(
        directory_path=directory_paths['AFM Path'],
        file_string='.csv')
    parent, batches = fp.get_all_batches(file_paths=file_paths)

    ''' Loop Files '''
    for batch, filepaths in batches.items():
        out_file = Path(
            f'{directory_paths["Results Path"]}'
            f'/{batch}_GratingThickness.json')
        if out_file.is_file():
            pass
        else:
            results_dictionary = batch_grating_thickness(
                parent_directory=parent,
                batch_name=batch,
                file_paths=filepaths,
                directory_paths=directory_paths,
                plot_files=info['Plot Files'])
            io.save_json_dicts(
                out_path=out_file,
                dictionary=results_dictionary)
