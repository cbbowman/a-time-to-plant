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
    def __init__(self, name: str, abs_temp: TempRange,
                 opt_temp: TempRange) -> None:
        self.name = name
        self.check_temp_ranges(abs_temp, opt_temp)
        self.abs_temp = abs_temp
        self.opt_temp = opt_temp

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def check_temp_ranges(
            self, abs_temp: TempRange, opt_temp: TempRange) -> None:
        error_msg = 'Optimal range must be inside absolute range!'
        min_wrong = abs_temp.minimum > opt_temp.minimum
        max_wrong = abs_temp.maximum < opt_temp.maximum
        opt_not_within_abs = min_wrong or max_wrong
        if opt_not_within_abs:
            raise ValueError(error_msg)
        return


class Country:
    name: str
    code: str


class LatLong:
    lat: float
    long: float


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
