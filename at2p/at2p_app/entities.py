class TempRange:
    def __init__(self, minimum: int, maximum: int) -> None:
        self.check_values(minimum, maximum)
        self.minimum = int(round(min(minimum, maximum)))
        self.maximum = int(round(max(minimum, maximum)))

    def __str__(self):
        min_str = "Minimum: " + str(self.minimum)
        max_str = "Maximum: " + str(self.maximum)
        return min_str + "\n" + max_str

    def __repr__(self):
        return (self.minimum, self.maximum)

    def check_values(self, min: int, max: int) -> None:
        min_type = type(min)
        max_type = type(max)
        min_is_num = min_type is int or min_type is float
        max_is_num = max_type is int or max_type is float
        values_are_nums = min_is_num and max_is_num
        if not values_are_nums:
            raise ValueError
        return


class Crop:
    def __init__(
        self, name: str, abs_temp: TempRange, opt_temp: TempRange
    ) -> None:
        self.check_values(name, abs_temp, opt_temp)
        self.name = name
        self.abs_temp = abs_temp
        self.opt_temp = opt_temp

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def check_values(self, name, abs_temp, opt_temp) -> None:
        self.check_name(name)
        self.check_temp_ranges(abs_temp, opt_temp)
        return

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

    def check_name(self, name: str) -> None:
        error_msg = "Name may not be blank or none!"
        name_is_blank = name == ""
        name_is_none = name == None
        if name_is_none or name_is_blank:
            raise ValueError(error_msg)
        return


class Country:
    def __init__(self, full_name: str, code: str) -> None:
        self.check_values(full_name, code)
        self.full_name = full_name.title()
        self.code = code.upper()

    def __str__(self):
        return self.full_name

    def __repr__(self):
        return self.code

    def check_values(self, full_name: str, code: str) -> None:
        self.check_name(full_name)
        self.check_code(code)
        return

    def check_name(self, full_name: str) -> None:
        error_msg = "Country name must be a string!"
        name_is_string = type(full_name) == str
        if not name_is_string:
            raise ValueError(error_msg)
        return

    def check_code(self, code: str) -> None:
        error_msg = "Country code must be a two character string!"
        code_is_string = type(code) == str
        if not code_is_string:
            raise ValueError(error_msg)

        code_length = 2
        if len(code) != code_length:
            raise ValueError(error_msg)

        return


class LatLong:
    lat: float
    long: float

    def __init__(self, lat: float, long: float) -> None:
        self.check_values(lat, long)
        self.lat = float(lat)
        self.long = float(long)

    def __str__(self):
        str_lat = f"Latitude: {self.lat:.4f}"
        str_long = f"Longitude: {self.long:.4f}"
        return str_lat + "\n" + str_long

    def __repr__(self):
        return (self.lat, self.long)

    def check_values(self, lat: float, long: float) -> None:
        self.check_lat(lat)
        self.check_long(long)

    def check_lat(self, lat: float) -> None:
        error_msg = "Latitude must be a number between -90 and 90"
        if self.is_a_number(lat):
            raise ValueError(error_msg)
        print(lat < 90)
        print(lat > -90)
        lat_ok = lat < 90 and lat > -90
        if not lat_ok:
            raise ValueError(error_msg)
        return

    def check_long(self, long: float) -> None:
        error_msg = "Longitude must be a number between -180 and 180"
        if self.is_a_number(long):
            raise ValueError(error_msg)
        long_ok = long < 180 and long > -180
        if not long_ok:
            raise ValueError(error_msg)

    def is_a_number(self, value) -> bool:
        val_type = type(value)
        return val_type in [int, float]



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
