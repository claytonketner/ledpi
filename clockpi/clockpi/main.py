#!/usr/bin/env python

import argparse
import time

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from clockpi.graphics.graphics import display_clock
from clockpi.utils import send_matrix


def main(driver, run_once):
    first_run = True
    while not run_once or first_run:
        first_run = False
        matrix = display_clock()
        if matrix:
            send_matrix(driver, matrix)
    time.sleep(3)
    driver.Clear()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-once', action='store_true')
    args = parser.parse_args()

    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 32
    options.chain_length = 2
    options.parallel = 1
    options.multiplexing = 0
    options.hardware_mapping = 'adafruit-hat-pwm'
    driver = RGBMatrix(options=options)

    main(driver, args.run_once)
