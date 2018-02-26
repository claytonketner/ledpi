from clockpi.alphanum import glyphs
from clockpi.alphanum import letters_tiny
from clockpi.alphanum import numbers_large
from clockpi.alphanum import numbers_small
from clockpi.alphanum import numbers_tiny


LARGE_WITH_TEMPERATURE_CONFIG = {
    'hour_digits': {
        'data_name': 'hour_digits',
        'spatial': {
            'origin_x': 1,
            'origin_y': 17,
            'spacing': 1,
        },
        'font': numbers_large,
    },
    'separator': {
        'item': numbers_large.SEPARATOR,
        'spatial': {
            'origin_x': 15,
            'origin_y': 17,
        },
    },
    'minute_digits': {
        'data_name': 'minute_digits',
        'spatial': {
            'origin_x': 18,
            'origin_y': 17,
            'spacing': 1,
        },
        'font': numbers_large,
    },
    'second_digits': {
        'data_name': 'second_digits',
        'spatial': {
            'origin_x': 32,
            'origin_y': 26,
            'spacing': 1,
        },
        'font': numbers_tiny,
    },
    'temp_digits': {
        'data_name': 'temp_digits',
        'spatial': {
            'origin_x': 51,
            'origin_y': 2,
            'spacing': 1,
        },
        'font_choices': [numbers_tiny, letters_tiny, glyphs],
    },
    'temp_deg_symbol': {
        'item': glyphs.DEGREE,
        'spatial': {
            'origin_x': 59,
            'origin_y': 1,
        },
    },
    'sun': {
        'data_name': 'sunshine_anim',
        'spatial': {
            'origin_x': 47,
            'origin_y': 8,
        },
        'font': glyphs.SHINING_SUN
    },
}

TRAFFIC_CONFIG = {
    'traffic_delta': {
        'data_name': 'traffic_delta_digits',
        'spatial': {
            'origin_x': 54,
            'origin_y': 25,
            'spacing': 1,
        },
        'font': numbers_small,
    },
    'travel_time': {
        'data_name': 'travel_time_digits',
        'spatial': {
            'origin_x': 54,
            'origin_y': 18,
            'spacing': 1,
        },
        'font': numbers_small,
    },
}
TRAFFIC_CONFIG.update(LARGE_WITH_TEMPERATURE_CONFIG)
