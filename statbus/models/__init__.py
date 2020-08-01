# empty file

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
    game_mode_result = db.Column(db.String(96), nullable=True)
    end_state = db.Column(db.String(96), nullable=True)
    map_name = db.Column(db.String(32), nullable=True)
    server_ip = db.Column(db.Integer)
    server_port = db.Column(db.Integer)
    commit_hash = db.Column(db.String(40), nullable=True)

    feedback = db.relationship(
        "Feedback", backref="round", lazy="dynamic", uselist=True
    )
    connections = db.relationship(
        "Connection", backref="round", lazy="dynamic", uselist=True
    )
    deaths = db.relationship("Death", backref="round", lazy="dynamic", uselist=True)

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
            "testmerged_prs": self.testmerged_prs,
            "round_stats": self.round_stats,
            "balance": self.balance,
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
    def testmerged_prs(self):
        fb = self.feedback.filter(Feedback.key_name == "testmerged_prs").first()
        if not fb:
            return {}
        return {v["number"]: v for _, v in fb.value.items()}

    @property
    def ship_name(self):
        fb = self.feedback.filter(Feedback.key_name == "ship_map").first()
        if not fb:
            return "UNSET"
        return fb.data[0]

    @property
    def round_stats(self):
        fb = self.feedback.filter(Feedback.key_name == "round_statistics").first()
        if not fb:
            return {}
        return fb.value

    @property
    def balance(self):
        fb = self.feedback.filter(Feedback.key_name == "balance").first()
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
            return datetime.timedelta()  # empty delta
        return self.end_datetime - self.start_datetime


class Connection(db.Model):
    __tablename__ = "connection_log"
    id = db.Column(db.Integer, primary_key=True)
    ckey = db.Column(db.String(32), nullable=True)
    computerid = db.Column(db.String(96), nullable=True)
    datetime = db.Column(db.DateTime)
    ip = db.Column(db.Integer)
    round_id = db.Column(db.Integer, db.ForeignKey("round.id"), nullable=False)
    server_ip = db.Column(db.Integer)
    server_port = db.Column(db.Integer)

    def to_object(self):
        return {"ckey": self.ckey}


class Death(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brainloss = db.Column(db.Integer)
    bruteloss = db.Column(db.Integer)
    byondkey = db.Column(db.String(96))
    cloneloss = db.Column(db.Integer)
    fireloss = db.Column(db.Integer)
    job = db.Column(db.String(96))
    lakey = db.Column(db.String(96), nullable=True)
    laname = db.Column(db.String(96), nullable=True)
    last_words = db.Column(db.String(255), nullable=True)
    mapname = db.Column(db.String(96))
    name = db.Column(db.String(96))
    oxyloss = db.Column(db.Integer)
    pod = db.Column(db.String(96))
    round_id = db.Column(db.Integer, db.ForeignKey("round.id"), nullable=False)
    server_ip = db.Column(db.Integer)
    server_port = db.Column(db.Integer)
    special = db.Column(db.String(96), nullable=True)
    staminaloss = db.Column(db.Integer)
    suicide = db.Column(db.Integer)
    tod = db.Column(db.DateTime)
    toxloss = db.Column(db.Integer)
    x_coord = db.Column(db.Integer)
    y_coord = db.Column(db.Integer)
    z_coord = db.Column(db.Integer)

    def to_object(self):
        return {
            "id": self.id,
            "brainloss": self.brainloss,
            "bruteloss": self.bruteloss,
            # "byondkey": self.byondkey,
            "cloneloss": self.cloneloss,
            "fireloss": self.fireloss,
            "job": self.job,
            # "lakey": self.lakey,
            # "laname": self.laname,
            "last_words": self.last_words,
            "mapname": self.mapname,
            "name": self.name,
            "oxyloss": self.oxyloss,
            "pod": self.pod,
            "round_id": self.round_id,
            # "special": self.special,
            "staminaloss": self.staminaloss,
            "suicide": self.suicide,
            "tod": self.tod,
            "toxloss": self.toxloss,
            "x_coord": self.x_coord,
            "y_coord": self.y_coord,
            "z_coord": self.z_coord,
        }


class KeyTypeEnum(Enum):
    text = "text"
    amount = "amount"
    tally = "tally"
    nested = "nested tally"
    associative = "associative"


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
            KeyTypeEnum.text: self.text,
            KeyTypeEnum.amount: self.amount,
            KeyTypeEnum.tally: self.tally,
            KeyTypeEnum.associative: self.assoc,
            KeyTypeEnum.nested: self.data,
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


class PollQuestion(db.Model):
    __tablename__ = "poll_question"

    id = db.Column(db.Integer, primary_key=True)
    polltype = db.Column(db.Text)
    starttime = db.Column(db.DateTime)
    endtime = db.Column(db.DateTime)
    question = db.Column(db.Text)
    adminonly = db.Column(db.Integer)
    multiplechoiceoptions = db.Column(db.Integer, nullable=True)
    createdby_ckey = db.Column(db.Text, nullable=True)
    createdby_ip = db.Column(db.Integer)
    dontshow = db.Column(db.Integer)

    text_replies = db.relationship(
        "PollTextReply", backref="question", lazy="dynamic", uselist=True
    )
    votes = db.relationship(
        "PollVote", backref="question", lazy="dynamic", uselist=True
    )
    options = db.relationship(
        "PollOption", backref="question", lazy="dynamic", uselist=True
    )

    def to_object(self):
        return {
            "id": self.id,
            "polltype": self.polltype,
            "starttime": self.starttime,
            "endtime": self.endtime,
            "question": self.question,
            "multiplechoiceoptions": self.multiplechoiceoptions,
            "createdby_ckey": self.createdby_ckey,
        }

    @classmethod
    def get_active(cls, limit=3):
        return (
            cls.query()
            .filter(
                cls.adminonly == False,
                cls.dontshow == False,
                cls.endtime > datetime.datetime.now(),
            )
            .limit(limit)
        )

    @property
    def status(self):
        if not self.endtime:
            return "FOREVER"
        if datetime.datetime.now() > self.endtime:
            return "ENDED"
        else:
            return "ONGOING"

    @property
    def status_text(self):
        time_until = (
            abs((datetime.datetime.now() - self.endtime).days) if self.endtime else None
        )
        return {
            "FOREVER": "This poll doesn't end",
            "ENDED": f"The poll has ended. {time_until} day(s) ago",
            "ONGOING": f"Time remaining: {time_until} day(s)",
        }[self.status]

    @property
    def total_votes(self):
        return self.votes.count()

    @property
    def is_hidden(self):
        return self.adminonly or self.dontshow


class PollTextReply(db.Model):
    __tablename__ = "poll_textreply"

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    pollid = db.Column(db.Integer, db.ForeignKey("poll_question.id"), nullable=False)
    ckey = db.Column(db.String(32))
    ip = db.Column(db.Integer)
    replytext = db.Column(db.Text)
    adminrank = db.Column(db.String(32), default="Player")


class PollVote(db.Model):
    __tablename__ = "poll_vote"

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    pollid = db.Column(db.Integer, db.ForeignKey("poll_question.id"), nullable=False)
    optionid = db.Column(db.Integer, db.ForeignKey("poll_option.id"), nullable=False)
    ckey = db.Column(db.String(32))
    ip = db.Column(db.Integer)
    adminrank = db.Column(db.String(32), default="Player")
    rating = db.Column(db.Integer, nullable=True)


class PollOption(db.Model):
    __tablename__ = "poll_option"

    id = db.Column(db.Integer, primary_key=True)
    pollid = db.Column(db.Integer, db.ForeignKey("poll_question.id"), nullable=False)
    text = db.Column(db.Text)
    minval = db.Column(db.Integer, nullable=True)
    maxval = db.Column(db.Integer, nullable=True)
    descmin = db.Column(db.Text, nullable=True)
    descmid = db.Column(db.Text, nullable=True)
    descmax = db.Column(db.Text, nullable=True)
    default_percentage_calc = db.Column(db.Integer, default=1)


class Player(db.Model):
    __tablename__ = "player"
    ckey = db.Column(db.String(32), primary_key=True)
    byond_key = db.Column(db.String(32))
    firstseen = db.Column(db.DateTime)
    firstseen_round_id = db.Column(
        db.Integer, db.ForeignKey("round.id"), nullable=False
    )
    lastseen = db.Column(db.DateTime)
    lastseen_round_id = db.Column(db.Integer, db.ForeignKey("round.id"), nullable=False)
    ip = db.Column(db.Integer)
    computerid = db.Column(db.String(32))
    lastadminrank = db.Column(db.String(32))
    accountjoindate = db.Column(db.DateTime)
    flags = db.Column(db.Integer)


class Ban(db.Model):
    __tablename__ = "player"
    a_ckey = db.Column(db.String(32))
    a_computerid = db.Column(db.String(32))
    a_ip = db.Column(db.Integer)
    adminwho = db.Column(db.String(32))
    applies_to_admins = db.Column(db.Integer, default=0)
    bantime = db.Column(db.DateTime)
    ckey = db.Column(db.String(32), nullable=True)
    computerid = db.Column(db.String(32), nullable=True)
    edits = db.Column(db.String(32), nullable=True)
    expiration_time = db.Column(db.DateTime, nullable=True)
    ip = db.Column(db.Integer, nullable=True)
    reason = db.Column(db.String(32))
    role = db.Column(db.String(32), nullable=True)
    round_id = db.Column(db.Integer)
    server_ip = db.Column(db.Integer)
    server_port = db.Column(db.Integer)
    unbanned_ckey = db.Column(db.String(32), nullable=True)
    unbanned_computerid = db.Column(db.String(32), nullable=True)
    unbanned_datetime = db.Column(db.Integer, nullable=True)
    unbanned_ip = db.Column(db.Integer, nullable=True)
    unbanned_round_id = db.Column(db.Integer, nullable=True)
    who = db.Column(db.String(32))
