import json
import datetime
from enum import Enum

from peewee import *
from flask import url_for, request

from statbus.models.message import Message
from statbus.models.connection import Connection
from statbus.models.round import Round
from statbus.models.util import DBModel, EnumField


class Player(DBModel):
    class Meta:
        table_name = "player"

    ckey = CharField(primary_key=True, unique=True)
    byond_key = CharField()
    firstseen = DateTimeField()
    firstseen_round_id = IntegerField()
    lastseen = DateTimeField()
    lastseen_round_id = IntegerField()
    ip = IntegerField()
    computerid = IntegerField()
    lastadminrank = CharField()
    accountjoindate = DateTimeField()
    flags = IntegerField()

    @property
    def rounds(self):
        return (
            Round.select()
            .join(Connection, on=(Connection.round_id == Round.id))
            .where(Connection.ckey == self.ckey)
            .order_by(Round.id.desc())
            .limit(10)
        )

    @property
    def notes(self):
        return (
            Message.select()
            .join(Player, on=(Player.ckey == Message.targetckey))
            .where(Message.targetckey == self.ckey)
            .order_by(Message.id.desc())
            .limit(10)
        )
