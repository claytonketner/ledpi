from types import ModuleType

from clockpi.constants import ARRAY_HEIGHT
from clockpi.constants import ARRAY_WIDTH
from clockpi.graphics.color_utils import set_brightness


def generate_empty_matrix(fill_with=[0, 0, 0]):
    """Generates a matrix of zeros that can be referenced like:
        my_matrix[x_coordinate][y_coordinate]
    """
    empty_matrix = []
    for _ in xrange(ARRAY_WIDTH):
        empty_matrix.append([fill_with] * ARRAY_HEIGHT)
    return empty_matrix


def add_to_matrix(partial_matrix, matrix, x, y, color=None, brightness=None,
                  transpose=True, bit_or=True, bit_and=False, bit_xor=False,
                  mask=False, mask_amount=0.5):
    """
    Adds `partial_matrix` to `matrix` at `x`, `y`. If `color` is specified,
    `partial_matrix` will be copied using that color - otherwise, the color
    in `partial_matrix` will just be copied over.

    transpose: transpose the partial_matrix before applying it to the `matrix`
    bit_or: do a bitwise OR (ish) to determine the final pixel color
    bit_and: do a bitwise AND to determine the final pixel color
    bit_xor: do a bitwise XOR to determine the final pixel color
    mask: dim pixels if they're adjacent to ON pixels (including diagonals)
    mask_amount: amount to dim pixels as a percentage for the mask
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
                        # TODO is this actually useful?
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
            if brightness:
                final_val = set_brightness(final_val, brightness)
            matrix[x+xx][y+yy] = final_val
            if mask and any(pm_val):
                # Knock back all adjacent pixels (including diagonals)
                for ii in xrange(-1, 2):
                    for jj in xrange(-1, 2):
                        if ii == 0 and jj == 0:
                            # Don't check our current/center pixel
                            continue
                        matrix_x = x + xx + ii
                        matrix_y = y + yy + jj
                        pm_x = xx + ii
                        pm_y = yy + jj
                        # Check if we're in bounds
                        in_matrix = (
                            matrix_x >= 0 and matrix_y >= 0 and
                            matrix_x < len(matrix) and
                            matrix_y < len(matrix[0]))
                        if not in_matrix:
                            continue
                        in_partial_matrix = (
                            pm_x >= 0 and pm_y >= 0 and
                            pm_x < partial_matrix_x_len and
                            pm_y < partial_matrix_y_len)
                        apply_mask = True
                        if in_partial_matrix:
                            # Make sure we don't knock back a pixel that
                            # came from the source matrix
                            if transpose:
                                mask_pm_val = partial_matrix[pm_y][pm_x]
                            else:
                                mask_pm_val = partial_matrix[pm_x][pm_y]
                            if type(mask_pm_val) not in (tuple, list):
                                apply_mask = not mask_pm_val
                            else:
                                apply_mask = not any(mask_pm_val)
                        if apply_mask:
                            matrix[matrix_x][matrix_y] = set_brightness(
                                matrix[matrix_x][matrix_y], mask_amount,
                                as_percentage=True)


def add_items_to_matrix(items, matrix, origin_x=None, origin_y=None,
                        center_x=None, center_y=None, spacing=0, **kwargs):
    """Adds a left-aligned 'sentence', which consists of `items`, which are
    separated by `spacing`, which can be an integer, or a list containing
    spacing distances between each item in `items` (len = n - 1)

    origin_x: top left corner X position (can use center_x instead)
    origin_y: top left corner Y position (can use center_y instead)
    center_x: center X position (optional). This will be the centerline of the
              resulting 'sentence'.
    center_y: center Y position (optional). This will be the centerline of the
              resulting 'sentence'.
    """
    if (origin_x is None and center_x is None) or all([origin_x, center_x]):
        raise ValueError("Must specify either origin_x or center_x")
    if (origin_y is None and center_y is None) or all([origin_y, center_y]):
        raise ValueError("Must specify either origin_y or center_y")
    if center_x or center_y:
        total_width = 0
        total_height = 0
        for ii in xrange(len(items)):
            item = items[ii]
            total_width += len(item[0])
            total_height = max(total_height, len(item))
            if ii > 0:
                space = spacing
                if hasattr(spacing, '__iter__'):
                    space = spacing[ii-1]
                total_width += space
        if center_x:
            origin_x = int(center_x - total_width / 2)
        if center_y:
            origin_y = int(center_y - total_height / 2)
    x = origin_x
    y = origin_y
    for ii in xrange(len(items)):
        item = items[ii]
        if ii > 0:
            space = spacing
            if hasattr(spacing, '__iter__'):
                space = spacing[ii-1]
            x += space + len(items[ii-1][0])
        add_to_matrix(item, matrix, x, y, **kwargs)


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


def config_to_matrix(config, data, color=None, brightness=None):
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
        if color is None and 'color' in group_config:
            color = group_config['color']
        mask = group_config.get('mask', False)
        add_items_to_matrix(group_display, matrix, color=color,
                            brightness=brightness, mask=mask, **spatial)
    return matrix
