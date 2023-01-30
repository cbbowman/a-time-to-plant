from dataclasses import dataclass


class LatLongError(Exception):
    generic_msg = "Generic Coordinates Error"

    def __init__(
        self, lat: float, long: float, error_msg: str = generic_msg
    ) -> None:
        message = f"\n{error_msg}\nLat: {lat}\nLong: {long}"
        super().__init__(message)


@dataclass
class LatLong:
    lat: float
    long: float

    def __post_init__(self):
        self._check_values()
        return

    def __str__(self):
        ns = "S" if self.lat < 0 else "N"
        ew = "W" if self.long < 0 else "E"
        lat_str = f"{abs(self.lat):.2f}\u00b0{ns}"
        long_str = f"{abs(self.long):.2f}\u00b0{ew}"
        return f"{lat_str} {long_str}"

    def _check_values(self) -> None:
        self._check_lat()
        self._check_long()

    def _check_lat(self) -> None:
        error_msg = "Latitude must be a number between -90 and 90"
        if not self._is_a_number(self.lat):
            raise LatLongError(self.lat, self.long, error_msg)
        lat_ok = self.lat < 90 and self.lat > -90
        if not lat_ok:
            raise LatLongError(self.lat, self.long, error_msg)
        return

    def _check_long(self) -> None:
        error_msg = "Longitude must be a number between -180 and 180"
        if not self._is_a_number(self.long):
            raise LatLongError(self.lat, self.long, error_msg)
        long_ok = self.long < 180 and self.long > -180
        if not long_ok:
            raise LatLongError(self.lat, self.long, error_msg)

    def _is_a_number(self, value) -> bool:
        return isinstance(value, int) or isinstance(value, float)
