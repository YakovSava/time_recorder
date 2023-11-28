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
            if line.startswith('[I]'):
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
            if line.startswith('[I]]'):
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
        print(data)
        connects = []
        discovers = []

        for con in data['connects']:
            connects.append(strptime('%H:%M %d.%m.%y', con))
        for disc in data['discovers']:
            discovers.append(strptime('%H:%M %d.%m.%y', disc))

        for con in connects:
            days_discovers = []
            for disc in discovers:
                if (con.tm_mday == disc.tm_mday) and (con.tm_mon == disc.tm_mon) and (con.tm_year == con.tm_year):
                    days_discovers.append(disc)


        return ...


    def _transform_into_human_form(self, data:dict) -> dict:
        ...

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