class Ban(BaseModel):
    a_ckey = CharField()
    a_computerid = CharField()
    a_ip = IntegerField()
    adminwho = CharField()
    applies_to_admins = IntegerField(constraints=[SQL("DEFAULT 0")])
    bantime = DateTimeField()
    ckey = CharField(null=True)
    computerid = CharField(null=True)
    edits = TextField(null=True)
    expiration_time = DateTimeField(null=True)
    ip = IntegerField(null=True)
    reason = CharField()
    role = CharField(null=True)
    round_id = IntegerField()
    server_ip = IntegerField()
    server_port = IntegerField()
    unbanned_ckey = CharField(null=True)
    unbanned_computerid = CharField(null=True)
    unbanned_datetime = DateTimeField(null=True)
    unbanned_ip = IntegerField(null=True)
    unbanned_round_id = IntegerField(null=True)
    who = CharField()

    class Meta:
        table_name = "ban"
        indexes = (
            (
                (
                    "bantime",
                    "a_ckey",
                    "applies_to_admins",
                    "unbanned_datetime",
                    "expiration_time",
                ),
                False,
            ),
            (
                (
                    "ckey",
                    "ip",
                    "computerid",
                    "role",
                    "unbanned_datetime",
                    "expiration_time",
                ),
                False,
            ),
            (("ckey", "role", "unbanned_datetime", "expiration_time"), False),
        )
