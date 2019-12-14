import json
import datetime
from enum import Enum

from peewee import *
from flask import url_for, request

from statbus.models.util import DBModel, EnumField


class KeyTypeEnum(Enum):
    TEXT = "text"
    AMOUNT = "amount"
    TALLY = "tally"
    NESTED = "nested tally"
    ASSOCIATIVE = "associative"


class Feedback(DBModel):
    class Meta:
        table_name = "feedback"

    id = IntegerField(unique=True)
    datetime = DateTimeField()
    round_id = IntegerField()
    key_name = CharField(32)
    version = IntegerField()
    key_type = EnumField(choices=KeyTypeEnum)
    json = CharField()

    @property
    def data(self):
        "Human readable status of the round"
        return json.loads(self.json).get("data")

    @property
    def value(self):
        mapping = {
            KeyTypeEnum.TEXT: self.text,
            KeyTypeEnum.AMOUNT: self.amount,
            KeyTypeEnum.TALLY: self.tally,
            KeyTypeEnum.ASSOCIATIVE: self.assoc,
            KeyTypeEnum.NESTED: self.data,
        }
        return mapping[self.key_type]

    @property
    def is_nested(self):
        return self.key_type != KeyTypeEnum.TEXT

    @property
    def text(self):
        return ", ".join(self.data)

    @property
    def amount(self):
        return self.data

    @property
    def tally(self):
        return self.data

    @property
    def assoc(self):
        return self.data
