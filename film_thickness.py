import src.fileIO as io
import src.filepaths as fp
import src.analysis as anal
import src.datalevelling as dl

from pathlib import Path


def batch_filmthickness(batch_name,
                        file_paths):
    '''
    Calculate sample batch film thickness, average thickness and error, from
    individual files within batch.
    Args:
        batch_name: <string> batch name string
        filepaths: <array> array of target file paths
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
        "File Path": []}
    film_thicknesses = []
    for file in file_paths:
        sample_details = fp.film_information(file_path=file)
        for key, value in sample_details.items():
            if key in batch_results.keys():
                batch_results[key].append(value)
        lateral, profile = io.read_thickness_file(
            sample_details=sample_details)
        step_results = dl.calculated_level_film_thickness(
            x_array=lateral,
            y_array=profile,
            file_name=sample_details['File Name'],
            sample_name=sample_details['Repeat Number'])
        batch_results.update(step_results)
        film_thicknesses.append(
            step_results[
                f'{sample_details["Repeat Number"]} Film Thickness'])
    thickness_results = anal.average_and_error(x=film_thicknesses)
    results_dictionary = dict(
        batch_results,
        **thickness_results)
    return results_dictionary


if __name__ == '__main__':

    ''' Organisation '''
    root = Path().absolute()
    film_path, _, results_path = fp.directory_paths(root_path=root)
    file_paths = fp.get_files_paths(
        root_path=film_path,
        file_string='.csv')
    batches = fp.find_all_batches(file_paths=file_paths)

    ''' Loop Batches '''
    for batch, filepaths in batches.items():
        results_dictionary = batch_filmthickness(
            batch_name=batch,
            file_paths=filepaths)

        io.save_json_dicts(
            out_path=Path(f'{results_path}/{batch}_Series_FilmThickness.json'),
            dictionary=results_dictionary)
