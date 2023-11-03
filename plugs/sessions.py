from time import strptime, strftime
from datetime import datetime

class Getter:

    def __init__(self, filename:str=None, tested:bool=False):
        self._tested = tested
        self._filename = filename
        self._test_filename = 'test_files/test_log.txt'

    def _parse_lines(self) -> dict:
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

    def _transform_into_human_form(self, data:dict) -> dict:
        new_data = {}
        for key, data in data.items():
            new_data[strftime('%d.%m.%y', key.total_seconds())] = data.total_seconds() / 3600
        return new_data

    def _calculate_connected_time(self, log:dict) -> dict:
        connected_time_by_date = {}

        for mac, data in log.items():
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
            to_ret[mac] = self._calculate_connected_time
        return to_ret