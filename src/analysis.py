import numpy as np

from src.userinput import trim_region


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


def average_and_error(x):
    '''
    Calculate average array and return standard error on the mean.
    Args:
        x: <array> data array
    Returns:
        result: <dict>
            Average Result
            Average Error
    '''
    return {
        "Average Result": np.average(x),
        "Average Error": standard_error_mean(x=x)}


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
                                sample_name):
    '''
    Calculate grating thickness based on regions of interest.
    Args:
        x_array: <array> x-data array
        y_array: <array> y-data array
        file_name: <string> file identifier string
        sample_name: <string> sample identifier string
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
    region1 = trim_region(
        x_array=x_array,
        y_array=y_array,
        file_name=file_name,
        region=f'{sample_name} Region 1')
    region2 = trim_region(
        x_array=x_array,
        y_array=y_array,
        file_name=file_name,
        region=f'{sample_name} Region 2')
    step_height = calc_stepheight(
        region_1=region1[f'{sample_name} Region 1 Trimmed Y'],
        region_2=region2[f'{sample_name} Region 2 Trimmed Y'],
        sample_name=sample_name)
    thickness_results = dict(
        region1,
        **region2,
        **step_height)
    return thickness_results