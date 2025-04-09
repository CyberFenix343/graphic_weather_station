import random


class Sensor:
    """Base class representing a generic sensor."""
    _name = None
    _unit = None
    NUM_OF_MEASUREMENTS = 50


    def __init__(self, low_limit, high_limit):
        if hasattr(self, '_max_limit'):
            assert high_limit <= self._max_limit, "Wartość poza zakresem"

        if hasattr(self, '_min_limit'):
            assert low_limit >= self._min_limit, "Wartość poza zakresem"
            
        assert low_limit < high_limit, "Dolna granica większa od górnej"
        self._low_limit = low_limit
        self._high_limit = high_limit
        self._history = []

        

    def __str__(self):
        return f'{self.name()}: {self.measurement:.2f} {self.unit()}'

    def __lt__(self, other):
        return self.measurement < other.measurement

    def __le__(self, other):
        return self.measurement <= other.measurement

    def __gt__(self, other):
        return self.measurement > other.measurement

    def __ge__(self, other):
        return self.measurement >= other.measurement

    def __eq__(self, other):
        return self.measurement == other.measurement

    def __ne__(self, other):
        return self.measurement != other.measurement

    def __del__(self):
        print(f"Object of type {type(self)} from address {hex(id(self))} removed")

    @staticmethod
    def __rand(low_limit, high_limit):
        """Function returning a random number in range [low_limit, high_limit)."""
        return low_limit + random.random() * (high_limit - low_limit)

    @property
    def measurement(self):
        """Function simulating the action of making a measurement -
        a random number in range [low_limit, high_limit) is returned."""
        self.__measurement = Sensor.__rand(self._low_limit, self._high_limit)
        return self.__measurement

    @classmethod
    def name(cls):
        """Function returning the name of the measured value."""
        return cls._name

    @classmethod
    def unit(cls):
        """Function returning the unit of the measured value."""
        return cls._unit

    @property
    def low_limit(self):
        """Getter of _low_limit"""
        return self._low_limit

    @low_limit.setter
    def low_limit(self, low_limit):
        assert isinstance(low_limit, int), "To nie int"

        assert low_limit < self._high_limit, "Dolna granica jest większa od górnej"

        if hasattr(self, '_min_limit'):
            assert low_limit >= self._min_limit, "Wartość poza zakresem"

        self._low_limit = low_limit

    @property
    def high_limit(self):
        """Getter of _high_limit"""
        return self._high_limit

    @high_limit.setter
    def high_limit(self, high_limit):
        assert isinstance(high_limit, int), "To nie int"

        assert high_limit > self._low_limit, "Górna granica jest mniejsza od dolnej"

        if hasattr(self, '_max_limit'):
            assert high_limit <= self._max_limit, "Wartość poza zakresem"

        self._high_limit = high_limit

    def update_history(self):
        if len(self._history) <= self.NUM_OF_MEASUREMENTS:
            self._history.append(self.measurement)
        else:
            self._history.pop(0)
            self._history.append(self.measurement)

    @property
    def history(self):
        return self._history
   
    #@staticmethod  
    def to_sensor(typ):
   
        if typ == 'Temperature':
            return TemperatureSensor
        if typ == 'Humidity':
            return HumiditySensor
        if typ == 'Pressure':
            return PressureSensor
        if typ == 'Wind':
            return WindSensor
        if typ == 'Insolation':
            return InsolationSensor

class TemperatureSensor(Sensor):
    """Class representing a temperature sensor."""
    _name = "Temperature"
    _unit = "deg. Celsius"
    _min_limit = -273


class HumiditySensor(Sensor):
    """Class representing a humidity sensor."""
    _name = "Humidity"
    _unit = "%"
    _min_limit = 0
    _max_limit = 100


class PressureSensor(Sensor):
    """Class representing a pressure sensor."""
    _name = "Pressure"
    _unit = "hPa"
    _min_limit = 0


class WindSensor(Sensor):
    """Class representing a wind sensor."""
    _name = "Wind"
    _unit = "km/h"
    _min_limit = 0


class InsolationSensor(Sensor):
    """Class representing an insolation sensor."""
    _name = "Insolation"
    _unit = "W/m^2"
    _min_limit = 0


if __name__ == '__main__':
    ts = TemperatureSensor(101, 100)
 
