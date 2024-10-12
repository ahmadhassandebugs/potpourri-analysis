from os import path
import pandas as pd

import matplotlib.pyplot as plt

from utils.context import plot_dir
from utils.utils import plotme, colorlist20

plt.rc('font', family='sans-serif', serif='cm10')
plt.rc('text', usetex=True)

## CONFIG ##
SHOW_PLOT_FLAG = False

## Data ##
header = ["year", "L0", "L1", "L2", "L3", "L4/5"]
data = [
    [2025, 34.2, 39.7, 25.7, 0, 0],
    [2030, 17.98, 33.97, 35.66, 9.89, 2.5],
    [2035, 5.2, 34.1, 35.9, 17.7, 7.1],
    [2040, 3.2, 16, 32.5, 33.9, 14.4]
]
df = pd.DataFrame(data, columns=header)
l2plus = [25.7, 48.05, 60.7, 80.8]
tesla_nn_power = 36  # TOPS
l2plus = [x * 52e6 for x in l2plus]
l2plus = [x*tesla_nn_power for x in l2plus]
l2plus = [x/1e9 for x in l2plus]


#### Plot graph
if True:
    plot_id = '03a'
    plot_name = 'avs-level-growth-bars'
    plt.close('all')
    fig, ax = plt.subplots(figsize=(3, 1.45))
    axr = ax.twinx()
    fig.tight_layout()

    color_scheme = colorlist20[1::2]
    width = 0.4
    pad = 0.0

    df.plot(kind='bar', stacked=True, x='year', ax=ax, color=color_scheme, width=width)
    x = range(len(df['year']))
    x = [i + (width/1.25) + pad for i in x]
    axr.bar(x, l2plus, width=0.2, color="indianred", alpha=1.0, zorder=2)

    ax.set_ylabel(r"\textbf{Percentage of}""\n"r"\textbf{cars (\%)}", fontsize=11)
    axr.set_ylabel(r"\textbf{L2+ cars' power}""\n"r"\textbf{(Billion TOPS)}", fontsize=11, color='indianred')
    ax.yaxis.set_label_coords(-0.17, 0.4)
    ax.set_xlabel('')
    ax.set_xlim(-0.3, 3.5)
    ax.set_yticks(range(0, 101, 25))
    axr.set_yticks(range(0, 130, 40))
    x = range(len(df['year']))
    x = [i + 0.2 for i in x]
    ax.set_xticks(x)
    ax.set_xticklabels(df['year'], rotation=0)
    ax.yaxis.grid(color='lightgray', linestyle='dashed', zorder=1, lw=0.75)
    ax.tick_params(axis='both', which='major', labelsize=11)
    axr.tick_params(axis='both', which='major', labelsize=11)
    for tl in axr.get_yticklabels():
        tl.set_color('indianred')
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.legend(loc='upper center',
              ncol=5, bbox_to_anchor=(0.45, 1.33), facecolor='#dddddd', columnspacing=0.2,
              handlelength=1.75, framealpha=.5, fontsize=12, borderpad=0.05, labelspacing=.05, handletextpad=0.1,
              frameon=False)

    # always use this function to save the figures
    plotme(plt, plot_id, plot_name, plot_dir, show_flag=SHOW_PLOT_FLAG, ignore_eps=True, pad_inches=0.07)

print('Complete./')
