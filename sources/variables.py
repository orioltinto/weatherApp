from enum import Enum


class Variables(Enum):
    precipitation = "niederschlag"
    accumulated_precipitation = "niederschlagssumme"
    temperature = "temperatur"
    humidity = "relfeuchte"
    dew_point = "taupunkt"
    pressure = "luftdruck"
