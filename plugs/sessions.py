import re
import datetime

from os.path import exists
from time import strptime, strftime, struct_time,\
    mktime


def _sort_st(sts: list[struct_time]):
    return sorted(sts, key=lambda x: mktime(x))


def _str_to_st(string: str) -> struct_time:
    return strptime(string, "%H:%M %d.%m.%y")


def _get_date_of_day(dates: list[struct_time], day: struct_time) -> list[struct_time]:
    return list(
        filter(
            lambda x: ((x.tm_mday == day.tm_mday) and (
                x.tm_mon == day.tm_mon) and (x.tm_year == day.tm_year)),
            dates
        )
    )

def _rm_repit_times(cons: list[struct_time], discs: list[struct_time]) -> list[list[struct_time], list[struct_time]]:
    connects = []
    disconnects = []
    for con in cons:
        if con not in connects:
            connects.append(con)

    for disc in discs:
        if (disc not in disconnects) and (disc not in connects):
            disconnects.append(disc)

    return [connects, disconnects]


def _get_all_days(dates: list[struct_time]) -> list[str]:
    days = []
    for date in dates:
        day = strftime("%d.%m.%y", date)
        if day not in days:
            days.append(day)
    return days


def _get_all_days_on_dict(times: dict) -> list[struct_time]:
    time = []
    for timename in times.keys():
        _t = _get_all_days(
            list(map(lambda x: strptime(x, "%H:%M %d.%m.%y"), times[timename]))
        )
        for t in _t:
            if t not in time:
                time.append(t)
    return list(map(lambda x: strptime(x, "%d.%m.%y"), time))

def _to_human_form(date: struct_time):
    return strftime("%d.%m.%y", date)

def _remove_all_replit_times(times: dict):
    all_days = _get_all_days_on_dict(times)
    all_cons = []
    all_discons = []
    for days in all_days:
        connects_on_day = _get_date_of_day(
            list(map(lambda x: strptime(x, "%H:%M %d.%m.%y"), times['connects'])), days)
        disconnects_on_day = _get_date_of_day(
            list(map(lambda x: strptime(x, "%H:%M %d.%m.%y"), times['discovers'])), days)

        connects_on_day, disconnects_on_day = _rm_repit_times(
            connects_on_day,
            disconnects_on_day
        )

        all_cons.append(connects_on_day)
        all_discons.append(disconnects_on_day)

    return [all_cons, all_discons]


class Getter:

    def __init__(self, filename: str=None, tested: bool=False):
        self._tested = tested
        self._filename = filename
        self._test_filename = 'test_files/test_log.txt'
        self._pattern = re.compile(r"\[A-Z] ")

        if not exists(self._test_filename if self._tested else self._filename):
            with open(self._test_filename if self._tested else self._filename, 'w', encoding='utf-8') as file:
                file.write('')

    def _get_STA(self, line: str) -> str:
        line = line.split('STA')
        line = line[1].split()[0][1:-1]
        # print(line)
        return line

    # def _calc_times(self, con:struct_time) -> int:
    #     disc = strptime("19:00 " + strftime("%d.%m.%y", con), "%H:%M %d.%m.%y")
    #     return ((con.tm_hour * 60 * 60) + (con.tm_min * 60) + (con.tm_sec)) // ((disc.tm_hour * 60 * 60) + (disc.tm_min * 60) + (disc.tm_sec))

    def _is_mac_address(self, string: str) -> bool:
        pattern = "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
        if re.match(pattern, string):
            return True
        else:
            return False

    # def parse_string(self, string:str) -> dict:
    #     data = {}
    #     lines = string.splitlines()
    #     for line in lines:
    #         if line.startswith('<14>'):
    #             line = line[4:]
    #         splitted_line = line.split()
    #         mac = splitted_line[-1][:-1]
    #         if not self._is_mac_address(mac):
    #             continue
    #         time = strptime(" ".join(splitted_line[:3]) + strftime(' %Y'), "%b %d %H:%M:%S %Y")
    #
    #         if data.get(mac) is None:
    #             data[mac] = {
    #                 'discovers': [],
    #                 'connects': []
    #             }
    #
    #         if "DHCPREQUEST" in line:
    #             data[mac]['connects'].append(strftime("%H:%M %d.%m.%y", time))
    #         elif "DHCPDISCOVER" in line:
    #             data[mac]['discovers'].append(strftime("%H:%M %d.%m.%y", time))
    #         elif "deauthenticated" in line:
    #             mac = line.split()[7][4:-1]
    #             if not self._is_mac_address(mac):
    #                 continue
    #             data[mac]['discovers'].append(strftime("%H:%M %d.%m.%y", time))
    #         else:
    #             continue
    #     return data

    def _format_system_log(self, line: str) -> str:
        return self._pattern.sub("<14>", line)

    def parse_file(self) -> dict:
        '''
        Test dictionary:
        {
            'mac': {
                'discovers': [...],
                'connects': [...]
            }
        }
        '''
        data = {}
        with open(self._test_filename if self._tested else self._filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        for line in lines:
            if line.startswith('<14>'):
                line = line[4:]
            elif line.startswith('[') and line.split()[0].endswith(']'):
                #line = self._format_system_log(line)
                raise
            else:
                continue
            splitted_line = line.split()
            try:
                time = strptime(
                    " ".join(splitted_line[:3]) + strftime(' %Y'), "%b %d %H:%M:%S %Y")
                mac = splitted_line[-1][:-1]
            except Exception as ex:
                continue
            if not self._is_mac_address(mac):
                if "deauthenticated" in line:
                    mac = self._get_STA(line)
                    if not self._is_mac_address(mac):
                        continue
                    if data.get(mac) is None:
                        data[mac] = {
                            'discovers': [],
                            'connects': []
                        }
                    data[mac]['discovers'].append(
                        strftime("%H:%M %d.%m.%y", time))
                else:
                    continue

            if data.get(mac) is None:
                data[mac] = {
                    'discovers': [],
                    'connects': []
                }

            # print(
            #     "DHCPREQUEST" in line, line, "\n",
            #     "DHCPDISCOVER" in line, line, "\n",
            #     "deauthenticated" in line, line, "\n"
            # )

            if "DHCPREQUEST" in line:
                data[mac]['connects'].append(strftime("%H:%M %d.%m.%y", time))
            elif "DHCPDISCOVER" in line:
                data[mac]['discovers'].append(strftime("%H:%M %d.%m.%y", time))
            else:
                continue
        return data

    def calculate_times(self, parsed_log: dict) -> dict:
        '''
        return this (example)
        {
            "mac": {"date": "hours", "date2": "hours"},
            "mac2": {"date": "hours", "date2": "hours"},
            "mac3": {"date": "hours", "date2": "hours"},
        }
        '''
        #print(parsed_log)
        to_ret = {}
        for mac, data in parsed_log.items():
            to_ret[mac] = _remove_all_replit_times(data)
        return to_ret
