import src.fileIO as io
import src.filepaths as fp
import src.analysis as anal

from pathlib import Path


def batch_grating_thickness(batch_name,
                            parent_directory,
                            file_paths,
                            plot_files,
                            figure_path):
    '''
    Calculate sample batch grating thicknesses, and error, from individual files
    within batch.
    Args:
        batch_name: <string> batch name string
        parent_directory: <string> parent directory identifier string
        filepaths: <array> array of target file paths
        plot_files: <string> "True" or "False" for plotting output
        figure_path: <string> path to results for figure save
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
        sample_details = fp.sample_information(file_path=file)
        for key, value in sample_details.items():
            if key in batch_dictionary.keys():
                batch_dictionary[key].append(value)
        lateral, profile = io.read_thickness_file(
            parent_directory=parent_directory,
            file_path=file)
        out_string = sample_details[f'{parent_directory} Secondary String']
        thickness_results = anal.calculate_grating_thickness(
            x_array=lateral,
            y_array=profile,
            file_name=sample_details[f'{parent_directory} File Name'],
            sample_name=sample_details[f'{parent_directory} Secondary String'],
            plot_files=plot_files,
            out_path=Path(
                f'{figure_path}/'
                f'{batch_name}_{out_string}'
                f'_GratingThickness.png'),
            graph_path=Path(
                f'{figure_path}/'
                f'{batch_name}_{out_string}'
                f'_Plain.png'))
        batch_dictionary.update(thickness_results)
    return batch_dictionary


if __name__ == '__main__':

    ''' Organisation '''
    root = Path().absolute()
    info, directory_paths = fp.get_directory_paths(root_path=root)
    file_paths = fp.get_files_paths(
        directory_path=directory_paths['AFM Path'],
        file_string='.txt')
    parent, batches = fp.get_all_batches(file_paths=file_paths)

    ''' Loop Files '''
    for batch, filepaths in batches.items():
        out_file = Path(
            f'{directory_paths["Results Path"]}/{batch}_Grating.json')
        if out_file.is_file():
            pass
        else:
            results_dictionary = batch_grating_thickness(
                batch_name=batch,
                parent_directory=parent,
                file_paths=filepaths,
                plot_files=info['Plot Figures'],
                figure_path=Path(f'{directory_paths["Results Path"]}'))

            io.save_json_dicts(
                out_path=out_file,
                dictionary=results_dictionary)
