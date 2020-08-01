from enum import Enum
from typing import Callable, Any

from peewee import *
from statbus.utils.FlaskDB import FlaskDBWrapper as FlaskDB

db_wrapper = FlaskDB()


class DBModel(db_wrapper.Model):
    """Meta model all models should parent from"""

    pass


""" Enum field hack
This isn't supported by peewee but easy enough to add
"""


class EnumField(CharField):
    """
    This class enable an Enum like field for Peewee
    """

    def __init__(self, choices: Callable, *args: Any, **kwargs: Any) -> None:
        super(CharField, self).__init__(*args, **kwargs)
        self.choices = choices
        self.max_length = 255

    def db_value(self, value: Any) -> Any:
        return value.value

    def python_value(self, value: Any) -> Any:
        return self.choices(type(list(self.choices)[0].value)(value))


class KeyTypeEnum(Enum):
    TEXT = "text"
    AMOUNT = "amount"
    TALLY = "tally"
    NESTED = "nested tally"
    ASSOCIATIVE = "associative"
