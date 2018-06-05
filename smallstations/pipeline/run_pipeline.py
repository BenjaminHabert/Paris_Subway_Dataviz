import logging

from smallstations.pipeline import (
    step_10_list_stations_and_lines,
)

def run():
    logging.info('Running main pipeline')

    steps_to_run = (
        step_10_list_stations_and_lines,
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
