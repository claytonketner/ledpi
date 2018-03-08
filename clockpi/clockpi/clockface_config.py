from clockpi.alphanum import glyphs
from clockpi.alphanum import letters_tiny
from clockpi.alphanum import numbers_large
from clockpi.alphanum import numbers_small
from clockpi.alphanum import numbers_tiny
from clockpi.alphanum import weather_animations


# The keys of this dict correspond to the possible weather forecasts
WEATHER_ANIMATIONS = {
    'sunny': {
        'sunshine_animation': {
            'data_key': 'weather_anim',
            'spatial': {
                'origin_x': 48,
                'origin_y': 8,
            },
            'font': weather_animations.SUN_ANIMATION,
        },
    },
    'moon': {
        'moon_animation': {
            'data_key': 'weather_anim',
            'spatial': {
                'origin_x': 48,
                'origin_y': 8,
            },
            'font': weather_animations.MOON_ANIMATION,
        },
    },
    'cloudy': {
        'cloudy_animation': {
            'data_key': 'weather_anim',
            'spatial': {
                'origin_x': 48,
                'origin_y': 8,
            },
            'font': weather_animations.CLOUDY_ANIMATION,
        },
    },
    'cloudy_sun': {
        'cloudy_sun_animation': {
            'data_key': 'weather_anim',
            'spatial': {
                'origin_x': 48,
                'origin_y': 8,
            },
            'font': weather_animations.CLOUDY_SUN_ANIMATION,
        },
    },
    'cloudy_moon': {
        'cloudy_moon_animation': {
            'data_key': 'weather_anim',
            'spatial': {
                'origin_x': 48,
                'origin_y': 8,
            },
            'font': weather_animations.CLOUDY_MOON_ANIMATION,
        },
    },
    'rain': {
        'rain_animation': {
            'data_key': 'weather_anim',
            'spatial': {
                'origin_x': 48,
                'origin_y': 8,
            },
            'font': weather_animations.RAIN_ANIMATION,
        },
    },
}

PLAIN_CLOCKFACE = {
    'hour_digits': {
        'data_key': 'hour_digits',
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
        'data_key': 'minute_digits',
        'spatial': {
            'origin_x': 18,
            'origin_y': 17,
            'spacing': 1,
        },
        'font': numbers_large,
    },
    'second_digits': {
        'data_key': 'second_digits',
        'spatial': {
            'origin_x': 32,
            'origin_y': 26,
            'spacing': 1,
        },
        'font': numbers_tiny,
    },
    'temp_digits': {
        'data_key': 'temp_digits',
        'spatial': {
            'origin_x': 52,
            'origin_y': 2,
            'spacing': 1,
        },
        'font_choices': [numbers_tiny, letters_tiny, glyphs],
    },
    'temp_deg_symbol': {
        'item': glyphs.DEGREE,
        'spatial': {
            'origin_x': 60,
            'origin_y': 1,
        },
    },
}

TRAFFIC_CLOCKFACE = {
    'traffic_delta': {
        'data_key': 'traffic_delta_digits',
        'spatial': {
            'origin_x': 54,
            'origin_y': 25,
            'spacing': 1,
        },
        'font': numbers_small,
    },
    'travel_time': {
        'data_key': 'travel_time_digits',
        'spatial': {
            'origin_x': 54,
            'origin_y': 18,
            'spacing': 1,
        },
        'font': numbers_small,
    },
}
TRAFFIC_CLOCKFACE.update(PLAIN_CLOCKFACE)
