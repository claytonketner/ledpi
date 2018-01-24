import math

from datetime import datetime
from random import random
from types import ModuleType

from clockpi.constants import ARRAY_HEIGHT
from clockpi.constants import ARRAY_WIDTH
from clockpi.constants import SUN_ANIMATION_DURATION
from clockpi.constants import SUN_ANIM_START_DIAMETER
from clockpi.constants import SUN_ANIM_GROWTH
from clockpi.constants import SUN_ANIM_TRAVEL
from clockpi.external import get_traffic
from clockpi.external import get_weather
from clockpi.graphics.color_utils import set_brightness
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
    red = calc_color_cos(day_elapsed_mins, 6*60, 24*60, 5, 150)
    green = calc_color_cos(day_elapsed_mins, 6*60, 24*60, 0, 150)
    blue = calc_color_cos(day_elapsed_mins, 6*60, 24*60, 0, 150)
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
    for item in data_list:
        if isinstance(item, int) and isinstance(alphanum_source, list):
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
    Takes a configuration and data and generates a matrix using the two. There
    is a special case where you can provide a list of fonts instead of a single
    font. In this case, each item in the list will be tried and the first one
    that works will be used.
    """
    matrix = generate_empty_matrix()
    for group_name, group_config in config.iteritems():
        data_name = group_config['data_name']
        if data_name not in data:
            print "{} not in the data given".format(data_name)
            continue
        group_data = data[data_name]
        font = group_config['font']
        if isinstance(font, list):
            for font_choice in font:
                try:
                    group_display = data_to_alphanums(group_data, font_choice)
                    break
                except Exception:
                    pass
            else:
                raise ValueError("None of the font choices for {} "
                                 "worked.".format(group_name))
        else:
            group_display = data_to_alphanums(group_data, font)
        add_items_to_matrix(group_display, matrix, color=color,
                            **group_config['spatial'])
    return matrix


def generate_sun_matrix(center_y, radius):
    """
    Generates a matrix containing a horizontally centered sun. Assumes only
    the upper half of the sun is needed.
    """
    orange = [255, 174, 0]
    orange = set_brightness(orange, 80)
    radius = int(radius)
    center_x = ARRAY_WIDTH / 2
    matrix = generate_empty_matrix()
    for ii in xrange(radius + 1):
        if center_x - ii < 0:
            # Off matrix
            continue
        x_t = math.acos(float(ii) / radius)
        edge_y = round(math.sin(x_t) * radius)
        for jj in xrange(int(edge_y) + 1):
            if center_y - jj > ARRAY_HEIGHT or center_y - jj < 0:
                # Off matrix
                continue
            # We only need the top hemisphere (quadrants 1 and 2)
            dist_from_center = math.sqrt(abs(ii - center_x)**2 +
                                         abs(jj - center_y)**2)
            new_brightness = dist_from_center / radius * 100
            if new_brightness > 100:
                new_brightness = 100
            current_orange = set_brightness(orange, new_brightness)
            add_to_matrix([[current_orange]], matrix,
                          int(center_x + ii + 0.5),
                          int(center_y - jj + 0.5))
            add_to_matrix([[current_orange]], matrix,
                          int(center_x - ii + 0.5),
                          int(center_y - jj + 0.5))
            # Add some noise all over and a little past the edge
            randomness = 0.1
            if random() < randomness:
                add_to_matrix([[orange]], matrix,
                              int(center_x + ii + 0.5),
                              int(center_y - jj - 0.5))
            if random() < randomness:
                add_to_matrix([[orange]], matrix,
                              int(center_x - ii + 0.5),
                              int(center_y - jj - 0.5))
    return matrix


def get_animated_sun(anim_pct, is_rising):
    """
    Given the current percent completion of the animation, returns an array
    of the sun showing the current frame of animation.

    anim_pct: float 0.0 to 1.0
    """
    if not is_rising:
        anim_pct = 1 - anim_pct
    sun_diameter = SUN_ANIM_START_DIAMETER + SUN_ANIM_GROWTH * anim_pct
    sun_y = sun_diameter / 2 + ARRAY_HEIGHT - SUN_ANIM_TRAVEL * anim_pct
    return generate_sun_matrix(sun_y, sun_diameter / 2)
