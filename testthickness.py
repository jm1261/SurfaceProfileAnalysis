import os
import src.fileIO as io
import src.filepaths as fp
import src.userinput as ui
import src.analysis as anal

from pathlib import Path

if __name__ == '__main__':

    ''' Organisation '''
    root = Path().absolute()
    file_paths = fp.get_files_paths(
        root_path=root,
        file_string='.csv')
    data_path, results_path = fp.directory_paths(root_path=root)

    ''' Loop Files '''
    for file in file_paths:
        sample_details = fp.sample_information(file_path=file)
        lateral, profile = io.read_thickness_file(sample_details=sample_details)

        ''' Find Regions of Interest '''
        region1 = ui.trim_region(
            x_array=lateral,
            y_array=profile,
            file_name=sample_details['File Name'],
            region='Region 1')
        region2 = ui.trim_region(
            x_array=lateral,
            y_array=profile,
            file_name=sample_details['File Name'],
            region='Region 2')

        ''' Calculate Step Height '''
        step_height = anal.calc_stepheight(
            region_1=region1['Region 1 Trimmed Y'],
            region_2=region2['Region 2 Trimmed Y'])

        ''' Results '''
        results_dictionary = dict(
            sample_details,
            **region1,
            **region2,
            **step_height)
        print(results_dictionary)
        io.save_json_dicts(
            out_path=Path(f'{results_path}/{sample_details["File Name"]}.json'),
            dictionary=results_dictionary)
