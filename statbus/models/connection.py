import json
import datetime
from enum import Enum

from peewee import *
from flask import url_for, request

from statbus.models.util import DBModel, EnumField


class Connection(DBModel):
    class Meta:
        table_name = "connection_log"

    id = IntegerField(unique=True)
    datetime = DateTimeField()
    server_ip = IntegerField()
    server_port = IntegerField()
    round_id = IntegerField()
    ckey = CharField()
    ip = IntegerField()
    computerid = CharField()

    @property
    def round(self):
        return Round.where(Round.id == self.round_id)
