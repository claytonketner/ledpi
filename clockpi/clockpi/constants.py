from clockpi.enums import WeatherType


ARRAY_HEIGHT = 32
ARRAY_WIDTH = 64
# Clockface colors go from min to max to min throughout the day
DAILY_R_MIN = 5
DAILY_G_MIN = 0
DAILY_B_MIN = 0
DAILY_R_MAX = 50
DAILY_G_MAX = 50
DAILY_B_MAX = 50
DEFAULT_SUNRISE_HOUR = 6
DEFAULT_SUNSET_HOUR = 19
BLOOM_START_HOUR_OFFSET = 0  # Offset from sunrise
BLOOM_END_HOUR_OFFSET = 3  # Offset from sunset
DAILY_BRIGHTNESS_MIN = 1
DAILY_BRIGHTNESS_MAX = 40
GLOBAL_BRIGHTNESS_MIN = 2
SUN_ANIMATION_DURATION = 600  # Seconds
WEATHER_FORECAST_HOURS = 8  # Number of hours ahead to show the forecast for
# Lookup to simplify down the possible weather forecasts
W_GOV_ICON_2_WEATHER = {
    # List: https://api.weather.gov/icons
    'skc': WeatherType.CLEAR,
    'few': WeatherType.CLEAR,
    'sct': WeatherType.PARTLYCLOUDY,
    'bkn': WeatherType.CLOUDY,
    'ovc': WeatherType.CLOUDY,
    'wind_skc': WeatherType.CLEAR,
    'wind_few': WeatherType.CLEAR,
    'wind_sct': WeatherType.PARTLYCLOUDY,
    'wind_bkn': WeatherType.CLOUDY,
    'wind_ovc': WeatherType.CLOUDY,
    'snow': WeatherType.RAIN,  # TODO: make snow animation
    'rain_snow': WeatherType.RAIN,
    'rain_sleet': WeatherType.RAIN,
    'snow_sleet': WeatherType.RAIN,
    'fzra': WeatherType.RAIN,
    'rain_fzra': WeatherType.RAIN,
    'snow_fzra': WeatherType.RAIN,
    'sleet': WeatherType.RAIN,
    'rain': WeatherType.RAIN,
    'rain_showers': WeatherType.RAIN,
    'rain_showers_hi': WeatherType.RAIN,
    'tsra': WeatherType.RAIN,  # TODO: make thunderstorm animation
    'tsra_sct': WeatherType.RAIN,
    'tsra_hi': WeatherType.RAIN,
    'tornado': WeatherType.DEATH,
    'hurricane': WeatherType.DEATH,
    'tropical_storm': WeatherType.RAIN,
    'dust': WeatherType.PARTLYCLOUDY,
    'smoke': WeatherType.PARTLYCLOUDY,
    'haze': WeatherType.PARTLYCLOUDY,
    'hot': WeatherType.CLEAR,  # ??
    'cold': WeatherType.CLEAR,  # ??
    'blizzard': WeatherType.RAIN,
    'fog': WeatherType.CLOUDY,
}
