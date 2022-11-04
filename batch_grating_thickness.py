import src.fileIO as io
import src.filepaths as fp
import src.userinput as ui
import src.analysis as anal

from pathlib import Path


def batch_grating_thickness(batch_name,
                            file_paths,
                            plot_files,
                            figure_path):
    '''
    Calculate sample batch grating thicknesses, and error, from individual files
    within batch.
    Args:
        batch_name: <string> batch name string
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
    batch_results = {
        "Batch Name": batch_name,
        "File Name": [],
        "File Path": [],
        "Secondary String": []}
    for file in file_paths:
        sample_details = fp.sample_information(file_path=file)
        for key, value in sample_details.items():
            if key in batch_results.keys():
                batch_results[key].append(value)
        lateral, profile = io.read_thickness_file(
            sample_details=sample_details)
        thickness_results = anal.calculate_grating_thickness(
            x_array=lateral,
            y_array=profile,
            file_name=sample_details['File Name'],
            sample_name=sample_details['Secondary String'],
            plot_files=plot_files,
            out_path=Path(
                f'{figure_path}/'
                f'{batch_name}_{sample_details["Secondary String"]}'
                f'_GratingThickness.png'))
        batch_results.update(thickness_results)
    return batch_results


if __name__ == '__main__':

    ''' Organisation '''
    root = Path().absolute()
    _, afm_path, results_path, info = fp.directory_paths(root_path=root)
    file_paths = fp.get_files_paths(
        root_path=afm_path,
        file_string='.csv')
    batches = fp.find_all_batches(file_paths=file_paths)

    ''' Loop Files '''
    for batch, filepaths in batches.items():
        if Path(f'{results_path}/{batch}_GratingThickness.json').is_file():
            pass
        else:
            results_dictionary = batch_grating_thickness(
                batch_name=batch,
                file_paths=filepaths,
                plot_files=info['Plot Figures'],
                figure_path=Path(f'{results_path}'))

            io.save_json_dicts(
                out_path=Path(
                    f'{results_path}/{batch}_GratingThickness.json'),
                dictionary=results_dictionary)
