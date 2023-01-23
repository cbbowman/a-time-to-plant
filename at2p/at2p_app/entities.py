import string


class TempRange:
    def __init__(self, minimum: int, maximum: int) -> None:
        self.minimum = min(minimum, maximum)
        self.maximum = max(minimum, maximum)

    def __str__(self):
        min_str = "Minimum: " + str(self.minimum)
        max_str = "Maximum: " + str(self.maximum)
        return min_str + "\n" + max_str

    def __repr__(self):
        return self.__str__()


class Crop:
    def __init__(
        self, name: str, abs_temp: TempRange, opt_temp: TempRange
    ) -> None:
        self.name = name
        self.check_temp_ranges(abs_temp, opt_temp)
        self.abs_temp = abs_temp
        self.opt_temp = opt_temp

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def check_temp_ranges(
        self, abs_temp: TempRange, opt_temp: TempRange
    ) -> None:
        error_msg = "Optimal range must be inside absolute range!"
        min_wrong = abs_temp.minimum > opt_temp.minimum
        max_wrong = abs_temp.maximum < opt_temp.maximum
        opt_not_within_abs = min_wrong or max_wrong
        if opt_not_within_abs:
            raise ValueError(error_msg)
        return


class Country:
    def __init__(self, full_name: str, code: str) -> None:
        self.full_name = full_name.title()
        self.code = code.upper()

    def __str__(self):
        return self.full_name

    def __repr__(self):
        return self.code


class LatLong:
    lat: float
    long: float

    def __init__(self, lat: float, long: float) -> None:
        self.lat = float(lat)
        self.long = float(long)

    def __str__(self):
        str_lat = f'Latitude: {self.lat:.4f}'
        str_long = f'Longitude: {self.long:.4f}'
        return str_lat + '\n' + str_long

    def __repr__(self):
        return (self.lat, self.long)


class Place:
    country: Country
    state: str
    city: str
    zip: str
    coord: LatLong
    elev: int


class Planter:
    username: str
    location: Place

    pass


class Weather:
    pass


class Weather:
    pass
