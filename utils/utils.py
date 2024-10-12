import os
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
import numpy as np

import pandas as pd
import seaborn as sns

# get colors
cmap10 = plt.cm.tab10
colorlist10 = [cmap10(i) for i in range(cmap10.N)]

cmap20 = plt.cm.tab20
colorlist20 = [cmap20(i) for i in range(cmap20.N)]

cmap20c = plt.cm.tab20c
colorlist20c = [cmap20c(i) for i in range(cmap20c.N)]

pastel1 = plt.cm.Pastel1
pastel1list = [pastel1(i) for i in range(pastel1.N)]

pastel2 = plt.cm.Pastel2
pastel2list = [pastel2(i) for i in range(pastel2.N)]

paired = plt.cm.Paired
pairedlist = [paired(i) for i in range(paired.N)]

set210 = plt.cm.Set1
colorlistset2 = [set210(i) for i in range(set210.N)]

# hatches list
hatches = ['//', '\\\\', '||', '--', '++', 'xx', 'oo', 'OO', '..', '**']

# hex list
HEX_COLOR_PALETTE = ['#4078c0', '#6cc644', '#bd2c00', '#c9510c', '#6e5494', '#ffff00', '#87005f']
HAPPY_COLORS_PALETTE = ["#01BEFE", "#FFDD00", "#FF7D00", "#FF006D", "#ADFF02", "#8F00FF"]


def remove_nan(arr):
    return arr[~np.isnan(arr)]


def remove_nan_object(arr):
    return arr[~pd.isnull(arr)]


def get_cdf(arr, is_object=False):
    if is_object:
        arr = remove_nan_object(arr)
    else:
        arr = remove_nan(arr)
    arr_x = np.sort(arr)
    arr_y = 1. * np.arange(len(arr)) / (len(arr) - 1)
    return arr_x, arr_y


def remove_outliers(arr, max_deviations=3):
    mean = np.mean(arr)
    standard_deviation = np.std(arr)
    distance_from_mean = abs(arr - mean)
    not_outlier = distance_from_mean < max_deviations * standard_deviation
    no_outliers = arr[not_outlier]
    return no_outliers


def get_std(arr, max_deviations=3):
    return np.std(remove_outliers(arr, max_deviations))


def show_confusion_matrix(confusion_matrix_):
    hmap = sns.heatmap(confusion_matrix_, annot=True, fmt="d", cmap="Blues")
    hmap.yaxis.set_ticklabels(hmap.yaxis.get_ticklabels(), rotation=0, ha='right')
    hmap.xaxis.set_ticklabels(hmap.xaxis.get_ticklabels(), rotation=30, ha='right')
    plt.ylabel('True best band')
    plt.xlabel('Predicted best band')
    plt.show()


def make_error_boxes(ax, xdata, ydata, xerror, yerror, facecolor='r',
                     edgecolor='none', alpha=0.4):
    # Loop over data points; create box from errors at each point
    errorboxes = [Rectangle((x - xe, y - ye), xe * 2, ye * 2)
                  for x, y, xe, ye in zip(xdata, ydata, xerror, yerror)]

    # Create patch collection with specified colour/alpha
    pc = PatchCollection(errorboxes, facecolor=facecolor, alpha=alpha,
                         edgecolor='none')

    # Add collection to axes
    ax.add_collection(pc)

    # Plot errorbars
    artists = ax.errorbar(xdata, ydata, xerr=xerror, yerr=yerror,
                          fmt='s', ecolor=edgecolor, elinewidth=2.0, capsize=4.0, capthick=2.0)

    return artists


def draw_brace(ax, xspan, yy, text, fontsize=14):
    """Draws an annotated brace on the axes."""
    xmin, xmax = xspan
    xspan = xmax - xmin
    ax_xmin, ax_xmax = ax.get_xlim()
    xax_span = ax_xmax - ax_xmin

    ymin, ymax = ax.get_ylim()
    yspan = ymax - ymin
    resolution = int(xspan / xax_span * 100) * 2 + 1  # guaranteed uneven
    beta = 300. / xax_span  # the higher this is, the smaller the radius

    x = np.linspace(xmin, xmax, resolution)
    x_half = x[:int(resolution / 2) + 1]
    y_half_brace = (1 / (1. + np.exp(-beta * (x_half - x_half[0])))
                    + 1 / (1. + np.exp(-beta * (x_half - x_half[-1]))))
    y = np.concatenate((y_half_brace, y_half_brace[-2::-1]))
    y = yy + (.1 * y - .01) * yspan  # adjust vertical position

    ax.autoscale(False)
    ax.plot(x, y, color='black', lw=1.5, clip_on=False)

    ax.text((xmax + xmin) / 2., yy + .15 * yspan, text, ha='center', va='bottom', fontsize=fontsize, clip_on=False)

def plotme(plt_, plot_id, plot_name, plot_path='plots', show_flag=True, ignore_eps=True, pad_inches=0):
    if show_flag:
        print('Showing Plot {}-{}'.format(plot_id, plot_name))
        plt_.show(bbox_inches='tight')
    else:
        ax = plt_.gca()
        os.makedirs(os.path.join(plot_path, 'png'), exist_ok=True)
        os.makedirs(os.path.join(plot_path, 'pdf'), exist_ok=True)

        plt_.savefig(os.path.join(plot_path, 'png', f'{plot_id}-{plot_name}.png'), format='png', dpi=300,
                     bbox_inches='tight', pad_inches=pad_inches)
        plt_.savefig(os.path.join(plot_path, 'pdf', f'{plot_id}-{plot_name}.pdf'), format='pdf', dpi=300,
                     bbox_inches='tight', pad_inches=pad_inches)
        if not ignore_eps:
            # Save it with rasterized points
            ax.set_rasterization_zorder(1)
            os.makedirs(os.path.join(plot_path, 'eps'), exist_ok=True)
            plt_.savefig(os.path.join(plot_path, 'eps', f'{plot_id}-{plot_name}.eps'), dpi=300, rasterized=True,
                         bbox_inches='tight', pad_inches=0)
        print('Saved Plot {}-{}'.format(plot_id, plot_name))
