import os
import numpy as np
import Functions.Maths as maths
import Functions.UserInput as ui
import Functions.Organisation as org
import Functions.StandardPlots as plot


def CsvIn(file_path):
    '''
    Loads Bruker Dektak csv file. Accessed through exporting data from Bruker
    software. Read through output file until "Lateral, Position" line, ignores
    all marker parameters.
    Args:
        file_path: <string> path to input file
    Returns:
        lateral: <array> lateral position array (x-array) [mm]
        profile: <array> surface profile array (y-array) [nm]
    '''
    with open(file_path) as infile:
        lines = infile.readlines()
        for index, line in enumerate(lines):
            if 'Lateral' in line:
                lateral, profile = np.genfromtxt(
                    fname=file_path,
                    delimiter=',',
                    skip_header=index + 1,
                    usecols=(0, 1),
                    unpack=True)
                lateral /= 1000  # convert to mm
                profile /= 10  # convert to nm
    return lateral, profile


def DektakPlots(dir_path,
                data_files,
                plot_files):
    '''
    Plot standard Bruker Dektak surface profile.
    Args:
        dir_path: <string> path to directory
        data_files: <array> list of filenames to plot in directory
        plot_files: <array> list of plotted files in directory
    Returns:
        None
    '''
    for file in data_files:
        if f'{file[0: -4]}.png' in plot_files:
            pass
        else:
            print(file)
            filepath = os.path.join(
                dir_path,
                file)
            filename = org.get_filename(file_path=filepath)
            lateral, profile = CsvIn(file_path=filepath)
            plot.xy_plot(
                x=lateral,
                y=profile,
                label='Profile',
                color='r',
                xlabel='Lateral Position [mm]',
                ylabel='Surface Profile [nm]',
                title=filename,
                out_path=os.path.join(
                    os.path.dirname(filepath),
                    f'{filename}.png'),
                line=True)
    print('Profiles Plotted')


def HeightPlots(dir_path,
                data_files,
                plot_files):
    '''
    Plot standard Bruker Dektak surface profile and calculate feature height.
    Calculates step height between two aspects of surface profile.
    Args:
        dir_path: <string> path to directory
        data_files: <array> list of filenames to plot in directory
        plot_files: <array> list of plotted files in directory
    Returns:
        None
    '''
    for file in data_files:
        if f'{file[0: -4]}_Height.png' in plot_files:
            pass
        else:
            filepath = os.path.join(
                dir_path,
                file)
            filename = org.get_filename(file_path=filepath)
            lateral, profile = CsvIn(file_path=filepath)
            print('Height ROI 1')
            _, yinterest1, x1, x2 = ui.GraphRegionInterest(
                x=lateral,
                y=profile,
                file_name='Height ROI 1')
            print('Height ROI 2')
            _, yinterest2, x3, x4 = ui.GraphRegionInterest(
                x=lateral,
                y=profile,
                file_name='Height ROI 2')
            mean1 = sum(yinterest1) / len(yinterest1)
            mean2 = sum(yinterest2) / len(yinterest2)
            error1 = maths.standard_error_mean(x=yinterest1)
            error2 = maths.standard_error_mean(x=yinterest2)
            height = mean2 - mean1
            error = maths.addition_error(
                delta_x=error1,
                delta_y=error2)
            textstring = f'height = ({round(height, 2)}+/-{round(error, 2)})nm'
            plot.xy_tworois_plot(
                x=lateral,
                y=profile,
                label='Surface Profile',
                color='r',
                x1=x1,
                x2=x2,
                x3=x3,
                x4=x4,
                vline_color='b',
                text_string=textstring,
                xlabel='Lateral Position [mm]',
                ylabel='Surface Profile [nm]',
                title=filename,
                out_path=os.path.join(
                    os.path.dirname(filepath),
                    f'{filename}_Height.png'),
                line=True)
    print('Heights Plotted')


def WidthsPlots(dir_path,
                data_files,
                plot_files):
    '''
    Plot standard Bruker Dektak surface profile and calculate feature width.
    Calculates step height between two aspects of surface profile.
    Args:
        dir_path: <string> path to directory
        data_files: <array> list of filenames to plot in directory
        plot_files: <array> list of plotted files in directory
    Returns:
        None
    '''
    for file in data_files:
        if f'{file[0: -4]}_Width.png' in plot_files:
            pass
        else:
            filepath = os.path.join(
                dir_path,
                file)
            filename = org.get_filename(file_path=filepath)
            lateral, profile = CsvIn(file_path=filepath)
            print('Width ROI')
            xinterest, _, x1, x2 = ui.GraphRegionInterest(
                x=lateral,
                y=profile,
                file_name='Width ROI')
            width = max(xinterest) - min(xinterest)
            pointerror = (xinterest[1] - xinterest[0]) / 2
            error = maths.addition_error(
                delta_x=pointerror,
                delta_y=pointerror)
            textstring = f'width = ({round(width, 2)}+/-{round(error, 2)})mm'
            plot.xy_roi_plot(
                x=lateral,
                y=profile,
                label='Surface Profile',
                color='r',
                x1=x1,
                x2=x2,
                vline_color='b',
                text_string=textstring,
                xlabel='Lateral Position [mm]',
                ylabel='Surface Profile [nm]',
                title=filename,
                out_path=os.path.join(
                    os.path.dirname(filepath),
                    f'{filename}_Width.png'),
                line=True)
    print('Widths Plotted')


def DimensionsPlots(dir_path,
                    data_files,
                    plot_files,
                    counter):
    '''
    Plot standard Bruker Dektak surface profile and calculate feature width
    and step height from substrate. Function calculates profile height on ROI 1
    and profile height and feature width for ROI 2.
    Args:
        dir_path: <string> path to directory
        data_files: <array> list of filenames to plot in directory
        plot_files: <array> list of plotted files in directory
    Returns:
        None
    '''
    for file in data_files:
        if f'{file[0: -4]}_Dimensions.png' in plot_files:
            pass
        else:
            filepath = os.path.join(
                dir_path,
                file)
            filename = org.get_filename(file_path=filepath)
            lateral, profile = CsvIn(file_path=filepath)
            print('Height ROI 1')
            _, yinterest1, x1, x2 = ui.GraphRegionInterest(
                x=lateral,
                y=profile,
                file_name='Height ROI 1')
            print('Height ROI 2, Width ROI')
            xinterest, yinterest2, x3, x4 = ui.GraphRegionInterest(
                x=lateral,
                y=profile,
                file_name='Height ROI 2, Width ROI')
            mean1 = sum(yinterest1) / len(yinterest1)
            mean2 = sum(yinterest2) / len(yinterest2)
            yerror1 = maths.standard_error_mean(x=yinterest1)
            yerror2 = maths.standard_error_mean(x=yinterest2)
            height = mean2 - mean1
            herror = maths.quadrature(
                x=mean1,
                y=mean2,
                z=height,
                delta_x=yerror1,
                delta_y=yerror2)
            width = max(xinterest) - min(xinterest)
            pointerror = (xinterest[1] - xinterest[0]) / 2
            werror = maths.addition_error(
                delta_x=pointerror,
                delta_y=pointerror)
            textstring = (
                f'height = ({round(height, 3)}+/-{round(herror, 3)})nm' +
                f'\nwidth = ({round(width, 3)}+/-{round(werror, 3)})mm')
            plot.xy_tworois_plot(
                x=lateral,
                y=profile,
                label='Surface Profile,',
                color='r',
                x1=x1,
                x2=x2,
                x3=x3,
                x4=x4,
                vline_color='b',
                text_string=textstring,
                xlabel='Lateral Position [mm]',
                ylabel='Surface Profile [nm]',
                title=filename,
                out_path=os.path.join(
                    os.path.dirname(filepath),
                    f'{filename}_Dimensions{counter}.png'),
                line=True)
    print('Dimensions Plotted')


if __name__ == '__main__':

    ''' Processes '''
    batch = False  # plot all unplotted data
    profile = True  # plot only surface profile
    height = True  # plot step height
    width = False  # plot feature width
    dimensions = False  # plot step height and feature width

    counter = 10

    ''' Organisation '''
    root = os.getcwd()
    dirpathsconfig = org.get_config(
        config_path=os.path.join(
            root,
            '..',
            'Dirpaths.config'))
    rootpath = os.path.join(
        dirpathsconfig['root'],
        dirpathsconfig['dektak'])

    if batch:

        ''' Find Data '''
        dirpath = org.find_path(
            default=rootpath,
            dir_path=True,
            title='Select A Directory')
        datafiles, plotfiles = org.find_files(
            dir_path=dirpath,
            file_string='.csv')

    else:

        ''' Find Data '''
        filepaths = org.find_path(
            default=rootpath,
            file_path=True,
            file_type=[('CSV', '*.csv')],
            title='Select CSV Files')
        dirpath = [os.path.dirname(file) for file in filepaths][0]
        datafiles = [f'{org.get_filename(file)}.csv' for file in filepaths]
        _, plotfiles = org.find_files(
            dir_path=dirpath,
            file_string='.csv')

    if profile:
        DektakPlots(
            dir_path=dirpath,
            data_files=datafiles,
            plot_files=plotfiles)

    if height:
        HeightPlots(
            dir_path=dirpath,
            data_files=datafiles,
            plot_files=plotfiles)

    if width:
        WidthsPlots(
            dir_path=dirpath,
            data_files=datafiles,
            plot_files=plotfiles)

    if dimensions:
        DimensionsPlots(
            dir_path=dirpath,
            data_files=datafiles,
            plot_files=plotfiles,
            counter=counter)
