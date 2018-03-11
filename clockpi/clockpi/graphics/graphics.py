from clockpi.clockface_config import PLAIN_CLOCKFACE
from clockpi.clockface_config import TRAFFIC_CLOCKFACE
from clockpi.clockface_config import WEATHER_ANIMATIONS
from clockpi.graphics.utils import add_to_matrix
from clockpi.graphics.utils import config_to_matrix
from clockpi.graphics.utils import generate_empty_matrix
from clockpi.update_clock_info import update_clock_info


def display_clock(clock_info={}, update_freq=0.2):
    """
    N.B.: Uses the fact that the default arg for clock_info can be mutated
    permanently because it's a dictionary. Kinda sketchy...?

    Returns the matrix to be displayed, or None, if the display shouldn't be
    updated.
    """
    if not update_clock_info(clock_info, update_freq):
        return None
    matrix = generate_empty_matrix()
    forecast_key = clock_info.get('forecast_key')
    if forecast_key:
        weather_config = WEATHER_ANIMATIONS[forecast_key]
        weather_matrix = config_to_matrix(weather_config, clock_info,
                                          brightness=clock_info['brightness'])
        add_to_matrix(weather_matrix, matrix, 0, 0, transpose=False)
    if clock_info['show_traffic']:
        clockface = config_to_matrix(TRAFFIC_CLOCKFACE, clock_info,
                                     color=clock_info['color'])
    else:
        clockface = config_to_matrix(PLAIN_CLOCKFACE, clock_info,
                                     color=clock_info['color'])
    add_to_matrix(clockface, matrix, 0, 0, transpose=False, bit_or=False,
                  mask=True)
    return matrix
