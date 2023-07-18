import matplotlib.pyplot as plt


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
