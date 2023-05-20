from peewee import Model, CharField, IntegerField, PostgresqlDatabase

# conexão com o banco
db = PostgresqlDatabase('tcc_database', user='marcos', password='marcos', host='localhost', port=5432)


class City(Model):
    city = CharField()
    state = CharField()

    class Meta:
        database = db

    @staticmethod
    def init():
        db.drop_tables([City])
        db.create_tables([City])


class PositionCity(Model):
    latitude = CharField()
    longitude = CharField()
    id_city = IntegerField()

    class Meta:
        database = db
        table_name = 'position_city'

    @staticmethod
    def init():
        db.drop_tables([PositionCity])
        db.create_tables([PositionCity])
