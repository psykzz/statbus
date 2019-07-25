from enum import Enum
from typing import Callable, Any

from peewee import *
from playhouse.flask_utils import FlaskDB

db_wrapper = FlaskDB()

""" Enum field hack
This isn't supported by peewee but easy enough to add
"""


class KeyTypeEnum(Enum):
    TEXT = "text"
    AMOUNT = "amount"
    TALLY = "tally"
    NESTED = "nested tally"
    ASSOCIATIVE = "associative"


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


"""
MariaDB [tgmc]> describe feedback;
+----------+------------------------------------------------------------+------+-----+---------+----------------+
| Field    | Type                                                       | Null | Key | Default | Extra          |
+----------+------------------------------------------------------------+------+-----+---------+----------------+
| id       | int(11) unsigned                                           | NO   | PRI | NULL    | auto_increment |
| datetime | datetime                                                   | NO   |     | NULL    |                |
| round_id | int(11) unsigned                                           | NO   |     | NULL    |                |
| key_name | varchar(32)                                                | NO   |     | NULL    |                |
| version  | tinyint(3) unsigned                                        | NO   |     | NULL    |                |
| key_type | enum('text','amount','tally','nested tally','associative') | NO   |     | NULL    |                |
| json     | longtext                                                   | NO   |     | NULL    |                |
+----------+------------------------------------------------------------+------+-----+---------+----------------+
"""


class Feedback(db_wrapper.Model):
    id = IntegerField(unique=True)
    datetime = DateTimeField()
    round_id = IntegerField()
    key_name = CharField(32)
    version = IntegerField()
    key_type = EnumField(choices=KeyTypeEnum)
    json = CharField()
