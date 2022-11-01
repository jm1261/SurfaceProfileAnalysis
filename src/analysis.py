import numpy as np


def mean_array(x):
    '''
    Calculate mean of array.
    Args:
        x: <array> data array
    Returns:
        mean: <float> mean value of x
    '''
    return np.sum(x) / len(x)


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


def calc_stepheight(region_1,
                    region_2):
    '''
    Calculate step height between two regions.
    Args:
        region_1: <array> profile (y) array for region 1
        region_2: <array> profile (y) array for region 2
    Returns:
        step_height: <dict>
            Step Height
            Step Height Error
    '''
    mean_region1 = mean_array(x=region_1)
    mean_region2 = mean_array(x=region_2)
    error_region1 = standard_error_mean(x=region_1)
    error_region2 = standard_error_mean(x=region_2)
    step_height = np.abs(mean_region2 - mean_region1)
    step_height_error = standard_addition_error(
        delta_x=error_region1,
        delta_y=error_region2)
    return {
        "Step Height": step_height,
        "Step Height Error": step_height_error}
