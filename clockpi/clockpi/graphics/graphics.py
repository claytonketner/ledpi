from clockpi.clockface_config import PLAIN_CLOCKFACE
from clockpi.clockface_config import TRAFFIC_CLOCKFACE
from clockpi.clockface_config import WEATHER_ANIMATIONS
from clockpi.graphics.utils import add_to_matrix
from clockpi.graphics.utils import config_to_matrix
from clockpi.graphics.utils import generate_empty_matrix
from clockpi.update_clock_info import ClockInfoUpdater


class LEDPi(object):
    def __init__(self, update_freq=0.0):
        self.update_freq = update_freq
        self.data = {}
        self.clock_info_updater = ClockInfoUpdater()

    def display_clock(self):
        """
        Returns the current matrix to be displayed, or None, if the display
        shouldn't be updated right now.
        """
        if not self.clock_info_updater.run(self.data, self.update_freq):
            return None
        matrix = generate_empty_matrix()
        forecast_key = self.data.get('forecast_key')
        if forecast_key:
            weather_config = WEATHER_ANIMATIONS[forecast_key]
            for conf in weather_config.itervalues():
                conf.setdefault('color', self.data['color'])
            weather_matrix = config_to_matrix(
                weather_config, self.data,
                brightness=self.data['brightness'], bit_or=False)
            add_to_matrix(weather_matrix, matrix, 0, 0, transpose=False)
        if self.data['show_traffic'] and self.data.get('traffic'):
            clockface = config_to_matrix(TRAFFIC_CLOCKFACE, self.data,
                                         color=self.data['color'])
        else:
            clockface = config_to_matrix(PLAIN_CLOCKFACE, self.data,
                                         color=self.data['color'])
        add_to_matrix(clockface, matrix, 0, 0, transpose=False,
                      bit_or=False, mask=True)
        return matrix
