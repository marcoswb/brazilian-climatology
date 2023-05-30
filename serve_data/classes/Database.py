from peewee import SQL

from database.Postgre import Forecast, ForecastAverage


class Database:

    @staticmethod
    def get_forecast_city(city, init_date, end_date):
        result = Forecast.select().where(SQL(f"id_city = '{city}'") &
                                         SQL(f"day >= '{init_date}'") &
                                         SQL(f"day <= '{end_date}'")).order_by(Forecast.day).dicts()
        return result

    @staticmethod
    def get_forecast_state(state, init_date, end_date):
        result = Forecast.select().where(SQL(f"id_city in (select sub.id from city as sub where sub.state = '{state}')") &
                                         SQL(f"day >= '{init_date}'") &
                                         SQL(f"day <= '{end_date}'")).order_by(Forecast.id_city, Forecast.day).dicts()
        return result

    @staticmethod
    def get_average_forecast_city(city, period_day):
        result = ForecastAverage.select().where(SQL(f"id_city = '{city}'") &
                                                SQL(f"period_day = '{period_day}'")).dicts()
        return result

    @staticmethod
    def get_average_forecast_state(state, period_day):
        result = ForecastAverage.select().where(SQL(f"id_city in (select sub.id from city as sub where sub.state = '{state}')") &
                                                SQL(f"period_day = '{period_day}'")).dicts()
        return result
