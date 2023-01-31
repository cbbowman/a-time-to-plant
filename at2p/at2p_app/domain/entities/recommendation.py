from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Tuple
from at2p_app.domain.entities.location import Place
from at2p_app.domain.entities.crop import Crop


@dataclass(eq=True)
class Confidence(Enum):
    LOW = 95
    MODERATE = 98
    HIGH = 100

    def __str__(self):
        return f"{self.name.capitalize()}"


@dataclass
class Recommendation:
    location: Place = Place("22405")
    crops: Tuple[Crop] = ()
    confidence: Confidence = Confidence.HIGH
    time_stamp: datetime = datetime.now()
