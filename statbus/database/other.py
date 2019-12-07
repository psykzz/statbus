import json
import datetime
from enum import Enum

from peewee import *
from flask import url_for, request

from statbus.database.util import DBModel, EnumField


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


class Round(DBModel):
    class Meta:
        table_name = "round"

    id = IntegerField(unique=True)
    initialize_datetime = DateTimeField()
    start_datetime = DateTimeField(null=True)
    shutdown_datetime = DateTimeField(null=True)
    end_datetime = DateTimeField(null=True)
    server_ip = IntegerField()
    server_port = SmallIntegerField()
    commit_hash = CharField(max_length=40, null=True)
    game_mode = CharField(max_length=32, null=True)
    game_mode_result = CharField(max_length=64, null=True)
    end_state = CharField(max_length=64, null=True)
    map_name = CharField(max_length=32, null=True)

    @classmethod
    def get_recent(cls, days=7, limit=5):
        today = datetime.date.today()
        since = today - datetime.timedelta(days=days)
        return (
            cls.select()
            .where(cls.end_datetime > since)
            .order_by(cls.id.desc())
            .limit(limit)
        )

    @property
    def merged_prs(self):
        fb = self.feedback.where(Feedback.key_name == "testmerged_prs").first()
        if not fb:
            return "UNSET"
        return fb.value

    @property
    def ship_name(self):
        fb = self.feedback.where(Feedback.key_name == "ship_map").first()
        if not fb:
            return "UNSET"
        return fb.data[0]

    @property
    def unique_players(self):
        return (
            Connection.select()
            .where(Connection.round_id == self.id)
            .group_by(Connection.ckey)
            .count()
        )

    @property
    def status(self):
        "Human readable status of the round"
        if not self.start_datetime:
            return "Initializing"
        if not self.end_datetime:
            return "Ongoing"
        return "Ended"

    @property
    def feedback(self):
        return Feedback.select().where(Feedback.round_id == self.id)

    @property
    def link_url(self):
        return url_for("rounds.detail", round_id=self.id)

    @property
    def duration(self):
        if not self.end_datetime or not self.start_datetime:
            return datetime.timedelta()
        return self.end_datetime - self.start_datetime


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
