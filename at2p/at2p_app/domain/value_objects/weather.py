from dataclasses import dataclass
from datetime import datetime
from at2p_app.domain.value_objects.temperature import Temperature
from at2p_app.domain.common.error import WeatherError
from at2p_app.domain.entities.place import Place


@dataclass(frozen=True)
class Weather:
    location: Place
    high: Temperature
    low: Temperature
    avg: Temperature
    time_stamp: datetime = datetime.now()
