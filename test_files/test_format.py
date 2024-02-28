from time import strptime, strftime, struct_time, mktime

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

def _check_in_associated(already_associated:list[list[str]], data:str) -> bool:
    for a in already_associated:
        if data in a:
            return True
    return False

def _comparison_con_and_discon_on_day(cons:list[str], discons:list[str]) -> tuple | list:
    if len(cons) == len(discons):
        return cons, discons
    if len(discons) == 0:
        min = sorted(cons)[0]
        print(min)
        return min, _not_disconnected(_get_day(cons[0]))
    if len(cons) < len(discons):
        associated = []
        for con in cons:
            for disc in discons:
                if len(associated) != 0:
                    if associated[-1][0] != con:
                        if _to_unix(associated[-1][-1]) < _to_unix(disc):
                            associated.pop()
                        else:
                            continue
                    else:
                        break
                if (_to_unix(disc) - _to_unix(con)) > 0:
                    associated.append([con, disc])
        return associated
    if len(discons) < len(cons):
        ...

if __name__ == "__main__":
    cons = ['09:13 28.02.24', '12:20 28.02.24']
    discons = ['10:11 28.02.24', '13:35 28.02.24', '14:20 28.02.24']
    print(_comparison_con_and_discon_on_day(cons, discons))