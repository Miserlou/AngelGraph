from peewee import *

DATABASE = 'angels.db'
database = SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta:
        database = database

class AngelEvent(BaseModel):
    al_id = CharField()
    event_type = CharField()
    username = CharField()
    target = CharField()
    datetime = DateTimeField()