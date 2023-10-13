import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import least_squares


def level_regions_interests(x : list,
                            y : list,
                            file_name : str) -> list:
    """
    Level data between two regions of interest.

    Use matplotlib ginput to select two regions of interest.

    Parameters
    ----------
    x, y: list
        x- and y- data arrays.
    file_name: string
        File name identifier for legend.
    
    Returns
    -------
    range_left, range_right: list
        Regions of interest on the left and right side of the x-array.
    
    See Also
    --------
    matplotlib ginput

    Notes
    -----
    Uses matplotlib ginput to select the two regions of interest to level data.
    First region should be on the same level, second region on a different
    level. Note that the graph only takes 4 inputs. A standard ginput timer is
    also applied.

    Example
    -------
    None

    """
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


def crop_xydata(x : list,
                y : list,
                x_range : list) -> list:
    """
    Crop x- y- data to specific x range.

    Parameters
    ----------
    x, y, x_range: list
        x data, y data, x range from region of interest.
    
    Returns
    -------
    x_crop, y_crop: list
        Trimmed x and y data arrays.
    
    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    None

    """
    min_index = np.argmin(np.abs(x - x_range[0]))
    max_index = np.argmin(np.abs(x - x_range[1]))
    x_crop = x[min_index: max_index]
    y_crop = y[min_index: max_index]
    return x_crop, y_crop


def standard_quadratic_equation(a : float,
                                b : float,
                                c : float,
                                x : float) -> float:
    """
    Evaluate the standard quadratic equation at specified x value.

    Parameters
    ----------
    a, b, c, x: float
        a, b, c from the quadratic equation, x value at which to evaluate.
    
    Returns
    -------
    y: float
        Evaluation of the quadratic equation at specified x value.
    
    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    None

    """
    return (a * (x ** 2)) + (b * x) + c


def residual_quadratic_equation(parameters : list,
                                x : float,
                                y : float) -> float:
    """
    Calculate the residual from the quadratic equation.

    Parameters
    ----------
    parameters: list
        Quadratic equation a, b, c.
    x, y: float
        x and y values at which to evaluate the residuals.
    
    Returns
    -------
    residual: float

    See Also
    --------
    standard_quadratic_equation

    Notes
    -----
    None

    Example
    -------
    None

    """
    return (
        standard_quadratic_equation(
            parameters[0],
            parameters[1],
            parameters[2],
            x)
        - y)


def residual_quadratic_step(step_parameters : list,
                            x_base : list,
                            y_base : list,
                            x_step : list,
                            y_step : list) -> list:
    """
    Calculate the residual quadratic step function.

    Return the residuals from both quadratic equations before and after step.

    Parameters
    ----------
    step_parameters, x_base, y_base, x_step, y_step: list
        Quadratic step parameters, x y data from left x-range data, x y data
        from right x-range data.
    
    Returns
    -------
    residual: list
        Residual parameters from the quadratic equation.
    
    See Also
    --------
    residual_quadratic_equation
    standard_quadratic_equation
    
    Notes
    -----
    None

    Example
    -------
    None

    """
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


def fit_quadratic(x : list, y: list) -> list:
    """
    Fit quadratic equation.
    
    Calculate least squares parameters.

    Parameters
    ----------
    x, y: list
        x y data sets
    
    Returns
    -------
    parameters: list
        Quadratic equation parameters.
    
    See Also
    --------
    least_squares
    residual_quadratic_equation
    standard_quadratic_equation

    Notes
    -----
    None

    Example
    -------
    None

    """
    initial_parameters = [0, np.average(x), np.average(y)]
    scales = [1e-3, np.average(x), np.abs(np.average(y))]
    residual_least_squares = least_squares(
        residual_quadratic_equation,
        initial_parameters,
        args=(x, y),
        x_scale=scales)
    parameters = residual_least_squares.x
    return parameters


def calculate_filmthickness(initial_parameters : list,
                            x_base : list,
                            y_base : list,
                            x_step : list,
                            y_step : list,
                            scales : list,
                            file_name : str) -> dict:
    """
    Use residual least squares with the residual quadratic step function to
    calculate the step height after data levelling.

    Parameters
    ----------
    initial_parameters, x_base, y_base, x_step, y_step, scales: list
        Initial parameters for a, b, c, step, x data array for base crop, y data
        array for base crop, x data array for step crop, y data array for step
        crop, scales for a, b, c, step values.
    file_name: string
        Sample name identifier.

    Returns
    -------
    step_result: dictionary
        Results dictionary:
            {
                Film Thickness (nm)
                Film Thickness Error (nm)
                Quadratic (a, b, c)
                Quadratic Errors (a, b, c)
            }
    
    See Also
    --------
    least_squares
    residual_quadratic_step
    residual_least_squares

    Notes
    -----
    None

    Example
    -------
    None

    """
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
        f'{file_name} Thickness': step_height,
        f'{file_name} Thickness Error': step_error,
        f'{file_name} Quadratic': [a, b, c],
        f'{file_name} Quadratic Errors': [a_error, b_error, c_error]}


def cm_to_inches(cm: float) -> float:
    """
    Returns centimeters as inches.

    Uses the conversion rate to convert a value given in centimeters to inches.
    Useful for matplotlib plotting.

    Parameters
    ----------
    cm : float
        Value of the desired figure size in centimeters.

    Returns
    -------
    inches : float
        Value of the desired figure size in inches.

    See Also
    --------
    None

    Notes
    -----
    Conversion rate given to 6 decimal places, but inches rounded to 2 decimal
    places.

    Examples
    --------
    >>> cm = 15
    >>> inches = cm_to_inches(cm=cm)
    >>> inches
    5.91

    """
    return round(cm * 0.393701, 2)


def plot_dektak_thicknesses(x_array : list,
                            y_array : list,
                            quadratic_parameters : list,
                            step_height : float,
                            plot_dict : dict,
                            out_path : str) -> None:
    """
    Plot dektak step height calculation with data levelled.

    Parameters
    ----------
    x_array, y_array, quadratic_parameters: list
        x-data array, y-data array, quadratic parameters [a, b, c].
    step_height: float
        Calculated step height (nm).
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
    out_path: string
        Path to save.

    Returns
    -------
    None

    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    None

    """
    fig, (ax1, ax2) = plt.subplots(
        nrows=1,
        ncols=2,
        figsize=[
            cm_to_inches(cm=plot_dict["width"]),
            cm_to_inches(cm=plot_dict["height"])],
        dpi=plot_dict["dpi"])
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
    if plot_dict["grid"] == "True":
        grid = True
    else:
        grid = False
    ax1.grid(
        visible=grid,
        alpha=0.5)
    ax1.plot(
        x_array,
        y_baseline,
        'r',
        lw=2,
        label='Quadratic Baseline')
    ax1.legend(
        loc=plot_dict["legend_loc"],
        ncol=plot_dict["legend_col"],
        prop={'size': plot_dict["legend_size"]})
    y_corrected = y_array - y_baseline
    ax2.plot(
        x_array,
        y_corrected,
        'b',
        lw=2,
        label='Level Data')
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
    ax2.grid(
        visible=grid,
        alpha=0.5)
    ax2.legend(
        loc=plot_dict["legend_loc"],
        ncol=plot_dict["legend_col"],
        prop={'size': plot_dict["legend_size"]})
    ax1.set_xlabel(
        'Lateral (mm)',
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold',
        color='black')
    ax2.set_xlabel(
        'Lateral (mm)',
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold',
        color='black')
    ax1.set_ylabel(
        'Profile (nm)',
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold',
        color='black')
    ax2.set_ylabel(
        'Vertical (nm)',
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold',
        color='black')
    fig.tight_layout()
    plt.savefig(out_path)
    fig.clf()
    plt.cla()
    plt.close(fig)


def calculated_level_film_thickness(x_array : list,
                                    y_array : list,
                                    file_name : str,
                                    plot_dict : dict,
                                    out_path : str) -> dict:
    """
    Calculate the film thickness of levelled Dektak data.

    Calculate the film thickness, error, quadratic parameters, and errors for
    levelled film thickness data measured with the Bruker Dektak.

    Parameters
    ----------
    x_array, y_array: list
        x- and y- data arrays.
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
    file_name, out_path: string
        File name and path to save.

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
    level_regions_interests
    crop_xydata
    fit_quadratic
    calculate_filmthickness
    plot_dektak_thicknesses

    Example
    -------
    None

    """
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
        file_name=file_name)
    plot_dektak_thicknesses(
        x_array=x_array,
        y_array=y_array,
        quadratic_parameters=step_results[f'{file_name} Quadratic'],
        step_height=step_results[f'{file_name} Thickness'],
        plot_dict=plot_dict,
        out_path=out_path)
    return step_results
