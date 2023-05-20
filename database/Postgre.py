from peewee import Model, CharField, IntegerField, FloatField, DateField, PostgresqlDatabase

# conexão com o banco
db = PostgresqlDatabase('tcc_database', user='marcos', password='marcos', host='localhost', port=5432)


class City(Model):
    city = CharField()
    state = CharField()

    class Meta:
        database = db
        table_name = 'city'

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


class Forecast(Model):
    day = DateField()
    weather_condition = CharField()
    maximum_temperature = IntegerField()
    minimum_temperature = IntegerField()
    ultra_violet_index = FloatField(null=True)
    id_city = IntegerField()

    class Meta:
        database = db
        table_name = 'forecast'

    @staticmethod
    def init():
        db.drop_tables([Forecast])
        db.create_tables([Forecast])


class WeatherType(Model):
    weather_condition = CharField()
    weather_condition_description = CharField()

    class Meta:
        database = db
        table_name = 'weather_type'

    @staticmethod
    def init():
        db.drop_tables([WeatherType])
        db.create_tables([WeatherType])
