import re

from os.path import exists
from time import strptime, strftime, struct_time,\
    mktime, gmtime, time
from pprint import pprint

def _today(day:str) -> bool:
    return strftime("%H:%M %d.%m.%y", gmtime(time())).endswith(day)

def _to_str(data:float) -> str:
    return strftime("%H:%M %d.%m.%y", gmtime(data))


def _get_date_of_day(dates: list[struct_time], day: struct_time) -> list[struct_time]:
    return list(
        filter(
            lambda x: ((x.tm_mday == day.tm_mday) and (
                x.tm_mon == day.tm_mon) and (x.tm_year == day.tm_year)),
            dates
        )
    )

def _rm_repit_times(cons: list[struct_time], discs: list[struct_time]) -> list[list[str], list[str]]:
    connects = []
    disconnects = []
    for con in cons:
        if _to_str(mktime(con)) not in connects:
            connects.append(_to_str(mktime(con)))

    for disc in discs:
        if (_to_str(mktime(disc)) not in disconnects) and (_to_str(mktime(disc)) not in connects):
            disconnects.append(_to_str(mktime(disc)))

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

        all_cons.append((connects_on_day))
        all_discons.append((disconnects_on_day))

    return [all_cons, all_discons]

def _to_unix(date:str) -> float:
    return mktime(strptime(date, "%H:%M %d.%m.%y"))

def _not_disconnected(date:str="%d.%m.%y") -> str:
    return strftime("%H:%M %d.%m.%y", strptime("18:00 "+date, "%H:%M %d.%m.%y"))

def _not_connected(date:str="%d.%m.%y") -> str:
    return strftime("%H:%M %d.%m.%y", strptime("8:00 "+date, "%H:%M %d.%m.%y"))

def _get_day(data:str) -> str:
    return data[-8:]

def _get_index(lst:list, index:int):
    try:
        return lst[index]
    except:
        return 0

def _get_day_force(data):
    for item in data:
        try:
            return _get_day(item)
        except:
            pass
    return False

def _count_all_the_times_in_all_the_lists(obj:list | float) -> float:
    if isinstance(obj, float):
        return obj
    res = 0.0
    for con, dis in obj:
        res += _to_unix(dis) - _to_unix(con)
    return abs(round(res / 3600, 2))

def _comparison_con_and_discon_on_day(cons:list[str], discons:list[str]) -> tuple | list:
    if len(discons) == 0:
        min = sorted(map(_to_unix, cons))[0]
        if _today(_get_day(_to_str(min))):
            return [[_to_str(min), strftime("%H:%M %d.%m.%y", gmtime(time()))]]
        return [[_to_str(min), _not_disconnected(_get_day(_to_str(min)))]]
    if len(cons) == 0:
        max = sorted(map(_to_unix, discons))[-1]
        return [[_not_connected(_get_day(discons[0])), _to_str(max)]]
    if len(cons) < len(discons):
        associated = []
        already_associated = []

        for index in range(0, len(cons)):
            for di_index in range(0, len(discons)):
                if cons[index] in already_associated:
                    if (_to_unix(already_associated[-1]) < _to_unix(discons[di_index])):
                        if _get_index(cons, index+1):
                            if _to_unix(already_associated[-1]) < _to_unix(discons[di_index]) < _to_unix(cons[index+1]):
                                associated.pop()
                                already_associated.pop()
                                already_associated.pop()

                                associated.append([cons[index], discons[di_index]])
                                already_associated.append(cons[index])
                                already_associated.append(discons[di_index])
                            else:
                                continue

                        associated.pop()
                        already_associated.pop()
                        already_associated.pop()

                        associated.append([cons[index], discons[di_index]])
                        already_associated.append(cons[index])
                        already_associated.append(discons[di_index])
                else:
                    if _to_unix(discons[di_index]) - _to_unix(cons[index]) > 0:
                        associated.append([cons[index], discons[di_index]])
                        already_associated.append(cons[index])
                        already_associated.append(discons[di_index])
        if _today(_get_day(associated[-1][-1])) and (time() < _to_unix(associated[-1][-1])):
            associated[-1][-1] = _to_str(time())
        return associated
    if len(discons) <= len(cons):
        associated = []
        already_associated = []

        for index in range(0, len(cons)):
            for di_index in range(0, len(discons)):
                if cons[index] in already_associated:
                    if (_to_unix(already_associated[-1]) < _to_unix(discons[di_index])):
                        if _get_index(cons, index + 1):
                            if _to_unix(already_associated[-1]) < _to_unix(discons[di_index]) < _to_unix(
                                    cons[index + 1]):
                                associated.pop()
                                already_associated.pop()
                                already_associated.pop()

                                associated.append([cons[index], discons[di_index]])
                                already_associated.append(cons[index])
                                already_associated.append(discons[di_index])
                                continue
                            else:
                                continue

                        associated.pop()
                        already_associated.pop()
                        already_associated.pop()

                        associated.append([cons[index], discons[di_index]])
                        already_associated.append(cons[index])
                        already_associated.append(discons[di_index])
                else:
                    if _to_unix(discons[di_index]) - _to_unix(cons[index]) > 0:
                        if _get_index(already_associated, -2):
                            if (_to_unix(already_associated[-2]) < _to_unix(cons[index])) and (_to_unix(already_associated[-1]) - _to_unix(cons[index]) > 0):
                                continue
                        associated.append([cons[index], discons[di_index]])
                        already_associated.append(cons[index])
                        already_associated.append(discons[di_index])

        return associated


def _analyze(data:list) -> dict:
    to_ret = {}

    for connects, disconnects in zip(*data):
        to_ret[_get_day_force(connects) if _get_day_force(connects) else _get_day_force(disconnects)] = _count_all_the_times_in_all_the_lists(_comparison_con_and_discon_on_day(connects, disconnects))

    return to_ret


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

    def extract_mac_address(self, text: str) -> str:
        """
        Функция извлекает MAC-адрес из заданного текста.

        Args:
          text: Строка, содержащая MAC-адрес.

        Returns:
          Строка с MAC-адресом.
        """
        # Регулярное выражение для поиска MAC-адреса
        pattern = r"(?:\(|\[)([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})(?:\)|\])"

        # Поиск MAC-адреса в тексте
        match = re.search(pattern, text)

        # Возвращение MAC-адреса, если он был найден
        if match:
            return str(match.group(0))[1:-1]

        # Возвращение пустой строки, если MAC-адрес не найден
        return ""

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
            time = strptime(
                " ".join(line.split()[:3]) + strftime(' %Y'), "%b %d %H:%M:%S %Y")
            mac = self.extract_mac_address(line)

            if data.get(mac) is None:
                data[mac] = {
                    'discovers': [],
                    'connects': []
                }

            if 'associated' in line:
                data[mac]['connects'].append(strftime("%H:%M %d.%m.%y", gmtime(mktime(time)-(5*3600))))
            elif 'deauthenticated' in line:
                data[mac]['discovers'].append(strftime("%H:%M %d.%m.%y", gmtime(mktime(time)-(5*3600))))

            # print(
            #     "DHCPREQUEST" in line, line, "\n",
            #     "DHCPDISCOVER" in line, line, "\n",
            #     "deauthenticated" in line, line, "\n"
            # )
            # if "DHCPREQUEST" in line:
            #     data[mac]['connects'].append(strftime("%H:%M %d.%m.%y", time))
            # elif "DHCPDISCOVER" in line:
            #     data[mac]['discovers'].append(strftime("%H:%M %d.%m.%y", time))
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
        prepare = {}
        for mac, data in parsed_log.items():
            prepare[mac] = _remove_all_replit_times(data)
        to_ret = {}

        pprint(prepare)

        for mac, val in prepare.items():
            to_ret[mac] = _analyze(val)

        return to_ret
