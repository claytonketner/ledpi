#!/usr/bin/env python
from clockpi import font_test
from clockpi import utils


arduino = utils.connect_to_arduino()
font_test.marquee_test(arduino, padding=1)
font_test.font_test(arduino, padding=1)
