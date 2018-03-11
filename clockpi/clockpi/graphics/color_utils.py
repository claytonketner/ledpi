import math


def set_brightness(color, brightness, as_percentage=False):
    """
    Scales a color to a new brightness (0 to 255) or scales it by `brightness`
    as a percentage (where `brightness` is 0-1). Return colors are 0-255.
    """
    if not as_percentage and (brightness < 0 or brightness > 255):
        raise ValueError('Brightness {} is invalid.'.format(brightness))
    average = float(sum(color))/len(color)
    if average == 0:
        return [0, 0, 0]
    if as_percentage:
        average = 1
    return map(int, [max(0, min(255, c / average * brightness))
                     for c in color])


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
