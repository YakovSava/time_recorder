import re

from time import strptime, strftime, gmtime
from datetime import datetime, time as dtime
from pprint import pprint

class Getter:

    def __init__(self, filename:str=None, tested:bool=False):
        self._tested = tested
        self._filename = filename
        self._test_filename = 'test_files/test_log.txt'

    def _is_mac_address(self, string:str) -> bool:
        pattern = "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
        if re.match(pattern, string):
            return True
        else:
            return False

    def parse_string(self, string:str) -> dict:
        data = {}
        for line in string.splitlines():
            splitted_line = line.split()
            mac = splitted_line[-1][-1:]
            time = strptime(" ".join(splitted_line[1:4]) + strftime(' %Y'), "%H:%M %d.%m.%y")

            if data.get(mac) is None:
                data[mac] = {
                    'discovers': [],
                    'connects': []
                }

            if "DHCPREQUEST" in line:
                data[mac]['connects'].append(time)
            elif "DHCPDISCOVER" in line:
                data[mac]['discovers'].append(time)
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
            time = strptime(" ".join(splitted_line[1:4]) + strftime(' %Y'), "%b %d %H:%M:%S %Y")

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
        connected_time_by_date = {}

        for i, connect_time in enumerate(data['connects']):
            try:
                connect_datetime = datetime.strptime(connect_time, "%H:%M %d.%m.%y")

                connect_date = connect_datetime.date()

                if i == len(data['connects']) - 1 and data['discovers'][i]:
                    prev_disconnect_datetime = datetime.strptime(data['discovers'][i], "%H:%M %d.%m.%y")
                    connected_time_by_date[connect_date] += connect_datetime - prev_disconnect_datetime
                elif connect_date in connected_time_by_date:
                    prev_disconnect_datetime = datetime.strptime(data['discovers'][i], "%H:%M %d.%m.%y")
                    connected_time_by_date[connect_date] += connect_datetime - prev_disconnect_datetime
                else:
                    connected_time_by_date[connect_date] = connect_datetime - connect_datetime.replace(hour=0,
                                                                                                       minute=0)
            except:
                continue

        return self._transform_into_human_form(connected_time_by_date)


    def _transform_into_human_form(self, data:dict) -> dict:
        new_data = {}
        for key, data in data.items():
            new_data[strftime('%d.%m.%y', gmtime(datetime.combine(key, dtime()).timestamp()))] = abs(round(data.total_seconds() / 3600, 2))
        return new_data

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