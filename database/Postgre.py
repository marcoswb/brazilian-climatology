from peewee import Model, CharField, IntegerField, FloatField, DateField, PrimaryKeyField, TimeField, PostgresqlDatabase

from utils.functions import get_env

# conexão com o banco
db = PostgresqlDatabase(
    get_env('DATABASE_NAME'),
    user=get_env('DATABASE_USER'),
    password=get_env('DATABASE_PASSWORD'),
    host=get_env('DATABASE_HOST'),
    port=get_env('DATABASE_POST')
)


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


class ForecastAverage(Model):
    period_day = IntegerField()
    weather_condition = CharField()
    maximum_temperature = FloatField()
    minimum_temperature = FloatField()
    ultra_violet_index = FloatField(null=True)
    id_city = IntegerField()

    class Meta:
        database = db
        table_name = 'forecast_average'

    @staticmethod
    def init():
        db.drop_tables([ForecastAverage])
        db.create_tables([ForecastAverage])


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


class Station(Model):
    id_station = PrimaryKeyField()
    name_station = CharField()
    state = CharField()
    latitude = CharField()
    longitude = CharField()

    class Meta:
        database = db
        table_name = 'station'

    @staticmethod
    def init():
        db.drop_tables([Station])
        db.create_tables([Station])


class History(Model):
    date = DateField()
    hour = TimeField()
    precipitation = FloatField(null=True)
    atmospheric_pressure = FloatField(null=True)
    maximum_atmospheric_pressure = FloatField(null=True)
    minimum_atmospheric_pressure = FloatField(null=True)
    global_radiation = FloatField(null=True)
    air_temperature = FloatField(null=True)
    temperature_dew_point = FloatField(null=True)
    maximum_temperature = FloatField(null=True)
    minimum_temperature = FloatField(null=True)
    maximum_dew_temperature = FloatField(null=True)
    minimum_dew_temperature = FloatField(null=True)
    maximum_relative_humidity = FloatField(null=True)
    minimum_relative_humidity = FloatField(null=True)
    relative_humidity_air = FloatField(null=True)
    direction_time_winds = FloatField(null=True)
    maximum_wind_speed = FloatField(null=True)
    wind_hourly_speed = FloatField(null=True)
    station_id = IntegerField()

    class Meta:
        database = db
        table_name = 'history'

    @staticmethod
    def init():
        db.drop_tables([History])
        db.create_tables([History])


class DailyAverageHistory(Model):
    date = DateField()
    precipitation = FloatField(null=True)
    atmospheric_pressure = FloatField(null=True)
    maximum_atmospheric_pressure = FloatField(null=True)
    minimum_atmospheric_pressure = FloatField(null=True)
    global_radiation = FloatField(null=True)
    air_temperature = FloatField(null=True)
    temperature_dew_point = FloatField(null=True)
    maximum_temperature = FloatField(null=True)
    minimum_temperature = FloatField(null=True)
    maximum_dew_temperature = FloatField(null=True)
    minimum_dew_temperature = FloatField(null=True)
    maximum_relative_humidity = FloatField(null=True)
    minimum_relative_humidity = FloatField(null=True)
    relative_humidity_air = FloatField(null=True)
    direction_time_winds = FloatField(null=True)
    maximum_wind_speed = FloatField(null=True)
    wind_hourly_speed = FloatField(null=True)
    station_id = IntegerField()

    class Meta:
        database = db
        table_name = 'daily_average_history'

    @staticmethod
    def init():
        db.drop_tables([DailyAverageHistory])
        db.create_tables([DailyAverageHistory])


class WeeklyAverageHistory(Model):
    init_date = DateField()
    end_date = DateField()
    precipitation = FloatField(null=True)
    atmospheric_pressure = FloatField(null=True)
    maximum_atmospheric_pressure = FloatField(null=True)
    minimum_atmospheric_pressure = FloatField(null=True)
    global_radiation = FloatField(null=True)
    air_temperature = FloatField(null=True)
    temperature_dew_point = FloatField(null=True)
    maximum_temperature = FloatField(null=True)
    minimum_temperature = FloatField(null=True)
    maximum_dew_temperature = FloatField(null=True)
    minimum_dew_temperature = FloatField(null=True)
    maximum_relative_humidity = FloatField(null=True)
    minimum_relative_humidity = FloatField(null=True)
    relative_humidity_air = FloatField(null=True)
    direction_time_winds = FloatField(null=True)
    maximum_wind_speed = FloatField(null=True)
    wind_hourly_speed = FloatField(null=True)
    station_id = IntegerField()

    class Meta:
        database = db
        table_name = 'weekly_average_history'

    @staticmethod
    def init():
        db.drop_tables([WeeklyAverageHistory])
        db.create_tables([WeeklyAverageHistory])


class MonthlyAverageHistory(Model):
    competence = DateField()
    precipitation = FloatField(null=True)
    atmospheric_pressure = FloatField(null=True)
    maximum_atmospheric_pressure = FloatField(null=True)
    minimum_atmospheric_pressure = FloatField(null=True)
    global_radiation = FloatField(null=True)
    air_temperature = FloatField(null=True)
    temperature_dew_point = FloatField(null=True)
    maximum_temperature = FloatField(null=True)
    minimum_temperature = FloatField(null=True)
    maximum_dew_temperature = FloatField(null=True)
    minimum_dew_temperature = FloatField(null=True)
    maximum_relative_humidity = FloatField(null=True)
    minimum_relative_humidity = FloatField(null=True)
    relative_humidity_air = FloatField(null=True)
    direction_time_winds = FloatField(null=True)
    maximum_wind_speed = FloatField(null=True)
    wind_hourly_speed = FloatField(null=True)
    station_id = IntegerField()

    class Meta:
        database = db
        table_name = 'monthly_average_history'

    @staticmethod
    def init():
        db.drop_tables([MonthlyAverageHistory])
        db.create_tables([MonthlyAverageHistory])
