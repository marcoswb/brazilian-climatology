from peewee import SQL

from database.Postgre import Forecast, ForecastAverage
from database.Postgre import History, DailyAverageHistory, WeeklyAverageHistory, MonthlyAverageHistory


class Database:

    @staticmethod
    def get_history_station(station, init_date, times):
        result = History.select().where(SQL(f"station_id = '{station}'") &
                                        SQL(f"date >= '{init_date}'") &
                                        SQL(f"hour in {times}")).order_by(History.date, History.hour).dicts()
        return result

    @staticmethod
    def get_history_state(state, init_date, times):
        result = History.select().where(SQL(f"station_id in (SELECT sub.id_station from station as sub where sub.state = '{state}')") &
                                        SQL(f"date >= '{init_date}'") &
                                        SQL(f"hour in {times}")).order_by(History.date, History.hour).dicts()
        return result

    @staticmethod
    def get_daily_average_history_station(station, init_date):
        result = DailyAverageHistory.select().where(SQL(f"station_id = '{station}'") &
                                                    SQL(f"date >= '{init_date}'")).order_by(DailyAverageHistory.date).dicts()
        return result

    @staticmethod
    def get_weekly_average_history_station(station, init_date):
        result = WeeklyAverageHistory.select().where(SQL(f"station_id = '{station}'") &
                                                     SQL(f"init_date >= '{init_date}'")).order_by(WeeklyAverageHistory.init_date).dicts()
        return result

    @staticmethod
    def get_monthly_average_history_station(station, init_date):
        result = MonthlyAverageHistory.select().where(SQL(f"station_id = '{station}'") &
                                                      SQL(f"competence >= '{init_date}'")).order_by(MonthlyAverageHistory.competence).dicts()
        return result

    @staticmethod
    def get_daily_average_history_state(state, init_date):
        result = DailyAverageHistory.select().where(SQL(f"station_id in (SELECT sub.id_station from station as sub where sub.state = '{state}')") &
                                                    SQL(f"date >= '{init_date}'")).order_by(DailyAverageHistory.date).dicts()
        return result

    @staticmethod
    def get_weekly_average_history_state(state, init_date):
        result = WeeklyAverageHistory.select().where(SQL(f"station_id in (SELECT sub.id_station from station as sub where sub.state = '{state}')") &
                                                     SQL(f"init_date >= '{init_date}'")).order_by(WeeklyAverageHistory.init_date).dicts()
        return result

    @staticmethod
    def get_monthly_average_history_state(state, init_date):
        result = MonthlyAverageHistory.select().where(SQL(f"station_id in (SELECT sub.id_station from station as sub where sub.state = '{state}')") &
                                                      SQL(f"competence >= '{init_date}'")).order_by(MonthlyAverageHistory.competence).dicts()
        return result

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
