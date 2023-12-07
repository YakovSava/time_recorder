import re

from os.path import exists
from time import strptime, strftime, struct_time

class Getter:

    def __init__(self, filename:str=None, tested:bool=False):
        self._tested = tested
        self._filename = filename
        self._test_filename = 'test_files/test_log.txt'

        if not exists(self._test_filename if self._tested else self._filename):
            with open(self._test_filename if self._tested else self._filename, 'w', encoding='utf-8') as file:
                file.write('')

    def _get_STA(self, line:str) -> str:
        line = line.split('STA')
        line = line[1].split()[0][1:-1]
        #print(line)
        return line

    def _calc_times(self, con:struct_time) -> int:
        disc = strptime("19:00 " + strftime("%d.%m.%y", con), "%H:%M %d.%m.%y")
        return ((con.tm_hour * 60 * 60) + (con.tm_min * 60) + (con.tm_sec)) // ((disc.tm_hour * 60 * 60) + (disc.tm_min * 60) + (disc.tm_sec))

    def _is_mac_address(self, string:str) -> bool:
        pattern = "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
        if re.match(pattern, string):
            return True
        else:
            return False

    def parse_string(self, string:str) -> dict:
        data = {}
        lines = string.splitlines()
        for line in lines:
            if line.startswith('<14>'):
                line = line[4:]
            splitted_line = line.split()
            mac = splitted_line[-1][:-1]
            if not self._is_mac_address(mac):
                continue
            time = strptime(" ".join(splitted_line[:3]) + strftime(' %Y'), "%b %d %H:%M:%S %Y")

            if data.get(mac) is None:
                data[mac] = {
                    'discovers': [],
                    'connects': []
                }

            if "DHCPREQUEST" in line:
                data[mac]['connects'].append(strftime("%H:%M %d.%m.%y", time))
            elif "DHCPDISCOVER" in line:
                data[mac]['discovers'].append(strftime("%H:%M %d.%m.%y", time))
            elif "deauthenticated" in line:
                mac = line.split()[7][4:-1]
                if not self._is_mac_address(mac):
                    continue
                data[mac]['discovers'].append(strftime("%H:%M %d.%m.%y", time))
            else:
                continue
        return data

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
            splitted_line = line.split()
            try:
                time = strptime(" ".join(splitted_line[:3]) + strftime(' %Y'), "%b %d %H:%M:%S %Y")
                mac = splitted_line[-1][:-1]
            except Exception as ex:
                continue
            if not self._is_mac_address(mac):
                if "deauthenticated" in line:
                    #print(line)
                    mac = self._get_STA(line)
                    #print(self._is_mac_address(mac))
                    if not self._is_mac_address(mac):
                        #print(mac)
                        continue
                    if data.get(mac) is None:
                        data[mac] = {
                            'discovers': [],
                            'connects': []
                        }
                    data[mac]['discovers'].append(strftime("%H:%M %d.%m.%y", time))
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


    def _calculate_connected_time(self, data:dict) -> dict:

        times = {}
        #print(data)
        connects = []
        discovers = []

        for con in data['connects']:
            connects.append(strptime(con, '%H:%M %d.%m.%y'))
        for disc in data['discovers']:
            discovers.append(strptime(disc, '%H:%M %d.%m.%y'))

        if len(connects) == 0:
            return {}

        for con in connects:
            try:
                filtered_discovers = sorted(list(
                        filter(
                            lambda x: ((con.tm_mday == x.tm_mday) and (con.tm_mon == x.tm_mon) and (con.tm_year == x.tm_year)),
                            discovers
                        )
                    ),
                    key=lambda x: (x.tm_hour * 3600) + (x.tm_min * 60) + (x.tm_sec)
                )[-1]
            except Exception as ex:
                #print(ex)
                filtered_discovers = 0
            if filtered_discovers == 0:
                times[strftime("%d.%m.%y", con)] = self._calc_times(con)
                continue
            if times.get(strftime("%d.%m.%y", con)) is not None:
                new = self._calculate_connected(con, filtered_discovers)
                if new > times[strftime("%d.%m.%y", con)]:
                    times[strftime("%d.%m.%y", con)] = new
                    continue
            times[strftime("%d.%m.%y", con)] = self._calculate_connected(con, filtered_discovers)
        return times

    def calculate_times(self, parsed_log:dict) -> dict:
        '''
        return this (example)
        {
            "mac": {"date": "hours", "date2": "hours"},
            "mac2": {"date": "hours", "date2": "hours"},
            "mac3": {"date": "hours", "date2": "hours"},
        }
        '''
        to_ret = {}
        for mac, data in parsed_log.items():
            to_ret[mac] = self._calculate_connected_time(data)
        return to_ret

    def _calculate_connected(self, con:struct_time, filtered_discovers:struct_time) -> int:
        #print(f"Connect: {con}\nDisconnect: {filtered_discovers}")
        _t = ((filtered_discovers.tm_hour * 60 * 60) + (filtered_discovers.tm_min * 60) + (filtered_discovers.tm_sec)) - ((con.tm_hour * 3600) + (con.tm_min * 60) + (con.tm_sec))
        return (_t if _t > 0 else 0) // (60 * 60)