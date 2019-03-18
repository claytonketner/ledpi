from collections import OrderedDict

from clockpi.alphanum import glyphs
from clockpi.alphanum import letters_tiny
from clockpi.alphanum import numbers_large
from clockpi.alphanum import numbers_small
from clockpi.alphanum import numbers_tiny
from clockpi.alphanum import weather_animations
from clockpi.procedural_animations import ProceduralRain


CLOUD_COLOR = [100, 100, 100]
"""
Clockface configuration information. A certain configuration consists of dict
of inner dicts that describe what should be displayed and where, along with
some other details. The outermost keys are just names and are not actually
used. Not all of the following keys are required.

- item: the item to be displayed. Useful for if you just want to show a static
    image and there is nothing to be looked up
- data_key: is the key to the `clock_info` dict whose value contains the data
    used to look up what should be displayed within the given `font`
- spatial: information on where/how the item should be drawn
- font: an iterable or module that contains the thing(s) to be drawn on screen
    which are looked up using `data_key`
- font_choices: an iterable of `font`s that get tried in order to be used, for
    example, if a number display should also sometimes be able to show letters
- color: a custom RGB color (0-255)

Put the word 'animation' in the key for that item to be handled as an
animation, which means you don't need to include a `data_key`.
"""

# The keys of this dict correspond to the possible weather forecasts
WEATHER_ANIMATIONS = {
    'sunny': {
        'sunshine_animation': {
            'spatial': {
                'center_x': 19,
                'center_y': 14,
            },
            'font': weather_animations.SUN_ANIMATION,
            'color': [244, 188, 66],
        },
    },
    'moon': {
        'moon': {
            'spatial': {
                'center_x': 19,
                'center_y': 9,
            },
            'item': weather_animations.MOON_LARGE,
            'color': [244, 188, 66],
            'mask': True,
        },
    },
    'cloudy': {
        'cloud': {
            'spatial': {
                'center_x': 18,
                'center_y': 8,
            },
            'item': weather_animations.CLOUD_LONG,
            'color': CLOUD_COLOR,
            'mask': True,
        },
    },
    'cloudy_sun': OrderedDict((
        ('sun_animation', {
            'spatial': {
                'center_x': 19,
                'center_y': 14,
            },
            'font': weather_animations.SUN_ANIMATION,
            'color': [244, 188, 66],
         }),
        ('cloudy_animation', {
            'spatial': {
                'center_x': 14,
                'center_y': 14,
            },
            'font': weather_animations.CLOUDY_ANIMATION_LATERAL,
            'color': CLOUD_COLOR,
            'mask': True,
         }),
        ('cloudy_animation_2', {
            'spatial': {
                'center_x': 24,
                'center_y': 12,
            },
            'font': weather_animations.CLOUDY_ANIMATION_UP_DOWN,
            'color': CLOUD_COLOR,
            'mask': True,
         }),
    )),
    'cloudy_moon': OrderedDict((
        ('cloud_1', {
            'spatial': {
                'center_x': 19,
                'center_y': 8,
            },
            'item': weather_animations.CLOUD_LONG,
            'color': CLOUD_COLOR,
            'mask': True,
         }),
        ('moon', {
            'spatial': {
                'center_x': 19,
                'center_y': 9,
            },
            'item': weather_animations.MOON_LARGE,
            'color': [244, 188, 66],
            'mask': True,
         }),
    )),
    'rain': OrderedDict((
        ('rain_animation', {
            'spatial': {
                'origin_x': 1,
                'origin_y': 6,
            },
            'procedural_animation': ProceduralRain(38, 32, [30, 172, 255]),
        }),
        ('cloud_1', {
            'spatial': {
                'center_x': 20,
                'center_y': 8,
            },
            'item': weather_animations.CLOUD_LONG,
            'color': CLOUD_COLOR,
            'mask': True,
         }),
    )),
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
            'center_x': 19,
            'origin_y': 6,
            'spacing': 1,
        },
        'font_choices': [numbers_tiny, letters_tiny, glyphs],
    },
    'temp_deg_symbol': {
        'item': glyphs.DEGREE,
        'spatial': {
            'origin_x': 24,
            'origin_y': 5,
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
