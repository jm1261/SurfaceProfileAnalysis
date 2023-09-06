import src.fileIO as io
import src.filepaths as fp
import src.analysis as anal
import src.datalevelling as dl

from pathlib import Path

'''
Need to add widths and feature mode, so something that measures a feature width
and something that measures both a thickness and a width. Also Andrea not happy
with the levelling aspect so might want to have that in as an option, i.e.,
sometimes it is not always necessary to do some levelling, sometimes it's nice
to just take an average like this code used to.
'''


def batch_dektak_thicks(batch_name,
                        parent_directory,
                        file_paths,
                        plot_files,
                        figure_path):
    batch_dictionary = fp.update_batch_dictionary(
        parent=parent_directory,
        batch_name=batch_name,
        file_paths=file_paths)
    film_thicknesses = []
    for file in file_paths:
        sample_details = fp.sample_information(file_path=file)
        out_string = sample_details[f'{parent_directory} Secondary String']
        step_results = anal.calculate_dektak_thicks(
            parent_directory=parent_directory,
            file_path=file,
            file_name=sample_details[f'{parent_directory} File Name'],
            sample_name=sample_details[f'{parent_directory} Secondary String'],
            plot_files=plot_files,
            out_path=Path(
                f'{figure_path}/{batch_name}_{out_string}_Dektak.png'))
        batch_dictionary.update(step_results)
        film_thicknesses.append(step_results[f'{out_string} Thickness'])
    thickness_results = anal.average_step_and_error(x=film_thicknesses)
    results_dictionary = dict(
        batch_dictionary,
        **thickness_results)
    return results_dictionary


if __name__ == '__main__':
    root = Path().absolute()
    info, directory_paths = fp.get_directory_paths(root_path=root)
    file_paths = fp.get_files_paths(
        directory_path=directory_paths['Dektak Path'],
        file_string='.csv')
    parent, batches = fp.get_all_batches(file_paths=file_paths)
    for batch, filepaths in batches.items():
        out_file = Path(
            f'{directory_paths["Dektak Results Path"]}/{batch}_Dektak.json')
        if out_file.is_file():
            pass
        else:
            results_dictionary = batch_dektak_thicks(
                batch_name=batch,
                parent_directory=parent,
                file_paths=filepaths,
                plot_files=info['Plot Figures'],
                figure_path=Path(f'{directory_paths["Dektak Results Path"]}'))
            io.save_json_dicts(
                out_path=out_file,
                dictionary=results_dictionary)