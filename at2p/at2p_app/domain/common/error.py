class CountryError(Exception):
    generic_msg = "Generic Country Error"

    def __init__(self, code: str, error_msg: str = generic_msg) -> None:
        message = f"\n{error_msg}\nCode: {code}"
        super().__init__(message)


class CropError(Exception):
    generic_msg = "Generic Crop Error"

    def __init__(self, name: str, error_msg: str = generic_msg) -> None:
        message = f"\n{error_msg}\nName: {name}\n"
        super().__init__(message)


class CropRepoError(Exception):
    generic_msg = "Generic Repository Error"

    def __init__(self, error_msg: str = generic_msg) -> None:
        message = f"\n{error_msg}\n"
        super().__init__(message)


class InterfaceError(Exception):
    generic_msg = "Generic Interface Error"

    def __init__(self, error_msg: str = generic_msg) -> None:
        message = f"\n{error_msg}\n"
        super().__init__(message)


class PlanterError(Exception):
    error_msg = "Generic Person Requirements Error"

    def __init__(self, message: str = error_msg) -> None:
        self.message = message
        super().__init__(self.message)


class RecommendationError(Exception):
    error_msg = "Generic Recommendation Error"

    def __init__(self, error_msg: str = error_msg) -> None:
        super().__init__(error_msg)


class RecommenderError(Exception):
    generic_msg = "Generic Recommender Error"

    def __init__(self, error_msg: str = generic_msg) -> None:
        message = f"\n{error_msg}\n"
        super().__init__(message)


class TemperatureError(Exception):
    error_msg = "Generic Temperature Error"

    def __init__(self, error_msg: str = error_msg) -> None:
        super().__init__(error_msg)


class WeatherError(Exception):
    generic_msg = "Generic Weather Error"

    def __init__(self, location, error_msg: str = generic_msg) -> None:
        message = f"\n{error_msg}\nLocation: {location}"
        super().__init__(message)


class ZipCodeError(Exception):
    generic_msg = "Generic Zip Code Error"

    def __init__(self, code: str, error_msg: str = generic_msg) -> None:
        message = f"\n{error_msg}\nCode: {code}"
        super().__init__(message)
