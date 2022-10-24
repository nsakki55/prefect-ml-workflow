from enum import Enum, auto


class InvalidEnvironmentError(Exception):
    """system environment should be set in Environment Enum values."""

    pass


class Environment(Enum):
    DEVELOP = auto()
    PRODUCTION = auto()

    @staticmethod
    def from_str(environment: str):
        if environment == "develop":
            return Environment.DEVELOP
        if environment == "production":
            return Environment.PRODUCTION
        raise InvalidEnvironmentError(f"{environment} is inappropriate environment")
