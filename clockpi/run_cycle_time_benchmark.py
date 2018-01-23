#!/usr/bin/env python
from clockpi import benchmark
from clockpi import utils


arduino = utils.connect_to_arduino()
benchmark.cycle_time_benchmark(arduino)
