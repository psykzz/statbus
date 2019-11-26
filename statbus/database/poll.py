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
