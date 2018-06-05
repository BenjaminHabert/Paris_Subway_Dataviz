import logging

import matplotlib
matplotlib.use('Agg')


from matplotlib.patches import Circle, Wedge
from matplotlib import pyplot as plt

from smallstations import io


import seaborn as sns



def run():
    logging.info("Creating plot...")

    stations = io.load_dataframe('stations_and_lines_with_color.csv')
    fig = create_figure(stations)
    save_figure(fig)

    logging.info("Creating plot: completed")

def create_figure(stations):
    max_index = stations['line_index'].max()
    lims = [-max_index - 1, max_index + 1]

    grid = (
        sns.FacetGrid(
            stations, size=3, xlim=lims, ylim=lims,
            col='station', col_wrap=14
        )
        .map(_plot_background, radius=max_index)
        .map(_plot_lines, 'line_index', 'line_color')
        .set_titles("{col_name}")
    )

    return grid

def save_figure(fig):
    _save_helper(fig, 'stations_small.png', dpi=30)
    _save_helper(fig, 'stations_medium.png', dpi=50)
    _save_helper(fig, 'stations_large.png', dpi=120)
    _save_helper(fig, 'stations.pdf')


def _save_helper(fig, filename, **kwargs):
    path = io.create_abspath(filename)
    logging.info('Saving figure to: ' + path)
    fig.savefig(path, bbox_inches='tight', pad_inches=3, **kwargs)


def _plot_background(radius, **kwargs):
    ax = plt.gca()
    ax.add_patch(Circle((0, 0), radius=radius, color='#e5e7ea'))
    ax.set_aspect(1)
    ax.axis('off')

def _plot_lines(line_index, line_color, **kwargs):
    ax = plt.gca()
    for i, c in zip(line_index, line_color):
        ax.add_patch(Wedge(
            (0, 0),
            i,
            0, 360,
            width=1,
            color=c
        ))
