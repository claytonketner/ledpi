from enum import Enum


class WeatherType(Enum):
    # Number is severity - higher is more severe weather
    CLEAR = 10
    PARTLYCLOUDY = 20
    CLOUDY = 30
    RAIN = 40
    DEATH = 999

    def __eq__(self, other):
        if self.value == other.value:
            return True
        return False

    def __gt__(self, other):
        if self.value > other.value:
            return True
        return False

    def __lt__(self, other):
        if self.value < other.value:
            return True
        return False
