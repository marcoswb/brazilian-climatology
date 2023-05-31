from datetime import date, time

from utils.functions import *


class FormatData:

    @staticmethod
    def format_line(dict_line, *columns_search):
        formated_line = {}
        values_search = []
        for key, value in dict_line.items():
            if isinstance(value, date):
                value = value.strftime('%d/%m/%Y')
            elif isinstance(value, time):
                value = value.strftime('%H:%M:%S')

            if columns_search:
                if key in columns_search:
                    values_search.append(value)

            formated_line[key] = value

        result = formated_line
        if columns_search:
            result = [formated_line]
            result.extend(values_search)

        return result

    @staticmethod
    def format_times_to_query(list_times):
        return "('"+"','".join([format_int_to_time(hour) for hour in list_times])+"')"

    @staticmethod
    def format_times_to_response(list_times):
        return [format_int_to_time(hour) for hour in list_times]
