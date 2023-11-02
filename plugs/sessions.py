from time import strptime, strftime

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
                'discovers': 5,
                'connects': 5,
                'times': {
                    '01.01': 12, // hours
                    '02.01': 11,
                    '05.01': 5
                }
            }
        }
        '''
        data = {}
        with open(self._test_filename if self._tested else self._filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        for line in lines:
            splitted_line = line.split()
            mac = splitted_line[-1][-1:]
            time = " ".join(splitted_line[1:4]) + strftime(' %Y')

            if data.get(mac) is None:
                data[mac] = {
                    'discovers': 0,
                    'connects': 0,
                    'times': {}
                }

            if ('DHCPDISCOVER' in line):
                data[mac]['discovers'] += 1
                data[mac]['times'][strftime('%d-%m-%y', time)]
            elif ('DHCPREQUEST' in line):
                ...