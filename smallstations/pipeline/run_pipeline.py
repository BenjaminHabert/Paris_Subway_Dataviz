import logging

from smallstations.pipeline import (
    step_10_list_stations_and_lines,
    step_20_add_line_infos,
    step_30_make_plot,
)


def run():
    logging.info('Running main pipeline')

    steps_to_run = (
        step_10_list_stations_and_lines,
        step_20_add_line_infos,
        step_30_make_plot,
    )
    for step in steps_to_run:
        step.run()


    logging.info('Main pipeline completed')


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s][%(levelname)s][%(module)s] %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S',
        level=logging.DEBUG)
    run()
