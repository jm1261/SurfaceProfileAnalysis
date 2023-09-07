import numpy as np

from src.userinput import trimindices
from src.fileIO import read_thickness_file
from src.plotting import xy_tworois_plot, plotafm
from src.datalevelling import calculated_level_film_thickness


def standard_error_mean(x : list) -> float:
    """
    Standard error on the mean of an array.

    Parameters
    ----------
    x: list
        Array.
    
    Returns
    -------
    SEOM: float
        Standard error on the mean.
    
    See Also
    --------
    numpy std
    numpy sqrt

    Notes
    -----
    Standard error on the mean formulation.

    Example
    -------
    None

    """
    return np.std(x) / np.sqrt(len(x) - 1)


def standard_addition_error(delta_x,
                            delta_y):
    '''
    Error of adding/subtracting two values with an associated error.
    Args:
        delta_x: <float> delta_x data point
        delta_y: <float> delta_y data point
    Returns:
        delta_z: <float> associated error with added/subtracted value
    '''
    return np.sqrt((delta_x ** 2) + (delta_y ** 2))


def average_step_and_error(x : list) -> dict:
    """
    Calculate average array and return standard error on the mean.

    Parameters
    ----------
    x: list
        Array to average.
    
    Returns
    -------
    dictionary: dictionary
        {
            Average Result:,
            Average Error:
        }
    
    See Also
    --------
    standard_error_mean

    Notes
    -----
    None

    Example
    -------
    None

    """
    return {
        "Average Result": np.average(np.abs(x)),
        "Average Error": standard_error_mean(x=np.abs(x))}


def calc_stepheight(region_1,
                    region_2,
                    sample_name):
    '''
    Calculate step height between two regions.
    Args:
        region_1: <array> profile (y) array for region 1
        region_2: <array> profile (y) array for region 2
        sample_name: <string> sample name identifier string
    Returns:
        step_height: <dict>
            Step Height
            Step Height Error
    '''
    mean_region1 = np.mean(a=region_1)
    mean_region2 = np.mean(a=region_2)
    error_region1 = standard_error_mean(x=region_1)
    error_region2 = standard_error_mean(x=region_2)
    step_height = np.abs(mean_region2 - mean_region1)
    step_height_error = standard_addition_error(
        delta_x=error_region1,
        delta_y=error_region2)
    return {
        f'{sample_name} Step Height': step_height,
        f'{sample_name} Step Height Error': step_height_error}


def calculate_grating_thickness(x_array,
                                y_array,
                                file_name,
                                sample_name,
                                plot_files,
                                out_path,
                                graph_path):
    '''
    Calculate grating thickness based on regions of interest.
    Args:
        x_array: <array> x-data array
        y_array: <array> y-data array
        file_name: <string> file identifier string
        sample_name: <string> sample identifier string
        plot_files: <string> "True" or "False" for plotting output
        out_path: <string> path to save
    Returns:
        thickness_results <dict>
            Region 1 Trim Index
            Region 1 Trimmed X
            Region 1 Trimmed Y
            Region 2 Trim Index
            Region 2 Trimmed X
            Region 2 Trimmed Y
            Step Height
            Step Height Error
    '''
    region1 = trimindices(
        x_array=x_array,
        y_array=y_array,
        file_name=file_name,
        region=f'{sample_name} Region 1')
    region2 = trimindices(
        x_array=x_array,
        y_array=y_array,
        file_name=file_name,
        region=f'{sample_name} Region 2')
    step_height = calc_stepheight(
        region_1=y_array[
            region1[f'{sample_name} Region 1 Trim Index'][0]:
            region1[f'{sample_name} Region 1 Trim Index'][1]],
        region_2=y_array[
            region2[f'{sample_name} Region 2 Trim Index'][0]:
            region2[f'{sample_name} Region 2 Trim Index'][1]],
        sample_name=sample_name)
    thickness_results = dict(
        region1,
        **region2,
        **step_height)
    step = step_height[f'{sample_name} Step Height']
    if plot_files == 'True':
        plotafm(
            x=x_array,
            y=y_array,
            label=f'{sample_name}',
            xlabel='Lateral [um]',
            ylabel='Profile [nm]',
            title=f'{file_name}',
            out_path=graph_path,
            line=True)
        xy_tworois_plot(
            x=x_array,
            y=y_array,
            label=f'{sample_name}',
            text_string=f'step = {step:.2f} nm',
            x1=x_array[(region1[f'{sample_name} Region 1 Trim Index'])[0]],
            x2=x_array[(region1[f'{sample_name} Region 1 Trim Index'])[1]],
            x3=x_array[(region2[f'{sample_name} Region 2 Trim Index'])[0]],
            x4=x_array[(region2[f'{sample_name} Region 2 Trim Index'])[1]],
            xlabel='Lateral [um]',
            ylabel='Profile [nm]',
            title=f'{file_name}',
            out_path=out_path,
            line=True)
    return thickness_results


def calculate_dektak_thicks(file_path : str,
                            file_name : str,
                            out_path : str,
                            plot_dict : dict) -> dict:
    """
    Read Dektak file and calculate individual step height results.

    Parameters
    ----------
    file_path, file_name, out_path: string
        Path to file, file name string, path to save out.
    plot_dict : dictionary
        Plot settings dictionary containing:
            {
                "width": plot width,\n
                "height": plot height,\n
                "dpi": dots per square inch,\n
                "grid": True/False,\n
                "legend_loc": legend location,\n
                "legend_col": legend column number,\n
                "legend_size": size of legend text,\n
                "axis_fontsize": font size for axis labels,\n
                "label_size": size for tick labels
            }
    
    Returns
    -------
    step_results: dictionary
        Calculated step height data:
            {
                Step height (nm)
                Step height error (nm)
                Quadratic (a, b, c)
                Quadratic errors (a, b, c)
            }

    See Also
    --------
    read_thickness_file
    calculated_level_film_thickness

    Notes
    -----
    Example
    -------
    None

    """
    lateral, profile = read_thickness_file(
        file_type="Dektak",
        file_path=file_path)
    step_results = calculated_level_film_thickness(
        x_array=lateral,
        y_array=profile,
        file_name=file_name,
        plot_dict=plot_dict,
        out_path=out_path)
    return step_results