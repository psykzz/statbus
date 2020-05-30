import json
import datetime
from enum import Enum

from flask import url_for, request

from statbus.ext import db


class Round(db.Model):
    __tablename__ = "round"
    id = db.Column(db.Integer, primary_key=True)
    initialize_datetime = db.Column(db.DateTime)
    shutdown_datetime = db.Column(db.DateTime, nullable=True)
    start_datetime = db.Column(db.DateTime, nullable=True)
    end_datetime = db.Column(db.DateTime, nullable=True)
    game_mode = db.Column(db.String(32), nullable=True)
    game_mode_result = db.Column(db.String(64), nullable=True)
    end_state = db.Column(db.String(64), nullable=True)
    map_name = db.Column(db.String(32), nullable=True)
    server_ip = db.Column(db.Integer)
    server_port = db.Column(db.Integer)
    commit_hash = db.Column(db.String(40), nullable=True)

    feedback = db.relationship(
        "Feedback", backref="round", lazy="dynamic", uselist=True
    )

    def __repr__(self):
        return f"<Round id={self.id} />"

    def to_object(self):
        return {
            "id": self.id,
            "initialize_datetime": self.initialize_datetime,
            "start_datetime": self.start_datetime,
            "shutdown_datetime": self.shutdown_datetime,
            "end_datetime": self.end_datetime,
            "commit_hash": self.commit_hash,
            "game_mode": self.game_mode,
            "game_mode_result": self.game_mode_result,
            "end_state": self.end_state,
            "map_name": self.map_name,
            "ship_name": self.ship_name,
        }

    @classmethod
    def get_recent(cls, days=7, limit=5):
        today = datetime.date.today()
        since = today - datetime.timedelta(days=days)
        return (
            cls.select()
            .where(cls.end_datetime > since, cls.start_datetime, cls.end_datetime)
            .order_by(cls.id.desc())
            .limit(limit)
        )

    @property
    def merged_prs(self):
        fb = self.feedback.filter(Round.feedback.key_name == "testmerged_prs").first()
        if not fb:
            return {}
        return fb.value

    @property
    def ship_name(self):
        fb = self.feedback.filter(Round.feedback.key_name == "ship_map").first()
        if not fb:
            return "UNSET"
        return fb.data[0]

    @property
    def round_stats(self):
        fb = self.feedback.filter(Round.feedback.key_name == "round_statistics").first()
        if not fb:
            return {}
        return fb.value

    @property
    def unique_players(self):
        return (
            Connection.select()
            .where(Connection.round_id == self.id)
            .group_by(Connection.ckey)
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
    def link_url(self):
        return url_for("rounds.detail", round_id=self.id)

    @property
    def duration(self):
        if not self.end_datetime or not self.start_datetime:
            return datetime.timedelta()
        return self.end_datetime - self.start_datetime


class KeyTypeEnum(Enum):
    TEXT = "text"
    AMOUNT = "amount"
    TALLY = "tally"
    NESTED = "nested tally"
    ASSOCIATIVE = "associative"


class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=True)
    round_id = db.Column(db.Integer, db.ForeignKey("round.id"), nullable=False)
    key_name = db.Column(db.String(32))
    version = db.Column(db.Integer)
    key_type = db.Column(db.Enum(KeyTypeEnum))
    json = db.Column(db.Text())

    @property
    def data(self):
        "Human readable status of the round"
        return json.loads(self.json).get("data")

    @property
    def value(self):
        return {
            KeyTypeEnum.TEXT: self.text,
            KeyTypeEnum.AMOUNT: self.amount,
            KeyTypeEnum.TALLY: self.tally,
            KeyTypeEnum.ASSOCIATIVE: self.assoc,
            KeyTypeEnum.NESTED: self.data,
        }[self.key_type]

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
