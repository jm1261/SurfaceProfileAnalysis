import matplotlib.pyplot as plt


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


def plotafm(x, y, label,
            xlabel, ylabel, title, out_path,
            line=False):
    fig, ax = plt.subplots(
        1,
        figsize=[round(7.5 * 0.393701, 2), round(9 * 0.393701, 2)],
        dpi=600)
    if line:
        ax.plot(
            x, y,
            'b',
            lw=2,
            label=label)
    else:
        ax.plot(
            x, y,
            'bx',
            markersize=4,
            label=label)
    ax.grid(True)
    #ax.legend(
    #    frameon=True,
    #    loc=0,
    #    prop={'size': 10})
    ax.set_xlabel(
        xlabel,
        fontsize=15,
        fontweight='bold',
        color='black')
    ax.set_ylabel(
        ylabel,
        fontsize=15,
        fontweight='bold',
        color='black')
    #ax.set_title(
    #    title,
    #    fontsize=18,
    #    fontweight='bold',
    #    color='black')
    ax.tick_params(
        axis='both',
        colors='black',
        labelsize=10)
    plt.savefig(out_path, bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)


def xy_tworois_plot(x, y, label, text_string,
                    x1, x2, x3, x4,
                    xlabel, ylabel, title, out_path,
                    line=False):
    '''
    Plot two regions of interest for (x, y) data on graph. Display start and
    end of regions of interest on x-axis.
    Args:
        x: <array> x-data array
        y: <array> y-data array
        x1: <float> initial x-coordinate for region of interest 1
        x2: <float> final x-coordinate for region of interest 1
        x3: <float> initial x-coordinate for region of interest 2
        x4: <float> final x-coordinate for region of interest 2
        text_string: <string> text string for display box
        xlabel: <string> x-axis label
        ylabel: <string> y-axis label
        label: <string> data label
        title: <string> plot title
        out_path: <string> save path
        line: <bool> if true, plots line, else plots markers
        show: <bool> if true, plot shows, always saves
    Returns:
        None
    '''
    fig, ax = plt.subplots(
        1,
        figsize=[round(7.5 * 0.393701, 2), round(9 * 0.393701, 2)],
        dpi=600)
    if line:
        ax.plot(
            x, y,
            'b',
            lw=2,
            label=label)
    else:
        ax.plot(
            x, y,
            'bx',
            markersize=4,
            label=label)
    ax.grid(True)
    #ax.legend(
    #    frameon=True,
    #    loc=0,
    #    prop={'size': 10})
    ax.axvline(
        x=x1,
        color='g',
        linestyle='--')
    ax.axvline(
        x=x2,
        color='g',
        linestyle='--')
    ax.axvline(
        x=x3,
        color='g',
        linestyle='--')
    ax.axvline(
        x=x4,
        color='g',
        linestyle='--')
    ax.set_xlabel(
        xlabel,
        fontsize=15,
        fontweight='bold',
        color='black')
    ax.set_ylabel(
        ylabel,
        fontsize=15,
        fontweight='bold',
        color='black')
    #ax.set_title(
    #    title,
    #    fontsize=18,
    #    fontweight='bold',
    #    color='black')
    ax.tick_params(
        axis='both',
        colors='black',
        labelsize=10)
    props = dict(
        boxstyle='round',
        facecolor='wheat',
        alpha=0.5)
    ax.text(
        0.05,
        0.05,
        text_string,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment='top',
        bbox=props)
    plt.savefig(out_path, bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)


def xy_roi_plot(x_array : list,
                y_array : list,
                x1 : float,
                x2 : float,
                text_string : str,
                plot_dict : dict,
                out_path : str) -> None:
    """
    Plot region of interest for (x, y) data on graph.

    Display start and end of region of interest for x-data.

    Parameters
    ----------
    x_array, y_array: list
        x- and y-data arrays.
    x1, x2: float
        x data values for regions of interest.
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
        Path so save.

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
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=plot_dict["width"]),
            cm_to_inches(cm=plot_dict["height"])],
        dpi=plot_dict["dpi"])
    ax.plot(
        x_array,
        y_array,
        'b',
        lw=2,
        label='Data')
    if plot_dict["grid"] == "True":
        grid = True
    else:
        grid = False
    ax.grid(
        visible=grid,
        alpha=0.5)
    ax.axvline(
        x=x1,
        color='r',
        linestyle='--',
        lw=2)
    ax.axvline(
        x=x2,
        color='r',
        linestyle='--',
        lw=2)
    props = dict(
        boxstyle='round',
        facecolor='wheat',
        alpha=0.5)
    ax.text(
        0.05,
        0.05,
        text_string,
        transform=ax.transAxes,
        fontsize=14,
        verticalalignment='top',
        bbox=props)
    ax.legend(
        loc=plot_dict["legend_loc"],
        ncol=plot_dict["legend_col"],
        prop={'size': plot_dict["legend_size"]})
    ax.set_xlabel(
        'Lateral (mm)',
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold',
        color='black')
    ax.set_ylabel(
        'Profile (nm)',
        fontsize=plot_dict["axis_fontsize"],
        fontweight='bold',
        color='black')
    ax.tick_params(
        axis='both',
        colors='black',
        labelsize=plot_dict["label_size"])
    fig.tight_layout()
    plt.savefig(out_path)
    fig.clf()
    plt.cla()
    plt.close(fig)
