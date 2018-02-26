import math
import time

from datetime import datetime
from types import ModuleType

from clockpi.alphanum import glyphs
from clockpi.constants import ARRAY_HEIGHT
from clockpi.constants import ARRAY_WIDTH
from clockpi.constants import DAILY_R_MIN
from clockpi.constants import DAILY_G_MIN
from clockpi.constants import DAILY_B_MIN
from clockpi.constants import DAILY_R_MAX
from clockpi.constants import DAILY_G_MAX
from clockpi.constants import DAILY_B_MAX
from clockpi.constants import SUN_ANIMATION_DURATION
from clockpi.external import get_traffic
from clockpi.external import get_weather
from clockpi.secret import DIRECTIONS_END_HOUR
from clockpi.secret import DIRECTIONS_START_HOUR


def generate_empty_matrix(fill_with=[0, 0, 0]):
    """Generates a matrix of zeros that can be referenced like:
        my_matrix[x_coordinate][y_coordinate]
    """
    empty_matrix = []
    for _ in xrange(ARRAY_WIDTH):
        empty_matrix.append([fill_with] * ARRAY_HEIGHT)
    return empty_matrix


def add_to_matrix(partial_matrix, matrix, x, y, color=None, transpose=True,
                  bit_or=True, bit_and=False, bit_xor=False):
    """
    Adds `partial_matrix` to `matrix` at `x`, `y`. If `color` is specified,
    `partial_matrix` will be copied using that color - otherwise, the color
    in `partial_matrix` will just be copied over.
    """
    if color:
        assert len(color) == 3
    if transpose:
        partial_matrix_x_len = len(partial_matrix[0])
        partial_matrix_y_len = len(partial_matrix)
    else:
        partial_matrix_x_len = len(partial_matrix)
        partial_matrix_y_len = len(partial_matrix[0])
    for xx in range(partial_matrix_x_len):
        for yy in range(partial_matrix_y_len):
            is_inside = (len(matrix) > (x+xx) and (x+xx) >= 0 and
                         len(matrix[0]) > (y+yy) and (y+yy) >= 0)
            if not is_inside:
                continue
            matrix_val = matrix[x+xx][y+yy]
            if transpose:
                pm_val = partial_matrix[yy][xx]
            else:
                pm_val = partial_matrix[xx][yy]
            # If the partial matrix doesn't contain colors, substitute
            # in `color` or the matrix color
            if type(pm_val) not in (tuple, list):
                if pm_val:
                    if any(matrix_val):
                        substitute_color = matrix_val
                    else:
                        substitute_color = [255, 255, 255]
                    pm_val = color or substitute_color
                else:
                    # pm_val is 0
                    pm_val = [0, 0, 0]
            if bit_and:
                if any(matrix_val) and any(pm_val):
                    # Take the average
                    final_val = [sum(z)/2 for z in zip(matrix_val, pm_val)]
                else:
                    final_val = [0, 0, 0]
            elif bit_xor:
                if any(matrix_val) and any(pm_val):
                    final_val = [0, 0, 0]
                else:
                    # One or the other or both are [0, 0, 0]
                    final_val = [sum(z) for z in zip(matrix_val, pm_val)]
            elif bit_or:
                # Use the greater of each rgb value
                final_val = [max(z) for z in zip(matrix_val, pm_val)]
            else:
                # Just overwrite the matrix with the partial matrix
                if any(pm_val):
                    final_val = pm_val
                else:
                    final_val = matrix_val
            matrix[x+xx][y+yy] = final_val


def add_items_to_matrix(items, matrix, origin_x, origin_y, spacing, color,
                        **kwargs):
    """Adds a left-aligned 'sentence', which consists of `items`, which are
    separated by `spacing`, which can be an integer, or a list containing
    spacing distances between each item in `items`
    """
    x = origin_x
    for ii in range(len(items)):
        item = items[ii]
        if ii > 0:
            space = spacing
            if hasattr(spacing, '__iter__'):
                space = spacing[ii-1]
            x += space + len(items[ii-1][0])
        add_to_matrix(item, matrix, x, origin_y, color, **kwargs)


def calc_color_cos(current_time, start, end, min_val, max_val):
    """
    Calculates an upside down cosine that is offset and has some period, but
    does not repeat. Instead of repeating, it just flatlines.
    |             ###
    |            #   #
    |           #     #
    |###########       ########
    -----------------------
               ^-------^ period
               ^ start
                       ^ end
                   ^ max_val
     ----------^       ^------ min_val
    """
    if current_time <= start or current_time >= end:
        return min_val
    period = end - start
    offset_time = current_time - start
    return int((math.cos(float(offset_time) / period * 2 * math.pi) * -1 + 1) *
               (max_val - min_val)/2 + min_val)


def update_clock_info(clock_info, update_freq):
    now = datetime.now()
    second = now.second
    last_update = clock_info.get('last_update_time')
    if last_update:
        update_time_delta = now - last_update
        if update_time_delta.total_seconds() < update_freq:
            return False
    clock_info['last_update_time'] = now
    # Time
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
    # Color
    day_elapsed_mins = hour_24 * 60 + minute
    red = calc_color_cos(day_elapsed_mins, 6*60, 24*60, DAILY_R_MIN,
                         DAILY_R_MAX)
    green = calc_color_cos(day_elapsed_mins, 6*60, 24*60, DAILY_G_MIN,
                           DAILY_G_MAX)
    blue = calc_color_cos(day_elapsed_mins, 6*60, 24*60, DAILY_B_MIN,
                          DAILY_B_MAX)
    clock_info['color'] = (red, green, blue)
    # Weather
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
    else:
        clock_info['temp_digits'] = ['E', 'R']
        # Default to sundown because the bright clockface is annoying at night
        clock_info['sun_is_up'] = False
        clock_info['show_sunrise'] = False
        clock_info['show_sunset'] = False
    # Traffic
    # Only show traffic around the times I may be going to work
    clock_info['show_traffic'] = (hour_24 >= DIRECTIONS_START_HOUR and
                                  hour_24 < DIRECTIONS_END_HOUR and
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
    # TODO: use sunset/sunrise and clock_info['weather']['state']
    clock_info['sunshine_anim'] = int(time.time()) % len(glyphs.SHINING_SUN)
    # Special cases
    clock_info['separator'] = ['SEPARATOR']
    return True


def data_to_alphanums(data_list, alphanum_source):
    """
    Converts a list of numbers or variable names to a list of alphanum arrays
    You can do different combinations of parameters (this is probably bad
    practice). The items in data_list are evaluated on a per-item basis, so
    data_list can contain both ints and strings. Not all combinations work.
    Examples:
        - One of the items in data_list is an int
        - alphanum_source is a list of alphanums
        The alphanum will be looked up by using the int from data_list as the
        index for alphanum_source

        - One of the items in data_list is an int
        - alphanum_source is a module
        The alphanum will be looked up by accessing the ALL_NUMBERS list in
        the alphanum_source module

        - One of the items in data_list is a str
        - alphanum_source is a module
        The alphanum will be looked up by using the str from data_list as the
        name of a variable in the module
    """
    alphanum_list = []
    if type(data_list) not in (list, tuple):
        # Just a single item
        data_list = [data_list]
    for item in data_list:
        if isinstance(item, int) and type(alphanum_source) in (tuple, list):
            alphanum_list.append(alphanum_source[item])
        elif isinstance(item, int) and isinstance(alphanum_source, ModuleType):
            alphanum_list.append(alphanum_source.ALL_NUMBERS[item])
        elif isinstance(item, str) and isinstance(alphanum_source, ModuleType):
            alphanum_list.append(getattr(alphanum_source, item))
        else:
            raise NotImplementedError("No way to relate {item} to the source "
                                      "data type given {source_type}".format(
                                          item=item,
                                          source_type=type(alphanum_source)))
    return alphanum_list


def config_to_matrix(config, data, color):
    """
    Takes a configuration and data and generates a matrix using the two.

    If your config contains 'font_choices' each item in the list will be tried
    and the first one that works will be used.

    The config can also a matrix under the key 'item', in case you just want to
    add a static image.
    """
    matrix = generate_empty_matrix()
    for group_name, group_config in config.iteritems():
        if 'item' in group_config:
            group_display = [group_config['item']]
        else:
            data_name = group_config['data_name']
            if data_name in data:
                group_data = data[data_name]
            else:
                raise ValueError("{} not in the data given".format(data_name))
            if 'font_choices' in group_config:
                font_choices = group_config['font_choices']
                for font_choice in font_choices:
                    try:
                        group_display = data_to_alphanums(group_data,
                                                          font_choice)
                        break
                    except NotImplementedError:
                        pass
                else:
                    raise ValueError("None of the font choices for {} "
                                     "worked.".format(group_name))
            else:
                group_display = data_to_alphanums(group_data,
                                                  group_config['font'])
        spatial = group_config['spatial']
        spatial.setdefault('spacing', 0)
        add_items_to_matrix(group_display, matrix, color=color, **spatial)
    return matrix
