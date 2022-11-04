import src.fileIO as io
import src.filepaths as fp
import src.analysis as anal
import src.datalevelling as dl

from pathlib import Path


def batch_filmthickness(batch_name,
                        file_paths,
                        plot_files,
                        figure_path):
    '''
    Calculate sample batch film thickness, average thickness and error, from
    individual files within batch.
    Args:
        batch_name: <string> batch name string
        filepaths: <array> array of target file paths
        plot_files: <string> "True" or "False" for plotting output
        figure_path: <string> path to results for figure save
    Returns:
        results_dictionary: <dict>
            Batch Name
            File Name
            File Patch
            Individual film thicknesses
            Individual film errors
            Individual quadratic constants
            Individual quadratic constants errors
            Average film thickness for batch
            Average film thickness error for batch
    '''
    batch_results = {
        "Batch Name": batch_name,
        "File Name": [],
        "File Path": [],
        "Secondary String": []}
    film_thicknesses = []
    for file in file_paths:
        sample_details = fp.sample_information(file_path=file)
        for key, value in sample_details.items():
            if key in batch_results.keys():
                batch_results[key].append(value)
        lateral, profile = io.read_thickness_file(
            sample_details=sample_details)
        step_results = dl.calculated_level_film_thickness(
            x_array=lateral,
            y_array=profile,
            file_name=sample_details['File Name'],
            sample_name=sample_details['Secondary String'],
            plot_files=plot_files,
            out_path=Path(
                f'{figure_path}/'
                f'{batch_name}_{sample_details["Secondary String"]}'
                f'_FilmThickness.png'))
        batch_results.update(step_results)
        film_thicknesses.append(
            step_results[
                f'{sample_details["Secondary String"]} Film Thickness'])
    thickness_results = anal.average_step_and_error(x=film_thicknesses)
    results_dictionary = dict(
        batch_results,
        **thickness_results)
    return results_dictionary


if __name__ == '__main__':

    ''' Organisation '''
    root = Path().absolute()
    dektak_path, _, results_path, info = fp.directory_paths(root_path=root)
    file_paths = fp.get_files_paths(
        root_path=dektak_path,
        file_string='.csv')
    batches = fp.find_all_batches(file_paths=file_paths)

    ''' Loop Batches '''
    for batch, filepaths in batches.items():
        if Path(f'{results_path}/{batch}_FilmThickness.json').is_file():
            pass
        else:
            results_dictionary = batch_filmthickness(
                batch_name=batch,
                file_paths=filepaths,
                plot_files=info['Plot Figures'],
                figure_path=Path(f'{results_path}'))

            io.save_json_dicts(
                out_path=Path(f'{results_path}/{batch}_FilmThickness.json'),
                dictionary=results_dictionary)
