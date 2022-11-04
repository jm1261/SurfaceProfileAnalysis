import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import least_squares


def level_regions_interests(x, y,
                            file_name):
    '''
    Use matplotlib ginput to select the two regions of interest to level data.
    First region should be above or below the step, second region should be
    below or above the step.
    Args:
        x: <array> x-data array
        y: <arrau> y-data array
        file_name: <string> file identifier for legend
    Returns:
        range_left: <array> 2 length array of x-coordinates for left region of
                    interest
        range_right: <array> 2 length array of x-coordinates for right region of
                    interest
    '''
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[10, 7])
    ax.plot(
        x,
        y,
        'b',
        lw=2,
        label=file_name)
    ax.legend(
        loc=0,
        prop={'size': 14})
    fig.show()
    regions = np.array(plt.ginput(4)).astype(float)
    range_left = regions[0: 2, 0]
    range_right = regions[2: 4, 0]
    plt.close(fig)
    return range_left, range_right


def crop_xydata(x, y,
                x_range):
    '''
    Crop xy data to specific x_range.
    Args:
        x: <array> x-data array
        y: <array> y-data array
        x_range: <array> x min and x max coordinate for range to trim
    Returns:
        crop: <dict>
            range Indices
            range X Crop
            range Y crop
    '''
    min_index = np.argmin(np.abs(x - x_range[0]))
    max_index = np.argmin(np.abs(x - x_range[1]))
    x_crop = x[min_index: max_index]
    y_crop = y[min_index: max_index]
    return x_crop, y_crop


def standard_quadratic_equation(a,
                                b,
                                c,
                                x):
    '''
    Calculate the standard quadratic equation.
    Args:
        a, b, c: <float> a, b, and c for quadratic equation
        x: <array> x-data array
    Returns:
        (a * (x ** 2)) + (b * x) + c
    '''
    return (a * (x ** 2)) + (b * x) + c


def residual_quadratic_equation(parameters,
                                x, y):
    '''
    Calculate the residual from the quadratic equation.
    Args:
        parameters: <array> a, b, c for quadratic equation
        x: <array> x-data array
        y: <array> y-data array
    Returns:
        quadtraic_equation(a, b, c, x) - y
    '''
    return (
        standard_quadratic_equation(
            parameters[0],
            parameters[1],
            parameters[2],
            x)
        - y)


def residual_quadratic_step(step_parameters,
                            x_base, y_base,
                            x_step, y_step):
    '''
    Calculate the residual quadratic step function to return the residuals from
    both quadratic equations before and after the step.
    Args:
        step_parameters: <array> a, b, c, step initial parameters for quadratic
                            equation
        x_base: <array> x-data array for the base level
        y_base: <array> y-data array for the base level
        x_step: <array> x-data array for the step level
        y_step: <array> y-data array for the step level
    Returns:
        residual: <array> residual parameters from the quadratic equation
    '''
    quadratic_parameters = step_parameters[0: -1]
    initial_step = step_parameters[-1]
    residual = np.append(
        residual_quadratic_equation(
            quadratic_parameters,
            x_base,
            y_base),
        residual_quadratic_equation(
            quadratic_parameters,
            x_step,
            y_step - initial_step))
    return residual


def fit_quadratic(x, y):
    '''
    Fit quadratic equation and calculate least squares parameters.
    Args:
        x: <array> x-data array
        y: <array> y-data array
    Returns:
        parameters: <array> initial parameters for quadratic equation a, b, c
    '''
    initial_parameters = [0, np.average(x), np.average(y)]
    scales = [1e-3, np.average(x), np.abs(np.average(y))]
    residual_least_squares = least_squares(
        residual_quadratic_equation,
        initial_parameters,
        args=(x, y),
        x_scale=scales)
    parameters = residual_least_squares.x
    return parameters


def calculate_filmthickness(initial_parameters,
                            x_base,
                            y_base,
                            x_step,
                            y_step,
                            scales,
                            sample_name):
    '''
    Use residual least squares with the residual quadratic step function to
    calculate the step height after data levelling.
    Args:
        initial_parameters: <array> initial parameters for a, b, c, step
        x_base: <array> x data array for base crop
        y_base: <array> y data array for base crop
        x_step: <array> x data array for step crop
        y_step: <array> y data array for step crop
        scales: <array> scales for a, b, c, step values
        sample_name: <string> sample name identifier
    Returns:
        step_result: <dict>
            Film Thickness (nm)
            Film Thickness Error (nm)
            Quadratic (a, b, c)
            Quadratic Errors (a, b, c)
    '''
    residual_least_squares = least_squares(
        residual_quadratic_step,
        initial_parameters,
        args=(
            x_base,
            y_base,
            x_step,
            y_step),
        x_scale=scales)
    a, b, c, step_height = residual_least_squares.x
    raw_errors = residual_least_squares.jac
    cov = np.linalg.inv(raw_errors.T.dot(raw_errors))
    a_error, b_error, c_error, step_error = np.sqrt(np.diag(cov))
    return {
        f'{sample_name} Film Thickness': step_height,
        f'{sample_name} Film Thickness Error': step_error,
        f'{sample_name} Quadratic': [a, b, c],
        f'{sample_name} Quadratic Errors': [a_error, b_error, c_error]}


def calculated_level_film_thickness(x_array,
                                    y_array,
                                    file_name,
                                    sample_name,
                                    plot_files,
                                    out_path):
    '''
    Calculate the film thickness, error, quadratic parameters, and quadratic
    parameter errors for levelled film thickness data.
    Args:
        x_array: <array> x-data array
        y_array: <array> y-data array
        file_name: <string> file identifier
        sample_name: <string> sample name identifier
        plot_files: <string> "True" or "False" for plotting output
        out_path: <string> path to save
    Returns:
        step_results: <dict>
            Step Height (nm)
            Step Height Error (nm)
            Quadratic (a, b, c)
            Quadratic Errors (a, b, c)
    '''
    range_left, range_right = level_regions_interests(
        x=x_array,
        y=y_array,
        file_name=file_name)
    x_base, y_base = crop_xydata(
        x=x_array,
        y=y_array,
        x_range=range_left)
    x_step, y_step = crop_xydata(
        x=x_array,
        y=y_array,
        x_range=range_right)
    initial_parameters_base = fit_quadratic(
        x=x_base,
        y=y_base)
    initial_parameters_step = fit_quadratic(
        x=x_step,
        y=y_step)
    step_estimate = np.average(y_step) - np.average(y_base)
    initial_parameters = np.average([
        initial_parameters_base,
        initial_parameters_step],
        0)
    initial_parameters = np.append(initial_parameters, step_estimate)
    scales = [1e-3, 500, 1, np.abs(step_estimate)]
    step_results = calculate_filmthickness(
        initial_parameters=initial_parameters,
        x_base=x_base,
        y_base=y_base,
        x_step=x_step,
        y_step=y_step,
        scales=scales,
        sample_name=sample_name)
    if plot_files == "True":
        plot_dektak_thicknesses(
            x_array=x_array,
            y_array=y_array,
            quadratic_parameters=step_results[f'{sample_name} Quadratic'],
            step_height=step_results[f'{sample_name} Film Thickness'],
            out_path=out_path)
    return step_results


def plot_dektak_thicknesses(x_array,
                            y_array,
                            quadratic_parameters,
                            step_height,
                            out_path):
    '''
    Plot dektak step height calculation with data levelled.
    Args:
        x_array: <array> x-data array
        y_array: <array> y-data array
        quadratic_parameters: <array> quadratic parameters [a, b, c]
        step_height: <float> calculated step height (nm)
        out_path: <string> path to save
    Returns:
        None
    '''
    fig, (ax1, ax2) = plt.subplots(
        nrows=1,
        ncols=2,
        figsize=[10, 7])
    ax1.plot(
        x_array,
        y_array,
        'b',
        lw=2,
        label='Data')
    y_baseline = standard_quadratic_equation(
        a=quadratic_parameters[0],
        b=quadratic_parameters[1],
        c=quadratic_parameters[2],
        x=x_array)
    ax1.plot(
        x_array,
        y_baseline,
        'r',
        lw=2,
        label='Quadratic Baseline')
    ax1.legend(
        loc=0,
        prop={'size': 14})
    y_corrected = y_array - y_baseline
    ax2.plot(
        x_array,
        y_corrected,
        'b',
        lw=2,
        label='Background Corrected Data')
    y_step = step_height * np.ones_like(y_array)
    ax2.plot(
        x_array,
        y_step,
        'r',
        lw=2,
        label=f'step = {step_height:.2f} nm')
    ax2.plot(
        x_array,
        np.zeros_like(y_array),
        'g',
        lw=2)
    ax2.legend(
        loc=0,
        prop={'size': 14})
    fig.tight_layout()
    plt.savefig(out_path)
    fig.clf()
    plt.cla()
    plt.close(fig)
