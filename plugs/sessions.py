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
                'discovers': {},
                'connects': {}
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
                    'discovers': {},
                    'connects': {}
                }

            if ('DHCPDISCOVER' in line):
                data[mac]['discovers'][strftime("%d-%m%y", time)] = mktime(time)
            elif ('DHCPREQUEST' in line):
                data[mac]['connects'][strftime("%d-%m%y", time)] = mktime(time)
        return data