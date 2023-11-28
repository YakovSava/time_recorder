import re

from os.path import exists
from time import strptime, strftime, gmtime
from datetime import datetime, time as dtime

class Getter:

    def __init__(self, filename:str=None, tested:bool=False):
        self._tested = tested
        self._filename = filename
        self._test_filename = 'test_files/test_log.txt'

        if not exists(self._test_filename if self._tested else self._filename):
            with open(self._test_filename if self._tested else self._filename, 'w', encoding='utf-8') as file:
                file.write('')

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


    def _calculate_connected_time(self, data:dict) -> dict:
        times = {}
        print(data)
        connects = []
        discovers = []

        for con in data['connects']:
            connects.append(strptime(con, '%H:%M %d.%m.%y'))
        for disc in data['discovers']:
            discovers.append(strptime(disc, '%H:%M %d.%m.%y'))

        for con in connects:
            days_discovers = []
            for disc in discovers:
                if (con.tm_mday == disc.tm_mday) and (con.tm_mon == disc.tm_mon) and (con.tm_year == con.tm_year):
                    connected_time = ((disc.tm_hour - con.tm_hour) * 60 * 60) + ((disc.tm_min - con.tm_min) * 60) + (disc.tm_sec - con.tm_sec)
                    if connected_time < 0:
                        continue
                    else:
                        if times.get(strftime('%d.%m.%y', con)) is not None:
                            times[strftime('%d.%m.%y', con)] += connected_time
                        else:
                            times[strftime('%d.%m.%y', con)] = connected_time
            else:
                if times.get(strftime('%d.%m.%y', con)) is not None:
                    times[strftime('%d.%m.%y', con)] = 0
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
            tm = self._calculate_connected_time(data)
            print(tm)
            to_ret[mac] = tm
        return to_ret