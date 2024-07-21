import os
from typing import get_type_hints


class BaseConfig:
    """
    Base class for any configuration. Can read values from environment and contains default constructor.
    """

    def __init__(self, **kwargs):
        type_hints = get_type_hints(self.__class__)
        for name, typ in type_hints.items():
            if name in kwargs:
                value = kwargs[name]
                if value is not None:
                    if typ == int:
                        value = int(value)
                    elif typ == bool:
                        value = value if isinstance(value, bool) else value.lower() in ['true', '1', 'yes']
                    elif typ == str | None:
                        value = value if value != 'None' else None
                setattr(self, name, value)
            else:
                setattr(self, name, getattr(self.__class__, name, None))

    @classmethod
    def from_env(cls):
        # Extract the prefix from the class name
        prefix = cls.__name__.replace('Config', '').upper() + '_'

        # Create a dictionary to hold the configuration values
        config_values = {}
        type_hints = get_type_hints(cls)

        # Iterate through all class annotations
        for name, typ in type_hints.items():
            env_value = os.getenv(prefix + name.upper())
            if env_value is not None:
                if typ == int:
                    env_value = int(env_value)
                elif typ == bool:
                    env_value = env_value.lower() in ['true', '1', 'yes']
                elif typ == str | None:
                    env_value = env_value if env_value != 'None' else None
                config_values[name] = env_value
            else:
                config_values[name] = getattr(cls, name)

        return cls(**config_values)
