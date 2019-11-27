import datetime
from flask import url_for
from peewee import *

from statbus.database.util import DBModel


class PollOption(DBModel):
    class Meta:
        table_name = "poll_option"

    id = IntegerField(unique=True)
    pollid = IntegerField()
    text = CharField()
    minval = IntegerField(null=True)
    maxval = IntegerField(null=True)
    descmin = CharField(null=True)
    descmid = CharField(null=True)
    descmax = CharField(null=True)
    default_percentage_calc = IntegerField(default=1)


class PollQuestion(DBModel):
    class Meta:
        table_name = "poll_question"

    id = IntegerField(unique=True)
    polltype = CharField()
    starttime = DateTimeField()
    endtime = DateTimeField()
    question = CharField()
    adminonly = IntegerField()
    multiplechoiceoptions = IntegerField(null=True)
    createdby_ckey = CharField(max_length=32, null=True)
    createdby_ip = IntegerField()
    dontshow = IntegerField()

    @classmethod
    def get_active(cls, limit=3):
        return cls.select().where(cls.adminonly == False, cls.dontshow == False).limit(limit)

    @property
    def poll_status(self):
        if not self.endtime:
            return "This poll doesn't end"
        time_until = abs((datetime.datetime.now() - self.endtime).days)
        if datetime.datetime.now() > self.endtime:
            return f"The poll has ended. {time_until} day(s) ago"
        else:
            return f"Time remaining: {time_until} day(s)"

    @property
    def is_hidden(self):
        return self.adminonly or self.dontshow

    @property
    def link_url(self):
        return url_for("polls.detail", poll_id=self.id)


class PollTextReply(DBModel):
    class Meta:
        table_name = "poll_textreply"

    id = IntegerField(unique=True)
    datetime = DateTimeField()
    pollid = IntegerField()
    ckey = CharField(max_length=32)
    ip = IntegerField()
    replytext = CharField(max_length=2048)
    adminrank = CharField(max_length=32, default="Player")


class PollVote(DBModel):
    class Meta:
        table_name = "poll_vote"

    id = IntegerField(unique=True)
    datetime = DateTimeField()
    pollid = IntegerField()
    optionid = IntegerField()
    ckey = CharField(max_length=32)
    ip = IntegerField()
    adminrank = CharField(max_length=32, default="Player")
    rating = IntegerField(null=True)
