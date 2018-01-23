#!/usr/bin/env python

import time

from clockpi.graphics.graphics import display_clock
from clockpi.utils import send_matrix


def main(driver, run_forever):
    first_run = True
    while run_forever or first_run:
        first_run = False
        matrix = display_clock()
        if matrix:
            send_matrix(driver, matrix)
            # time.sleep(0.2)
    time.sleep(3)
    driver.Clear()
