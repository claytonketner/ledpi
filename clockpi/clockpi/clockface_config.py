from clockpi.alphanum import glyphs
from clockpi.alphanum import letters_tiny
from clockpi.alphanum import numbers_large
from clockpi.alphanum import numbers_small
from clockpi.alphanum import numbers_tiny


LARGE_WITH_TEMPERATURE_CONFIG = {
    'hour_digits': {
        'data_name': 'hour_digits',
        'spatial': {
            'origin_x': 12,
            'origin_y': 8,
            'spacing': 1,
        },
        'font': numbers_large,
    },
    'separator': {
        'data_name': 'separator',
        'spatial': {
            'origin_x': 26,
            'origin_y': 8,
            'spacing': 1,
        },
        'font': numbers_large,
    },
    'minute_digits': {
        'data_name': 'minute_digits',
        'spatial': {
            'origin_x': 29,
            'origin_y': 8,
            'spacing': 1,
        },
        'font': numbers_large,
    },
    'second_digits': {
        'data_name': 'second_digits',
        'spatial': {
            'origin_x': 43,
            'origin_y': 17,
            'spacing': 1,
        },
        'font': numbers_tiny,
    },
    'temp_digits': {
        'data_name': 'temp_digits',
        'spatial': {
            'origin_x': 43,
            'origin_y': 8,
            'spacing': 1,
        },
        'font': [numbers_tiny, letters_tiny, glyphs],
    },
}

TRAFFIC_CONFIG = {
    'hour_digits': {
        'data_name': 'hour_digits',
        'spatial': {
            'origin_x': 12,
            'origin_y': 8,
            'spacing': 1,
        },
        'font': numbers_large,
    },
    'separator': {
        'data_name': 'separator',
        'spatial': {
            'origin_x': 26,
            'origin_y': 8,
            'spacing': 1,
        },
        'font': numbers_large,
    },
    'minute_digits': {
        'data_name': 'minute_digits',
        'spatial': {
            'origin_x': 29,
            'origin_y': 8,
            'spacing': 1,
        },
        'font': numbers_large,
    },
    'second_digits': {
        'data_name': 'second_digits',
        'spatial': {
            'origin_x': 43,
            'origin_y': 17,
            'spacing': 1,
        },
        'font': numbers_tiny,
    },
    'temp_digits': {
        'data_name': 'temp_digits',
        'spatial': {
            'origin_x': 43,
            'origin_y': 8,
            'spacing': 1,
        },
        'font': [numbers_tiny, letters_tiny, glyphs],
    },
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
