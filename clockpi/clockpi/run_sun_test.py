#!/usr/bin/env python
from clockpi import sun_test
from clockpi import utils


arduino = utils.connect_to_arduino()
sun_test.sun_test(arduino)
