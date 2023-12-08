from time import strptime, strftime, mktime, struct_time

times = [
	{'discovers': [], 'connects': []},
	{'discovers': ['09:52 22.11.23', '10:04 22.11.23'], 'connects': ['20:38 01.12.23', '10:04 22.11.23', '13:34 22.11.23', '17:04 22.11.23']},
	{'discovers': [], 'connects': []},
	{'discovers': [], 'connects': []},
	{'discovers': [], 'connects': []},
	{'discovers': ['20:01 21.11.23'], 'connects': ['20:01 21.11.23', '11:55 01.12.23']},
	{'discovers': ['08:56 01.12.23'], 'connects': ['08:56 01.12.23', '13:18 01.12.23']},
	{'discovers': ['09:06 01.12.23'], 'connects': ['09:07 01.12.23', '13:14 01.12.23']},
	{'discovers': ['09:07 01.12.23', '09:45 01.12.23', '10:37 01.12.23', '11:07 01.12.23', '12:13 01.12.23', '13:14 01.12.23', '13:14 01.12.23', '13:40 01.12.23', '13:40 01.12.23', '13:41 01.12.23'], 'connects': ['09:07 01.12.23', '10:23 01.12.23', '10:24 01.12.23', '11:07 01.12.23', '12:12 01.12.23', '13:14 01.12.23', '13:14 01.12.23', '13:40 01.12.23', '13:40 01.12.23', '13:40 01.12.23', '13:41 01.12.23', '13:41 01.12.23']},
	{'discovers': ['09:07 01.12.23'], 'connects': ['09:07 01.12.23', '12:20 01.12.23', '12:22 01.12.23', '12:24 01.12.23', '12:27 01.12.23', '12:29 01.12.23', '13:13 01.12.23', '13:14 01.12.23', '13:15 01.12.23', '13:17 01.12.23', '13:19 01.12.23', '13:21 01.12.23', '13:25 01.12.23', '13:26 01.12.23', '13:37 01.12.23', '13:41 01.12.23', '13:43 01.12.23']},
	{'discovers': ['09:09 01.12.23'], 'connects': ['09:09 01.12.23', '12:39 01.12.23', '13:25 01.12.23', '13:22 22.11.23', '16:52 22.11.23']},
	{'discovers': ['14:03 01.12.23', '20:45 21.11.23', '15:17 27.11.23'], 'connects': ['14:03 01.12.23', '20:45 21.11.23', '20:45 21.11.23', '15:17 27.11.23']},
	{'discovers': ['14:24 01.12.23'], 'connects': ['14:24 01.12.23']}
]

# 9 часов 7 минут

def _sort_st(sts:list[struct_time]) -> struct_time:
	return sorted(sts, key=lambda x: mktime(x))

def _get_minimal_st(sts:list[struct_time]) -> struct_time:
	return _sort_st(sts)[-1]

def _get_maximal_st(sts:list[struct_time]) -> struct_time:
	return _sort_st(sts)[0]

def _str_to_st(string:str) -> struct_time:
	return strptime(string, "%H:%M %d.%m.%y")

def _liststr_to_listst(liststr:list[str]) -> list[struct_time]:
	return list(map(_str_to_st, liststr))

def _get_date_of_day(dates:list[struct_time], day:struct_time) -> list[struct_time]:
	return list(
		filter(
			lambda x: ((x.tm_mday == day.tm_mday) and (x.tm_mon == day.tm_mon) and (x.tm_year == day.tm_year)),
			dates
		)
	)

def _get_minimal_time_on_day(dates:list[struct_time], day:struct_time) -> struct_time:
	return _get_minimal_st(
		_get_date_of_day(dates, day)
	)

def _get_maximal_time_on_day(dates:list[struct_time], day:struct_time) -> struct_time:
	return _get_maximal_st(
		_get_date_of_day(dates, day)
	)

def _rm_repit_times(cons:list[struct_time], discs:list[struct_time]) -> list[list[struct_time], list[struct_time]]:
	connects = []
	disconnects = []
	for con in cons:
		if con not in connects:
			connects.append(con)

	for disc in discs:
		if (disc not in disconnects) and (disc not in connects):
			disconnects.append(disc)

	return [connects, disconnects]

def _get_all_days(dates:list[struct_time]) -> list[str]:
	days = []
	for date in dates:
		day = strftime("%d.%m.%y", date)
		if day not in days:
			days.append(day)
	return days

# def _get_all_days_from_dict(all_dates:list[dict]) -> list[str]:
# 	all_days = []
# 	for date in all_dates:
# 		for date1 in (_get_all_days(date['connects'])):
# 			if date1 not in all_days:
# 				all_days.append(date1)
# 		for date1 in (_get_all_days(date['discovers'])):
# 			if date1 not in all_days:
# 				all_days.append(date1)
# 	return all_days

def _not_disconnected(con:struct_time) -> int:
	day_time = mktime(
		strptime(
			"19:00 "+strftime("%d.%m.%y", con),
			"%H:%M %d.%m.%y"
		)
	) - mktime(con)
	return abs(round(day_time / 3600))

def _not_connected(disc:struct_time) -> int:
	day_time = mktime(disc) - mktime(
		strptime(
			"9:00 "+strftime("%d.%m.%y", disc),
			"%H:%M %d.%m.%y"
		)
	)
	return abs(round(day_time / 3600))

def _get_all_days_on_dict(times:dict) -> list[struct_time]:
	time = []
	for timename in times.keys():
		_t = _get_all_days(
			list(map(lambda x: strptime(x, "%H:%M %d.%m.%y"), times[timename]))
		)
		for t in _t:
			if t not in time:
				time.append(t)
	return list(map(lambda x: strptime(x, "%d.%m.%y"), time))

def _calculate_time(con:struct_time, disc:struct_time) -> int:
	return abs(round((mktime(disc) - mktime(con)) / 3600))

def _to_human_form(date:struct_time):
	return strftime("%d.%m.%y", date)

def analyze(times:dict):
	result = {}

	all_days = _get_all_days_on_dict(times)
	for days in all_days:
		connects_on_day = _get_date_of_day(list(map(lambda x: strptime(x, "%H:%M %d.%m.%y"), times['connects'])), days)
		disconnects_on_day = _get_date_of_day(list(map(lambda x: strptime(x, "%H:%M %d.%m.%y"), times['discovers'])), days)

		connects_on_day, disconnects_on_day = _rm_repit_times(
			connects_on_day,
			disconnects_on_day
		)

		if len(disconnects_on_day) == 0:
			if len(connects_on_day) != 0:
				result[_to_human_form(days)] = _not_disconnected(_get_minimal_st(connects_on_day))
			else:
				result[_to_human_form(days)] = 0
		elif len(connects_on_day) == 0:
			if len(disconnects_on_day) != 0:
				result[_to_human_form(days)] = _not_connected(_get_maximal_st(disconnects_on_day))
			else:
				result[_to_human_form(days)] = 0
		else:
			previously_connect = _get_minimal_st(connects_on_day)
			latest_disconnect = _get_maximal_st(disconnects_on_day)

			result[_to_human_form(days)] = _calculate_time(previously_connect, latest_disconnect)
	return result

if __name__ == '__main__':
	for time in times:
		print(analyze(time))