import logging

import matplotlib
matplotlib.use('Agg')  # still annoying that I have to do this.

from matplotlib.patches import Circle, Wedge
from matplotlib.font_manager import FontProperties
from matplotlib import pyplot as plt
import seaborn as sns

from smallstations import io


N_COLS = 14


def run():
    logging.info("Creating plot...")

    stations = io.load_dataframe('stations_and_lines_with_color.csv')
    fig = create_figure(stations)
    fig = add_infos(fig, stations)
    save_figure(fig)

    logging.info("Creating plot: completed")


def create_figure(stations):
    max_index = stations['line_index'].max()

    grid = (
        sns.FacetGrid(
            stations, size=3,
            col='station', col_wrap=N_COLS
        )
        .map(_plot_background, radius=max_index)
        .map(_plot_lines, 'line_index', 'line_color')
        .set_titles("{col_name}")
    )

    return grid.fig


def add_infos(fig, stations):

    x_left, y_bottom, delta_x, delta_y, w, h = _compute_positions(fig)
    _add_legend_data(fig, stations, x_left, y_bottom, delta_x, delta_y, w, h)
    _add_legend_text(fig, x_left, y_bottom, delta_x, delta_y)
    _add_title_and_signature(fig, x_left, y_bottom, delta_x, delta_y)

    return fig


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
    lims = [-radius - 1, radius + 1]
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.add_patch(Circle((0, 0), radius=radius, color='#e5e7ea'))
    ax.set_aspect(1)
    ax.axis('off')


def _plot_lines(line_index, line_color, line_names=None, **kwargs):
    ax = plt.gca()
    if line_names is None:
        line_names = [None] * len(line_index)
    for radius, color, name in zip(line_index, line_color, line_names):
        ax.add_patch(Wedge(
            (0, 0),
            radius,
            0 if name is None else 90, 360,
            width=1,
            color=color
        ))
        if name is not None:
            ax.text(1, radius - 0.5, name,
                    fontsize=8,
                    verticalalignment='center', horizontalalignment='left')


###############################################################################
# Extra infos


def _compute_positions(fig):
    top_left = fig.axes[0]
    diagonal = fig.axes[N_COLS + 1]
    bottom = fig.axes[-1]

    x0, y0, w, h = top_left.get_position().bounds
    x1, y1, _, _ = diagonal.get_position().bounds
    _, y_bottom, _, _ = bottom.get_position().bounds

    x_left = x0
    delta_y = y1 - y0
    delta_x = x1 - x0

    return x_left, y_bottom, delta_x, delta_y, w, h


def _add_legend_data(fig, stations, x_left, y_bottom, delta_x, delta_y, w, h):
    legend_groups = [
        [   # greens
            'Ligne 3',
            'Ligne 6',
            'Ligne 7bis',
            'Ligne 9',
            'Ligne 12'
        ],
        [   # blues
            'Ligne 2',
            'Ligne 3bis',
            'Ligne 11',
            'Ligne 13',
        ],
        [   # pinks
            'Ligne 4',
            'Ligne 7',
            'Ligne 8',
            'Ligne 14',
        ],
        [   # reds
            'Ligne 1',
            'Ligne 5',
            'Ligne 10'
        ]
    ]
    ax_positions = [
        (x_left + i * delta_x, y_bottom + delta_y, w, h)
        for i in range(len(legend_groups))
    ]


    lines = stations.drop_duplicates(subset='line').sort_values(by='line_index')
    max_index = stations['line_index'].max()
    # slims = [-max_index - 1, max_index + 1]

    for position, line_sample in zip(ax_positions, legend_groups):
        ax = fig.add_axes(position)
        _plot_background(max_index)

        sample = lines.loc[lines['line'].isin(line_sample)]
        _plot_lines(sample['line_index'], sample['line_color'],
                    line_names=sample['line'])


def _add_legend_text(fig, x_left, y_bottom, delta_x, delta_y):
    infos = '\n'.join([
        '',
        'Each dot is a subway station ;',
        'stations are ordered alphabetically.',
        '',
        'Each circle indicates a subway line stopping at this station.',
        '',
        'Source:',
        'https://fr.wikipedia.org/wiki/Liste_des_stations_du_métro_de_Paris'
    ])
    fig.text(x_left + 4.2 * delta_x, y_bottom + 0.5 * delta_y, infos,
             fontproperties=FontProperties(family='serif', size=18),
             horizontalalignment='left', verticalalignment='center')


def _add_title_and_signature(fig, x_left, y_bottom, delta_x, delta_y):
    # title
    fig.suptitle('Paris Subway Stations and Lines', y=1 - delta_y,
                     fontproperties=FontProperties(family='serif', size=60),
                     horizontalalignment='center', verticalalignment='bottom')

    # signature
    font = FontProperties(family='serif', size=50)
    fig.text(x_left + (N_COLS - 0.2) * delta_x, y_bottom + 0.8 * delta_y,
             "rand-on.com",
             fontproperties=FontProperties(family='serif', size=50),
             horizontalalignment='right', verticalalignment='bottom')


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s][%(levelname)s][%(module)s] %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S',
        level=logging.DEBUG)
    run()
