from dataclasses import dataclass
from datetime import datetime
from at2p_app.domain.value_objects.temperature import Temperature


@dataclass(frozen=True)
class Weather:
    high: Temperature
    low: Temperature
    avg: Temperature
    time_stamp: datetime = datetime.now()
