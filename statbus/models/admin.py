class Admin(BaseModel):
    ckey = CharField(primary_key=True)
    rank = CharField()

    class Meta:
        table_name = "admin"


class AdminLog(BaseModel):
    adminckey = CharField()
    adminip = IntegerField()
    datetime = DateTimeField()
    log = CharField()
    operation = CharField()
    round_id = IntegerField()
    target = CharField()

    class Meta:
        table_name = "admin_log"


class AdminRanks(BaseModel):
    can_edit_flags = IntegerField()
    exclude_flags = IntegerField()
    flags = IntegerField()
    rank = CharField(primary_key=True)

    class Meta:
        table_name = "admin_ranks"
