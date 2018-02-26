import time

from datetime import datetime

from clockpi.alphanum import glyphs
from clockpi.constants import DAILY_R_MIN
from clockpi.constants import DAILY_G_MIN
from clockpi.constants import DAILY_B_MIN
from clockpi.constants import DAILY_R_MAX
from clockpi.constants import DAILY_G_MAX
from clockpi.constants import DAILY_B_MAX
from clockpi.constants import SUN_ANIMATION_DURATION
from clockpi.external import get_traffic
from clockpi.external import get_weather
from clockpi.graphics.utils import calc_color_cos
from clockpi.secret import DIRECTIONS_END_HOUR
from clockpi.secret import DIRECTIONS_START_HOUR


def update_time(clock_info, now):
    second = now.second
    minute = now.minute
    hour_24 = now.hour
    hour_12 = hour_24 % 12
    if hour_24 == 0 or hour_24 == 12:
        hour_12 = 12
    clock_info['hour_digits'] = map(int, [hour_12 / 10, hour_12 % 10])
    clock_info['minute_digits'] = map(int, [minute / 10, minute % 10])
    clock_info['second_digits'] = map(int, [second / 10, second % 10])
    clock_info['hour'] = hour_24
    clock_info['minute'] = minute
    clock_info['second'] = second
    if hour_12 < 10:
        clock_info['hour_digits'][0] = 'BLANK'


def update_color(clock_info, now):
    day_elapsed_mins = now.hour * 60 + now.minute
    red = calc_color_cos(day_elapsed_mins, 6*60, 24*60, DAILY_R_MIN,
                         DAILY_R_MAX)
    green = calc_color_cos(day_elapsed_mins, 6*60, 24*60, DAILY_G_MIN,
                           DAILY_G_MAX)
    blue = calc_color_cos(day_elapsed_mins, 6*60, 24*60, DAILY_B_MIN,
                          DAILY_B_MAX)
    clock_info['color'] = (red, green, blue)


def update_weather(clock_info, now):
    clock_info['weather_update_time'], clock_info['weather'] = get_weather(
        clock_info.get('weather_update_time'), clock_info.get('weather', {}))
    if clock_info.get('weather'):
        # Temp out of range
        if (clock_info['weather']['current_temp'] > 99 or
                clock_info['weather']['current_temp'] < 0):
            clock_info['temp_digits'] = ['SKULL']
        else:
            clock_info['temp_digits'] = map(
                int, [clock_info['weather']['current_temp'] / 10 % 10,
                      clock_info['weather']['current_temp'] % 10])
        clock_info['sun_is_up'] = (clock_info['weather']['sunrise'] < now and
                                   clock_info['weather']['sunset'] > now)
        sunrise_anim_pct = (
            1 - ((clock_info['weather']['sunrise'] - now).total_seconds() /
                 SUN_ANIMATION_DURATION))
        clock_info['sunrise_anim_pct'] = sunrise_anim_pct
        clock_info['show_sunrise'] = (sunrise_anim_pct > 0 and
                                      sunrise_anim_pct < 1)
        sunset_anim_pct = (
            1 - ((clock_info['weather']['sunset'] - now).total_seconds() /
                 SUN_ANIMATION_DURATION))
        clock_info['sunset_anim_pct'] = sunset_anim_pct
        clock_info['show_sunset'] = (sunset_anim_pct > 0 and
                                     sunset_anim_pct < 1)
        clock_info['sunshine_anim'] = (int(time.time()) %
                                       len(glyphs.SHINING_SUN))
        # TODO: use sunset/sunrise and clock_info['weather']['state']
        weather_state = clock_info['weather']['state']
        if clock_info['sun_is_up'] and weather_state in ('sunny', 'clear'):
            pass  # TODO
    else:
        clock_info['temp_digits'] = ['E', 'R']
        # Default to sundown because the bright clockface is annoying at night
        clock_info['sun_is_up'] = False
        clock_info['show_sunrise'] = False
        clock_info['show_sunset'] = False


def update_traffic(clock_info, now):
    # Only show traffic around the times I may be going to work
    clock_info['show_traffic'] = (now.hour >= DIRECTIONS_START_HOUR and
                                  now.hour < DIRECTIONS_END_HOUR and
                                  now.isoweekday() <= 5)
    if clock_info['show_traffic']:
        clock_info['traffic_update_time'], clock_info['traffic'] = get_traffic(
            clock_info.get('traffic_update_time'),
            clock_info.get('traffic', {}))
        if clock_info.get('traffic'):
            clock_info['traffic_delta_digits'] = map(
                int, [clock_info['traffic']['traffic_delta'] / 10 % 10,
                      clock_info['traffic']['traffic_delta'] % 10])
            clock_info['travel_time_digits'] = map(
                int, [clock_info['traffic']['travel_time'] / 10 % 10,
                      clock_info['traffic']['travel_time'] % 10])
    clock_info['show_traffic'] = (clock_info['show_traffic'] and
                                  clock_info.get('traffic'))


def update_clock_info(clock_info, update_freq):
    now = datetime.now()
    last_update = clock_info.get('last_update_time')
    if last_update:
        update_time_delta = now - last_update
        if update_time_delta.total_seconds() < update_freq:
            return False
    clock_info['last_update_time'] = now
    update_time(clock_info, now)
    update_color(clock_info, now)
    update_weather(clock_info, now)
    update_traffic(clock_info, now)
    return True
