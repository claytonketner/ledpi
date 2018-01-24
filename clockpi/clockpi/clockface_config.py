from clockpi.alphanum import glyphs
from clockpi.alphanum import letters_tiny
from clockpi.alphanum import numbers_large
from clockpi.alphanum import numbers_small
from clockpi.alphanum import numbers_tiny


LARGE_WITH_TEMPERATURE_CONFIG = {
    'hour_digits': {
        'data_name': 'hour_digits',
        'spatial': {
            'origin_x': 1+12,
            'origin_y': 1+8,
            'spacing': 1,
        },
        'font': numbers_large,
    },
    'separator': {
        'data_name': 'separator',
        'spatial': {
            'origin_x': 15+12,
            'origin_y': 1+8,
            'spacing': 1,
        },
        'font': numbers_large,
    },
    'minute_digits': {
        'data_name': 'minute_digits',
        'spatial': {
            'origin_x': 18+12,
            'origin_y': 1+8,
            'spacing': 1,
        },
        'font': numbers_large,
    },
    'second_digits': {
        'data_name': 'second_digits',
        'spatial': {
            'origin_x': 32+12,
            'origin_y': 10+8,
            'spacing': 1,
        },
        'font': numbers_tiny,
    },
    'temp_digits': {
        'data_name': 'temp_digits',
        'spatial': {
            'origin_x': 32+12,
            'origin_y': 1+8,
            'spacing': 1,
        },
        'font': [numbers_tiny, letters_tiny, glyphs],
    },
}

TRAFFIC_CONFIG = {
    'hour_digits': {
        'data_name': 'hour_digits',
        'spatial': {
            'origin_x': 3+12,
            'origin_y': 1+8,
            'spacing': 1,
        },
        'font': numbers_small,
    },
    'hour_minute_separator': {
        'data_name': 'separator',
        'spatial': {
            'origin_x': 13+12,
            'origin_y': 1+8,
            'spacing': 1,
        },
        'font': numbers_small,
    },
    'minute_digits': {
        'data_name': 'minute_digits',
        'spatial': {
            'origin_x': 15+12,
            'origin_y': 1+8,
            'spacing': 1,
        },
        'font': numbers_small,
    },
    'minute_second_separator': {
        'data_name': 'separator',
        'spatial': {
            'origin_x': 25+12,
            'origin_y': 1+8,
            'spacing': 1,
        },
        'font': numbers_small,
    },
    'minute_second_separator_2': {
        'data_name': 'separator',
        'spatial': {
            'origin_x': 26+12,
            'origin_y': 1+8,
            'spacing': 1,
        },
        'font': numbers_small,
    },
    'second_digits': {
        'data_name': 'second_digits',
        'spatial': {
            'origin_x': 28+12,
            'origin_y': 1+8,
            'spacing': 1,
        },
        'font': numbers_small,
    },
    'traffic_delta': {
        'data_name': 'traffic_delta_digits',
        'spatial': {
            'origin_x': 3+12,
            'origin_y': 9+8,
            'spacing': 1,
        },
        'font': numbers_small,
    },
    'travel_time': {
        'data_name': 'travel_time_digits',
        'spatial': {
            'origin_x': 28+12,
            'origin_y': 9+8,
            'spacing': 1,
        },
        'font': numbers_small,
    },
}
