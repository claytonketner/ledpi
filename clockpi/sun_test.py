from datetime import datetime
from datetime import timedelta

from clockpi.constants import ARRAY_HEIGHT
from clockpi.graphics.graphics import display_clock
from clockpi.graphics.utils import add_to_matrix
from clockpi.graphics.utils import generate_sun_matrix
from clockpi.utils import send_matrix


def sun_test(arduino):
    sun_start_diameter = 10
    sun_growth = 200
    total_duration = 60
    start = datetime.now()
    end = start + timedelta(seconds=total_duration)
    total_travel = ARRAY_HEIGHT + 3
    while datetime.now() < end:
        clock_matrix = display_clock(update_freq=0.3)
        if clock_matrix:
            elapsed_seconds = (datetime.now() - start).total_seconds()
            percent_done = elapsed_seconds / total_duration
            sun_current_diameter = int(sun_start_diameter / 2 +
                                       percent_done * sun_growth)
            sun_y = (sun_current_diameter / 2 + ARRAY_HEIGHT -
                     (total_travel * percent_done))
            sun_matrix = generate_sun_matrix(sun_y, sun_current_diameter / 2)
            add_to_matrix(sun_matrix, clock_matrix, 0, 0, bit_xor=True,
                          transpose=False)
            send_matrix(arduino, clock_matrix)
