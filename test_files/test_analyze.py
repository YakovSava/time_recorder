from time import strptime, strftime, mktime, struct_time, gmtime, time
from typing import List

times = [
    {'discovers': [], 'connects': []},
    {'discovers': ['09:52 22.11.23', '10:04 22.11.23'], 'connects': [
        '20:38 01.12.23', '10:04 22.11.23', '13:34 22.11.23', '17:04 22.11.23']},
    {'discovers': [], 'connects': []},
    {'discovers': [], 'connects': []},
    {'discovers': [], 'connects': []},
    {'discovers': ['20:01 21.11.23'], 'connects': [
        '20:01 21.11.23', '11:55 01.12.23']},
    {'discovers': ['08:56 01.12.23'], 'connects': [
        '08:56 01.12.23', '13:18 01.12.23']},
    {'discovers': ['09:06 01.12.23'], 'connects': [
        '09:07 01.12.23', '13:14 01.12.23']},
    {'discovers': ['09:07 01.12.23', '09:45 01.12.23', '10:37 01.12.23', '11:07 01.12.23', '12:13 01.12.23', '13:14 01.12.23', '13:14 01.12.23', '13:40 01.12.23', '13:40 01.12.23', '13:41 01.12.23'], 'connects': [
        '09:07 01.12.23', '10:23 01.12.23', '10:24 01.12.23', '11:07 01.12.23', '12:12 01.12.23', '13:14 01.12.23', '13:14 01.12.23', '13:40 01.12.23', '13:40 01.12.23', '13:40 01.12.23', '13:41 01.12.23', '13:41 01.12.23']},
    {'discovers': ['09:07 01.12.23'], 'connects': ['09:07 01.12.23', '12:20 01.12.23', '12:22 01.12.23', '12:24 01.12.23', '12:27 01.12.23', '12:29 01.12.23', '13:13 01.12.23',
                                                   '13:14 01.12.23', '13:15 01.12.23', '13:17 01.12.23', '13:19 01.12.23', '13:21 01.12.23', '13:25 01.12.23', '13:26 01.12.23', '13:37 01.12.23', '13:41 01.12.23', '13:43 01.12.23']},
    {'discovers': ['09:09 01.12.23'], 'connects': ['09:09 01.12.23',
                                                   '12:39 01.12.23', '13:25 01.12.23', '13:22 22.11.23', '16:52 22.11.23']},
    {'discovers': ['14:03 01.12.23', '20:45 21.11.23', '15:17 27.11.23'], 'connects': [
        '14:03 01.12.23', '20:45 21.11.23', '20:45 21.11.23', '15:17 27.11.23']},
]

# 9 часов 7 минут


def _sort_st(sts: list[struct_time]) -> list[struct_time]:
    return sorted(sts, key=lambda x: mktime(x))



def _get_minimal_st(sts: list[struct_time]) -> struct_time:
    return _sort_st(sts)[-1]


def _get_maximal_st(sts: list[struct_time]) -> struct_time:
    return _sort_st(sts)[0]


def _str_to_st(string: str) -> struct_time:
    return strptime(string, "%H:%M %d.%m.%y")


def _liststr_to_listst(liststr: list[str]) -> list[struct_time]:
    return list(map(_str_to_st, liststr))


def _get_date_of_day(dates: list[struct_time], day: struct_time) -> list[struct_time]:
    return list(
        filter(
            lambda x: ((x.tm_mday == day.tm_mday) and (
                x.tm_mon == day.tm_mon) and (x.tm_year == day.tm_year)),
            dates
        )
    )


def _get_minimal_time_on_day(dates: list[struct_time], day: struct_time) -> struct_time:
    return _get_minimal_st(
        _get_date_of_day(dates, day)
    )


def _get_maximal_time_on_day(dates: list[struct_time], day: struct_time) -> struct_time:
    return _get_maximal_st(
        _get_date_of_day(dates, day)
    )


def analyze(data: dict) -> dict:
    """
    Return:
            {
                    "day.month.year": 12 // Integer. Count of hours of job worker
            }
    """
    try:
        ...
    except Exception as ex:
        print(ex)
        return {}
