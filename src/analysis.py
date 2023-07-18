import numpy as np
import scipy.optimize as opt

from src.userinput import trimindices
from src.fileIO import read_thickness_file
from src.plotting import xy_tworois_plot, plotafm
from src.datalevelling import calculated_level_film_thickness


def standard_error_mean(x):
    '''
    Standard error of the mean of an array.
    Args:
        x: <array> data array
    Returns:
        SEOM: <float> standard error of the mean of x
    '''
    return np.std(x) / np.sqrt(len(x) - 1)


def standard_addition_error(delta_x,
                            delta_y):
    '''
    Error of adding/subtracting two values with an associated error.
    Args:
        delta_x: <float> delta_x data point
        delta_y: <float> delta_y data point
    Returns:
        delta_z: <float> associated error with added/substracted value
    '''
    return np.sqrt((delta_x ** 2) + (delta_y ** 2))


def average_step_and_error(x):
    '''
    Calculate average array and return standard error on the mean. Takes the
    absolute value of step height x, to counter any differences in measuring
    techniques that result in negative step heights.
    Args:
        x: <array> data array
    Returns:
        result: <dict>
            Average Result
            Average Error
    '''
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


def calculate_dektak_thicks(parent_directory,
                            file_path,
                            file_name,
                            sample_name,
                            plot_files,
                            out_path):
    '''
    Read Dektak file and calculate individual step height result.
    Args:
        parent_directory: <string> parent directory identifier (e.g., Dektak)
        file_path: <string> path to file
        file_name: <string> file identifier
        sample_name: <string> sample name identifier
        plot_files: <string> "True" or "False" for plotting output
        out_path: <string> path to save
    Returns:
        step_results: <dict> step height, error, quadratic, errors
    '''
    lateral, profile = read_thickness_file(
        parent_directory=parent_directory,
        file_path=file_path)
    step_results = calculated_level_film_thickness(
        x_array=lateral,
        y_array=profile,
        file_name=file_name,
        sample_name=sample_name,
        plot_files=plot_files,
        out_path=out_path)
    return step_results