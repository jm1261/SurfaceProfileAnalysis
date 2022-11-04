import src.fileIO as io
import src.filepaths as fp

from pathlib import Path
from film_thickness import batch_filmthickness
from grating_thickness import batch_grating_thickness


if __name__ == '__main__':

    ''' Organisation '''
    root = Path().absolute()
    film_path, grating_path, results_path = fp.directory_paths(root_path=root)

    ''' Dektak Films '''
    dektak_file_paths = fp.get_files_paths(
        root_path=film_path,
        file_string='.csv')
    dektak_batches = fp.find_all_batches(file_paths=dektak_file_paths)
    for batch, filepaths in dektak_batches.items():
        if Path(f'{results_path}/{batch}_FilmThickness.json').is_file():
            pass
        else:
            results_dictionary = batch_filmthickness(
                batch_name=batch,
                file_paths=filepaths)
            io.save_json_dicts(
                out_path=Path(f'{results_path}/{batch}_FilmThickness.json'),
                dictionary=results_dictionary)

    ''' AFM Files '''
    afm_file_paths = fp.get_files_paths(
        root_path=grating_path,
        file_string='.csv')
    afm_batches = fp.find_all_batches(file_paths=afm_file_paths)
    for batch, filepaths in afm_batches.items():
        if Path(f'{results_path}/{batch}_GratingThickness.json').is_file():
            pass
        else:
            results_dictionary = batch_grating_thickness(
                batch_name=batch,
                file_paths=filepaths)
            io.save_json_dicts(
                out_path=Path(
                    f'{results_path}/{batch}_GratingThickness.json'),
                dictionary=results_dictionary)
