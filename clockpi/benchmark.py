import datetime

from clockpi.alphanum import numbers_large
from clockpi.constants import NUM_LEDS
from clockpi.constants import ON
from clockpi.graphics.utils import add_to_matrix
from clockpi.graphics.utils import MatrixGenerator
from clockpi.utils import matrix_to_command
from clockpi.utils import send_data
from clockpi.utils import wait_for_ping


def test_ping(arduino, iterations):
    total = datetime.timedelta(seconds=0)
    pings = []
    for ii in range(iterations):
        start = datetime.datetime.now()
        arduino.write('p')
        wait_for_ping(arduino)
        end = datetime.datetime.now()
        diff = end - start
        pings.append(diff)
        total += diff
    print "Ping stats:\n\tmin: {}\n\tmax: {}\n\tavg: {}".format(
        min(pings), max(pings), total/iterations)


def test_speed(arduino):
    start = datetime.datetime.now()
    arduino.write('s')
    data = ON*NUM_LEDS
    send_data(arduino, data)
    elapsed_time = datetime.datetime.now() - start
    arduino.write('rp')
    wait_for_ping(arduino)
    return elapsed_time


def benchmark(arduino):
    start = datetime.datetime.now()
    matrix = MatrixGenerator.generate_empty_matrix([255, 255, 255])
    send_data(arduino, matrix_to_command(matrix))

    matrix = MatrixGenerator.generate_empty_matrix()
    add_to_matrix(numbers_large.ZERO, matrix, 0, 0)
    add_to_matrix(numbers_large.ONE, matrix, 8, 0)
    add_to_matrix(numbers_large.TWO, matrix, 16, 0)
    add_to_matrix(numbers_large.THREE, matrix, 24, 0)
    add_to_matrix(numbers_large.FOUR, matrix, 32, 0)
    send_data(arduino, matrix_to_command(matrix))

    matrix = MatrixGenerator.generate_empty_matrix()
    add_to_matrix(numbers_large.FIVE, matrix, 0, 0)
    add_to_matrix(numbers_large.SIX, matrix, 8, 0)
    add_to_matrix(numbers_large.SEVEN, matrix, 16, 0)
    add_to_matrix(numbers_large.EIGHT, matrix, 24, 0)
    add_to_matrix(numbers_large.NINE, matrix, 32, 0)
    send_data(arduino, matrix_to_command(matrix))
    finish = datetime.datetime.now()
    elapsed_time = finish - start
    print "Benchmark time: {}".format(elapsed_time)
    print "Approx time/LED: {}".format(elapsed_time/(640*3))


def cycle_time_benchmark(arduino, num_cycles=100):
    start = datetime.datetime.now()
    for _ in range(num_cycles/len(numbers_large.ALL_NUMBERS)):
        for number in numbers_large.ALL_NUMBERS:
            matrix = MatrixGenerator.generate_empty_matrix([255, 255, 255])
            add_to_matrix(number, matrix, 0, 0)
            add_to_matrix(number, matrix, 8, 0)
            add_to_matrix(number, matrix, 16, 0)
            add_to_matrix(number, matrix, 24, 0)
            add_to_matrix(number, matrix, 32, 0)
            send_data(arduino, matrix_to_command(matrix))

    finish = datetime.datetime.now()
    elapsed_time = finish - start
    print "Time/cycle: {}".format(elapsed_time/num_cycles)
