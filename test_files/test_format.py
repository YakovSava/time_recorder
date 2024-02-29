from time import strptime, strftime, mktime, gmtime

time = {'00:27:0e:12:46:7c': [[['17:05 29.01.24'],
      ['11:57 08.02.24', '15:27 08.02.24', '16:17 08.02.24'],
      ['12:05 09.02.24', '15:35 09.02.24'],
      ['13:08 10.02.24', '16:38 10.02.24'],
      ['19:25 11.02.24']],
      [[], [], [], [], []]],
 '32:9a:21:4a:7f:d8': [[['08:19 12.02.24']], [[]]],
 '3a:75:ff:70:04:09': [[['08:29 08.02.24',
       '11:59 08.02.24',
       '15:29 08.02.24',
       '16:17 08.02.24'],
      ['13:08 10.02.24',
       '16:38 10.02.24',
       '16:53 10.02.24',
       '17:03 10.02.24',
       '17:23 10.02.24',
       '17:32 10.02.24',
       '17:43 10.02.24',
       '17:53 10.02.24'],
      ['08:24 12.02.24']],
      [[],
      ['16:57 10.02.24',
       '17:07 10.02.24',
       '17:28 10.02.24',
       '17:35 10.02.24',
       '17:51 10.02.24'],
      []]],
 '50:a1:32:1d:88:af': [[['19:45 11.02.24'], ['08:21 12.02.24']], [[], []]],
 '50:ff:20:a0:e3:c4': [[], []],
 '50:ff:20:a0:e3:c5': [[], []],
 '52:ff:20:a0:e3:c3': [[], []],
 '64:a2:00:a1:bf:94': [[['13:01 08.02.24', '16:31 08.02.24'],
      ['13:28 09.02.24', '16:58 09.02.24'],
      ['10:01 10.02.24', '13:31 10.02.24', '17:01 10.02.24']],
      [[], [], []]],
 '8c:7a:3d:8c:44:be': [[['09:44 08.02.24', '13:14 08.02.24', '16:44 08.02.24'],
      ['09:04 09.02.24', '12:34 09.02.24', '16:04 09.02.24'],
      ['08:54 12.02.24']],
      [[], [], []]],
 'ba:60:e9:e8:a0:eb': [[['12:16 08.02.24'],
      ['18:21 09.02.24'],
      ['14:45 10.02.24', '15:31 10.02.24', '16:04 10.02.24']],
      [[], [], []]],
 'c2:77:14:2f:b9:41': [[[],
      ['09:50 09.02.24', '10:29 09.02.24'],
      ['12:01 10.02.24'],
      ['19:42 11.02.24'],
      ['08:22 12.02.24']],
      [['10:01 08.02.24'],
      ['10:30 09.02.24'],
      ['12:00 10.02.24'],
      [],
      []]],
 'c2:eb:ea:56:80:85': [[['16:03 08.02.24']], [[]]],
 'f8:ab:82:5a:ea:22': [[['08:35 09.02.24', '12:05 09.02.24', '15:35 09.02.24']],
      [[]]]}

def _to_unix(date:str) -> float:
    return mktime(strptime(date, "%H:%M %d.%m.%y"))

def _not_disconnected(date:str="%d.%m.%y") -> str:
    return strftime("%H:%M %d.%m.%y", strptime("18:00 "+date, "%H:%M %d.%m.%y"))

def _not_connected(date:str="%d.%m.%y") -> str:
    return strftime("%H:%M %d.%m.%y", strptime("8:00 "+date, "%H:%M %d.%m.%y"))

def _to_str(data:float) -> str:
    return strftime("%H:%M %d.%m.%y", gmtime(data))

def _get_day(data:str) -> str:
    return data[-8:]

def _str_to_unix(strs:list[str]) -> list[float]:
    return list(map(_to_unix, strs))

def _get_connects_and_disconnects_on_day(day:str, cons_discons:list[str]) -> list[str]:
    result = []
    for cd in cons_discons:
        if cd.endswith(day):
            result.append(cd)
    return result

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

def _comparison_con_and_discon_on_day(cons:list[str], discons:list[str]) -> tuple | list | float:
    if len(discons) == 0:
        min = sorted(map(_to_unix, cons))[0]
        return [[_to_str(min), _not_disconnected(_get_day(cons[0]))]]
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
        print(connects, disconnects)
        to_ret[_get_day_force(connects) if _get_day_force(connects) else _get_day_force(disconnects)] = _count_all_the_times_in_all_the_lists(_comparison_con_and_discon_on_day(connects, disconnects))

    return to_ret

def _main_calculate_times(data:dict):
    to_ret = {}

    for mac, val in data.items():
        to_ret[mac] = _analyze(val)

    return to_ret

if __name__ == '__main__':
    print(_main_calculate_times(time))