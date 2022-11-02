import src.fileIO as io
import src.filepaths as fp
import src.userinput as ui
import src.analysis as anal

from pathlib import Path


def batch_grating_thickness(batch_name,
                            file_paths):
    '''
    Calculate sample batch grating thicknesses, and error, from individual files
    within batch.
    Args:
        batch_name: <string> batch name string
        filepaths: <array> array of target file paths
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
        "Sample Name": [],
        "Grating Period": []}
    for file in file_paths:
        sample_details = fp.grating_information(file_path=file)
        for key, value in sample_details.items():
            if key in batch_results.keys():
                batch_results[key].append(value)
        lateral, profile = io.read_thickness_file(
            sample_details=sample_details)
        thickness_results = anal.calculate_grating_thickness(
            x_array=lateral,
            y_array=profile,
            file_name=sample_details['File Name'],
            sample_name=sample_details['Grating Period'])
        batch_results.update(thickness_results)
    return batch_results


if __name__ == '__main__':

    ''' Organisation '''
    root = Path().absolute()
    _, grating_path, results_path = fp.directory_paths(root_path=root)
    file_paths = fp.get_files_paths(
        root_path=grating_path,
        file_string='.csv')
    batches = fp.find_all_batches(file_paths=file_paths)

    ''' Loop Files '''
    for batch, filepaths in batches.items():
        results_dictionary = batch_grating_thickness(
            batch_name=batch,
            file_paths=filepaths)

        io.save_json_dicts(
            out_path=Path(
                f'{results_path}/{batch}_Series_GratingThickness.json'),
            dictionary=results_dictionary)
