import googlemaps
import logging
import re
import requests
from datetime import datetime
from urlparse import urlparse

from clockpi.constants import W_GOV_ICON_2_WEATHER
from clockpi.constants import WEATHER_FORECAST_HOURS
from clockpi.secret import DIRECTIONS_DESTINATION
from clockpi.secret import DIRECTIONS_ORIGIN
from clockpi.secret import GMAPS_DIRECTIONS_API_KEY
from clockpi.secret import WU_ASTRO_URL
from clockpi.secret import W_GOV_WEATHER_URL


logger = logging.getLogger(__name__)


class APIClient(object):
    """Base class for an API client.
    """
    def __init__(self, mp_pipe):
        """mp_pipe is a multiprocessing pipe used to transfer data.
        Make sure to set `cache_minutes` so that you don't go over usage
        limits!
        """
        self.mp_pipe = mp_pipe
        self.cache_minutes = 10
        self.last_update_time = None  # Datetime object
        self.cleaned_data = {}  # Data from the API that has been cleaned
        self.enabled = True  # Won't run if False

    def run(self):
        """The method to be called continuously. Handles keeping track of rate
        limiting based on `cache_minutes` to avoid going over API usage limits.
        Returns True if an update happened.
        """
        # Get data from the pipe, which will just be enable/disable
        if self.mp_pipe.poll():
            self.enabled = self.mp_pipe.recv()
            logger.info("API client received {}".format(self.enabled))
        if not self.enabled:
            return False
        now = datetime.now()
        if self.last_update_time:
            passed_minutes = (now - self.last_update_time).seconds/60
        else:
            passed_minutes = self.cache_minutes
        if passed_minutes >= self.cache_minutes:
            self.last_update_time = now
            new_data = self.call_api()
            self.cleaned_data.update(new_data)
            self.mp_pipe.send(self.cleaned_data)
            return True
        return False

    def call_api(self):
        """Override this in your child class. It should return a dict of
        cleaned data from the API.
        """
        pass


class WeatherAPIClient(APIClient):
    def __init__(self, mp_pipe):
        super(WeatherAPIClient, self).__init__(mp_pipe)
        self.cache_minutes = 10

    def call_api(self):
        weather = {}
        weather['error'] = False
        try:
            weather_json = requests.get(W_GOV_WEATHER_URL).json()
            # List of hourly weather forecast. Index is number of hours
            # into the future from now (0 = now, 1 = next hour, etc.)
            hourly_weather = weather_json['properties']['periods']
            weather['current_temp'] = int(hourly_weather[0]['temperature'])
            logger.info("Got current temp {}".format(weather['current_temp']))
            weather['forecast'] = None
            for hour_weather in hourly_weather[0:WEATHER_FORECAST_HOURS+1]:
                # Find the most severe weather in this interval. Use the
                # icon to determine the weather, because that's the most
                # pared down. https://api.weather.gov/icons
                forecast_icon_url = hour_weather['icon']
                icon_path = urlparse(forecast_icon_url).path
                # Sometimes, the icon path will have a comma and a number after
                # like: /icons/land/night/rain_showers,20
                icon_re = re.compile('/[A-Za-z_]+')
                re_matches = icon_re.findall(icon_path)
                if re_matches:
                    # Icon name will be the last match. Also, strip off the
                    # leading slash from the regex match
                    icon_name = re_matches[-1][1:]
                    matched_forecast = W_GOV_ICON_2_WEATHER[icon_name]
                    if weather.get('forecast'):
                        # Replace the forecast with the more severe weather
                        weather['forecast'] = max(weather['forecast'],
                                                  matched_forecast)
                    else:
                        # First valid forecast
                        weather['forecast'] = matched_forecast
            logger.info("Got forecast {}".format(weather['forecast']))
        except Exception:
            logger.exception('Exception during weather API call.')
            weather['error'] = True
        try:
            wu_astro = requests.get(WU_ASTRO_URL).json()
            sun_info = wu_astro['sun_phase']
            now = datetime.now()
            weather['sunrise'] = datetime(
                now.year, now.month, now.day,
                int(sun_info['sunrise']['hour']),
                int(sun_info['sunrise']['minute']))
            weather['sunset'] = datetime(now.year, now.month, now.day,
                                         int(sun_info['sunset']['hour']),
                                         int(sun_info['sunset']['minute']))
            logger.info("Got sunrise {} and sunset {}".format(
                        weather['sunrise'], weather['sunset']))
        except Exception:
            logger.exception('Exception during astro API call.')
            weather['error'] = True
        return weather


class TrafficAPIClient(APIClient):
    def __init__(self, mp_pipe):
        # Google maps standard API allows 2500 requests/day, which is just over
        # two per minute
        super(TrafficAPIClient, self).__init__(mp_pipe)
        self.cache_minutes = 5

    def call_api(self):
        traffic = {}
        directions = None
        now = datetime.now()
        try:
            cl = googlemaps.Client(key=GMAPS_DIRECTIONS_API_KEY)
            directions = cl.directions(
                DIRECTIONS_ORIGIN,
                DIRECTIONS_DESTINATION,
                mode='driving',
                departure_time=now)
        except Exception:
            logger.exception('Exception during traffic API call')
            traffic = {}
        if directions:
            # Only one destination, so just extract the first leg
            directions = directions[0]['legs'][0]
            duration = directions['duration']['value']
            # Google doesn't always include duration_in_traffic
            if directions.get('duration_in_traffic'):
                dur_in_traffic = directions['duration_in_traffic']['value']
            else:
                dur_in_traffic = duration
            if dur_in_traffic > duration:
                traffic['traffic_delta'] = (
                    dur_in_traffic - directions['duration']['value']) / 60
            else:
                traffic['traffic_delta'] = 0
            traffic['travel_time'] = dur_in_traffic / 60
        return traffic
