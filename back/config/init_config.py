from configparser import ConfigParser
from termcolor import colored

import os

config_path = "config/config.ini"
config_parser = ConfigParser()

DEBUG_COLOR = "light_blue"
DEBUG_SECONDARY_COLOR = "blue"
ERROR_COLOR = "light_red"
SUCCESS_COLOR = "green"

# Default config
config = {
    "ARANGODB": {
        "HOST": None,
        "PORT": None,
        "DATABASE": None,
        "USER": None,
        "PASSWORD": None,
    },
}

# Env vars mapping
TYPES_MAPPING = {
    "ARANGODB": {
        "HOST": str,
        "PORT": int,
        "DATABASE": str,
        "USER": str,
        "PASSWORD": str,
    },
}

# Env vars mapping
ENV_VAR_MAPPING = {
    "ARANGODB": {
        "HOST": "MUSEUMGO_ARANGODB_HOST",
        "PORT": "MUSEUMGO_ARANGODB_PORT",
        "DATABASE": "MUSEUMGO_ARANGODB_DATABASE",
        "USER": "MUSEUMGO_ARANGODB_USER",
        "PASSWORD": "MUSEUMGO_ARANGODB_PASSWORD",
    },
}


def get_config_value(section, key, config_parser):
    # Return the value of the key in the section of the config_parser
    # Or return the ENV_VAR if it exists

    value = None
    ENV_VAR = ENV_VAR_MAPPING[section][key]

    # Get the value from the config file
    if section in config_parser and key in config_parser[section]:
        value = config_parser[section][key]

    # Get the value from the environment variables
    if ENV_VAR in os.environ:
        value = os.environ[ENV_VAR]

    if value is None:
        print(
            " - Missing "
            + colored(section, DEBUG_SECONDARY_COLOR)
            + " / "
            + colored(key, DEBUG_SECONDARY_COLOR)
            + " in config or in "
            + colored(ENV_VAR, DEBUG_SECONDARY_COLOR)
            + " env var, using default"
        )

        raise ValueError(
            "Missing "
            + section
            + " / "
            + key
            + " in config/config.ini or in "
            + ENV_VAR
            + " env var"
        )

    return value


def set_config_value(section, key, value):
    global config

    if section in config and key in config[section]:
        if config[section][key] != value:
            # The default value is different from the one in the config file
            config[section][key] = value

            print(
                " - Set "
                + colored(section, DEBUG_COLOR)
                + " / "
                + colored(key, DEBUG_COLOR)
            )


def init_config():
    global config

    print("\nInitializing config...")

    # Read the config file
    config_parser.read(config_path)

    for section in config.keys():
        # Deal with boolean, integer and string values
        for key in config[section].keys():
            # Get the value from the config file or the environment variables
            value = get_config_value(section, key, config_parser)

            # Set the value in the config according to its type
            value_type = TYPES_MAPPING[section][key]
            if value_type == bool:
                value = value == "true"
            elif value_type == int:
                try:
                    value = int(value)
                except ValueError:
                    raise ValueError(
                        " - "
                        + colored(section, ERROR_COLOR)
                        + " / "
                        + colored(key, ERROR_COLOR)
                        + " should be an integer"
                    )
            elif value_type == str:
                value = str(value)

            set_config_value(section, key, value)


def get_config():
    if config["ARANGODB"]["HOST"] is None:
        init_config()
    return config
