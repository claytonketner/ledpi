#!/usr/env/python

import argparse

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from clockpi.main import main as clockpi_main


def main(run_forever):
    options = RGBMatrixOptions()
    options.rows = 32
    options.chain_length = 2
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat-pwm'
    # options.pwm_bits = 8
    # options.gpio_slowdown = 2
    driver = RGBMatrix(options=options)
    clockpi_main(driver, run_forever)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-forever', action='store_true')
    args = parser.parse_args()
    main(args.run_forever)
