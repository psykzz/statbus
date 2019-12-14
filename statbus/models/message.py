import json
import datetime
from enum import Enum

from peewee import *
from flask import url_for, request

from statbus.models.connection import Connection
from statbus.models.round import Round
from statbus.models.util import DBModel, EnumField


class Message(DBModel):
    class Meta:
        table_name = "messages"

    id = IntegerField(primary_key=True, unique=True)
    type = CharField()
    targetckey = CharField()
    adminckey = CharField()
    text = CharField()
    timestamp = DateTimeField()
    server = CharField()
    server_ip = IntegerField()
    server_port = IntegerField()
    round_id = IntegerField()
    secret = CharField()
    expire_timestamp = DateTimeField(null=True)
    severity = CharField()
    lasteditor = CharField()
    edits = CharField()
    deleted = IntegerField()
