import json
import datetime
from enum import Enum

from peewee import *
from flask import url_for, request

from statbus.models.util import DBModel, EnumField


class Connection(DBModel):
    ckey = CharField(null=True)
    computerid = CharField(null=True)
    datetime = DateTimeField(null=True)
    ip = IntegerField()
    round_id = IntegerField()
    server_ip = IntegerField()
    server_port = IntegerField()

    class Meta:
        table_name = "connection_log"

    @property
    def round(self):
        return Round.where(Round.id == self.round_id)
