#!/usr/bin/env python
from clockpi import benchmark
from clockpi import utils


arduino = utils.connect_to_arduino()
benchmark.benchmark(arduino)
