import os
from os import path
import pandas as pd
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.proj3d import proj_transform
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.text import Annotation
from matplotlib import animation

from utils.context import data_processed_dir, plot_dir
from utils.utils import colorlist10
from utils.config import short_names_dict

plt.rc('font', family='sans-serif', serif='cm10')
plt.rc('text', usetex=True)
random.seed(42)

############### Config ####################
SHOW_PLOT_FLAG = False
DATA_FOLDER = path.join(data_processed_dir, "batting-stats")
os.makedirs(plot_dir, exist_ok=True)

## read the data
df = pd.read_csv(path.join(DATA_FOLDER, "combined.csv"))
df["short_name"] = df["player"].map(short_names_dict)


class Annotation3D(Annotation):

    def __init__(self, text, xyz, *args, **kwargs):
        super().__init__(text, xy=(0, 0), *args, **kwargs)
        self._xyz = xyz

    def draw(self, renderer):
        x2, y2, z2 = proj_transform(*self._xyz, self.axes.M)
        self.xy = (x2, y2)
        super().draw(renderer)


def _annotate3D(ax_, text, xyz, *args, **kwargs):
    """Add annotation `text` to an `Axes3d` instance."""

    annotation = Annotation3D(text, xyz, *args, **kwargs)
    ax_.add_artist(annotation)


setattr(Axes3D, 'annotate3D', _annotate3D)

#### Plot graph
plot_id = "01a"
plot_name = "batting_stats_comparison"
plt.close("all")
fig = plt.figure(figsize=(6, 5))
ax = fig.add_subplot(projection="3d")
fig.tight_layout()

colors = [colorlist10[i % len(colorlist10)] for i in range(df.shape[0])]


def init():

    ax.scatter(df["average_test"], df["average_odi"], df["average_t20"],
               c=colors, s=df["average_test"] + df["average_odi"] + df["average_t20"])
    for idx, row in df.iterrows():
        ax.text(row["average_test"] + 1.5, row["average_odi"] + 1.5, row["average_t20"] + 1.5,
                r"\textbf{"f"{row['short_name']}"r"}", size=8, zorder=2, c=colors[idx])

    ax.set_xlabel(r"\textbf{Test Average} $\rightarrow$", fontsize=16)
    ax.set_ylabel(r"\textbf{ODI Average} $\rightarrow$", fontsize=16)
    ax.set_zlabel(r"\textbf{T20 Average} $\rightarrow$", fontsize=16)
    ax.set_xlim(20, 70)
    ax.set_ylim(20, 70)
    ax.set_zlim(20, 70)

    ## annotate a 3D arrow to show direction of best performance
    # ax.annotate3D("better", (60, 60, 60),
    #               xytext=(-50, -25),
    #               textcoords='offset points',
    #               bbox=dict(boxstyle="round", fc="lightyellow"),
    #               arrowprops=dict(arrowstyle="-|>", ec='black', fc='white', lw=5))

    ## draw a cube to indicate best performing players
    # prepare some coordinates
    # x, y, z = np.indices((70, 70, 70))
    # cube = (x > 50) & (y > 50) & (z > 50)
    # cube_color = np.empty(cube.shape, dtype=object)
    # cube_color[cube] = 'lightgreen'
    # ax.voxels(cube, facecolors=cube_color)

    ax.view_init(elev=30, azim=270)
    return fig,


def animate(i):
    if i % 10 == 0:
        print(f"frame={i}")
    ax.view_init(elev=30, azim=270 + i)
    return fig,


# Animate
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=90, interval=100, blit=True)
# Save
anim.save(path.join(plot_dir, f"{plot_id}-{plot_name}_animation.gif"), fps=30)

print('Complete./')
