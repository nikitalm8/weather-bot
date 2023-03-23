import yaml


class AutoConfig(dict):

    def __init__(self, **kwargs):

        for key, value in kwargs.items():

            if isinstance(value, dict):

                setattr(self, key, AutoConfig(**value))

            else:

                setattr(self, key, value)

    def __repr__(self):

        return str(self.__dict__)


def load_config(path: str) -> dict:
    """Load config from yaml file."""

    with open(path, "r") as file:

        config_as_json = yaml.safe_load(file)

    return AutoConfig(**config_as_json)