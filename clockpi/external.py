import googlemaps
import requests
from datetime import datetime

from clockpi.secret import DIRECTIONS_DESTINATION
from clockpi.secret import DIRECTIONS_ORIGIN
from clockpi.secret import GMAPS_DIRECTIONS_API_KEY
from clockpi.secret import WU_ASTRO_URL
from clockpi.secret import WU_WEATHER_URL


def get_weather(last_update_time, weather={}, cache_minutes=10):
    """
    Gets weather via the Weather Underground (wunderground.com) API
    cache_minutes should be >= 6 due to WU rate limits (because we're making
    two requests each time)
    """
    now = datetime.now()
    if last_update_time:
        passed_minutes = (now - last_update_time).seconds/60
    else:
        passed_minutes = cache_minutes
    if passed_minutes >= cache_minutes:
        try:
            wu_weather = requests.get(WU_WEATHER_URL).json()
            wu_astro = requests.get(WU_ASTRO_URL).json()
            current_temp = wu_weather['current_observation']['feelslike_f']
            weather['current_temp'] = float(current_temp)
            sun_info = wu_astro['sun_phase']
            now = datetime.now()
            weather['sunrise'] = datetime(now.year, now.month, now.day,
                                          int(sun_info['sunrise']['hour']),
                                          int(sun_info['sunrise']['minute']))
            weather['sunset'] = datetime(now.year, now.month, now.day,
                                         int(sun_info['sunset']['hour']),
                                         int(sun_info['sunset']['minute']))
        except Exception as e:
            print e.message
            weather = {}
        last_update_time = now
    return last_update_time, weather


def get_traffic(last_update_time, traffic, cache_minutes=5):
    # Google maps standard API allows 2500 requests/day, which is just over
    # two per minute
    now = datetime.now()
    if last_update_time:
        passed_minutes = (now - last_update_time).seconds/60
    else:
        passed_minutes = cache_minutes
    if passed_minutes >= cache_minutes:
        directions = None
        try:
            cl = googlemaps.Client(key=GMAPS_DIRECTIONS_API_KEY)
            directions = cl.directions(
                DIRECTIONS_ORIGIN,
                DIRECTIONS_DESTINATION,
                mode='driving',
                departure_time=now)
        except Exception as e:
            print e.message
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
        last_update_time = now
    return last_update_time, traffic
