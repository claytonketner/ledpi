import math
from types import ModuleType

from clockpi.constants import ARRAY_HEIGHT
from clockpi.constants import ARRAY_WIDTH


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
            data_key = group_config['data_key']
            if data_key in data:
                group_data = data[data_key]
            else:
                raise ValueError("{} not in the data given".format(data_key))
            if 'font_choices' in group_config:
                font_choices = group_config['font_choices']
                for font_choice in font_choices:
                    try:
                        group_display = data_to_alphanums(group_data,
                                                          font_choice)
                        break
                    except Exception:
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
