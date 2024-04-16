# include <iostream>
# include <Python.h>
# include <string>
# include <map>
# include <vector>
# include <ctime>
# include <algorithm>
# include <sstream>
using namespace std;

// Python dict to C++ map
map<string, int> dict_to_map(PyObject* dict) {
  map<string, int> db;

  PyObject* key = NULL;
  PyObject* value = NULL;
  Py_ssize_t pos = 0;

  while (PyDict_Next(dict, &pos, &key, &value)) {
	string keyStr = PyUnicode_AsUTF8(key);
	int valueStr = PyLong_AsLong(value);

	db[keyStr] = valueStr;
  }
  return db;
}

// C++ string to Pyhton str
static PyObject* string_to_str(string c_str) {
	return PyUnicode_FromString(c_str.c_str());
}

// Python str to C++ string
const char* str_to_string(PyObject* python_string) {
	return PyUnicode_AsUTF8(python_string);
}

// Python list to C++ vector
vector<int> list_to_vector(PyObject* list) {
	vector<int> lst = {};
	Py_ssize_t listSize = PyList_Size(list);
	for (Py_ssize_t i = 0; i < listSize; ++i) {
		PyObject* pyElement = PyList_GetItem(list, i);

		int intValue = PyLong_AsLong(pyElement);
		lst.push_back(intValue);
	}
	return lst;
}

// C++ vector to Python list
static PyObject* vector_to_list(vector<int> lst) {
	PyObject* pyList = PyList_New(0);
	for (int i = 0; i < lst.size(); i++) {
		PyList_Append(pyList, PyLong_FromLong(lst[i]));
	}
	return pyList;
}

bool ends_with(const string& str, const string& suffix) {
  return find_end(str.begin(), str.end(), suffix.begin(), suffix.end()) != str.end();
}

string local_strftime(string type, time_t t) {
	stringstream ss;
	strftime(ss.rdbuf(), 100, type, &t);
	return ss.str();
}

time_t local_strptime(string tim, string type) {
	time_t t;
	strptime(tim, type, &t);
	return t;
}

float to_unix(time_t struct_time) {
	return mktime(struct_time);
}

string to_str(float unix_time) {
	return local_strftime("%H:%M %d.%m.%y", static_cast<time_t>(unix_time));
}

string trim_string(const string& str) {
  size_t pos = 0;
  while (pos < str.length() && str[pos] == ' ') {
    ++pos;
  }

  return str.substr(pos);
}

vector<string> get_date_of_day(vector<string> dates, string day) {
	vector<string> needs;
	for (string date : dates) {
		if (ends_with(date, day)) {
			need.push_back(date);
		}
	}
	return needs;
}

string not_disconnected(string date) {
	return local_strftime("%H:%M %d.%m.%y", local_strptime("18:00 "+date, "%d.%m.%y"));
}

string not_connected(string date) {
	return local_strftime("%H:%M %d.%m.%y", local_strptime("8:00 "+date, "%d.%m.%y"));
}

string get_day(string date) {
	return trim_string(date);
}

bool get_day_force(vector<string> dates) {
	if (dates.size() == 0) {
		return false;
	}
	return true;
}

float get_vector_min(vector<string> data) {
	vector<float> ret;
	for (string item : data) {
		ret.push_back(to_unix(item));
	}
	stable_sort(ret.begin(), ret.end());
	return ret[0];
}

float get_vector_max(vector<string> data) {
	vector<float> ret;
	for (string item : data) {
		ret.push_back(to_unix(item));
	}
	stable_sort(ret.begin(), ret.end());
	return ret[ret.size()-1];
}

vector<vector<string>> comparison_connects_and_disconnects_on_day(vector<string> cons, vector<string> discons) {
	if (discons.size() == 0) {
		float minimal = get_vector_min(cons);
		return {to_str(minimal), not_disconnected(get_day(to_str(minimal)))};
	} else if (cons.size() == 0) {
		float maximal = get_vector_max(discons);
		return {not_connected(get_day(to_str(maximal))), to_str(max)};
	} else if (cons.size() < discons.size()) {
		vector<vector<string>> associated;
		vector<string> already_associated;

		for (int index = 0; index < cons.size(); index++) {
			for (int di_index = 0; di_index < discons.size(); di_index++) {
				if (find(already_associated.begin(), already_associated.end(), cons[index]) != already_associated.end()) {\
					if (cons.size() >= index+1) {
						if (to_unix(already_associated[already_associated.size()-1]) < to_unix(discons[di_index]) < to_unix(cons[index+1])) {
							associated.pop_back();
							already_associated.pop_back();
							already_associated.pop_back();

							associated.push_back({cons[index], discons[di_index]})
							already_associated.push_back(cons[index]);
							already_associated.push_back(discons[di_index]);
						} else {
							continue;
						}
					}
					associated.pop_back();
					already_associated.pop_back();
					already_associated.pop_back();

					associated.push_back({cons[index], discons[di_index]})
					already_associated.push_back(cons[index]);
					already_associated.push_back(discons[di_index]);
				} else {
					if ((to_unix(discons[di_index]) - to_unix(cons[index])) > 0) {
						associated.push_back({cons[index], discons[di_index]})
						already_associated.push_back(cons[index]);
						already_associated.push_back(discons[di_index]);
					}
				}
			}
		}
		return associated;
	} else if (discons.size() <= cons.size()) {
		vector<vector<string>> associated;
		vector<string> already_associated;

		for (int index = 0; index < cons.size(); index++) {
			for (int di_index = 0; di_index < discons.size(); di_index++) {
				if (find(already_associated.begin(), already_associated.end(), cons[index]) != already_associated.end()) {\
					if (cons.size() >= index+1) {
						if (to_unix(already_associated[already_associated.size()-1]) < to_unix(discons[di_index]) < to_unix(cons[index+1])) {
							associated.pop_back();
							already_associated.pop_back();
							already_associated.pop_back();

							associated.push_back({cons[index], discons[di_index]})
							already_associated.push_back(cons[index]);
							already_associated.push_back(discons[di_index]);
						} else {
							continue;
						}
					}
					associated.pop_back();
					already_associated.pop_back();
					already_associated.pop_back();

					associated.push_back({cons[index], discons[di_index]})
					already_associated.push_back(cons[index]);
					already_associated.push_back(discons[di_index]);
				} else {
					if ((to_unix(discons[di_index]) - to_unix(cons[index])) > 0) {
						if (already_associated.size() <= already_associated.size()-2) {
							if ((to_unix(already_associated[already_associated.size()-2]) < to_unix(cons[index])) && ((to_unix(already_associated[already_associated.size()-1]) - to_unix(cons[index])) > 0)) {
								continue;
							}
						}
						associated.push_back({cons[index], discons[di_index]})
						already_associated.push_back(cons[index]);
						already_associated.push_back(discons[di_index]);
					}
				}
			}
		}
		return associated;
	}
}

map<string, vector<vector<string>>> analyze(vector<vector<vector<string>>> data) {
	map<string, vector<vector<string>>> to_ret;
	for (int i = 0; i < data.size(); i++) {
		if (get_day_force(data[i][0])) {
			string day = get_day(data[i][0][0]);
		} else {
			string day = get_day(data[i][1][0]);
		}
		to_ret[day] = comparison_connects_and_disconnects_on_day(data[i][0], data[i][1])
	}
	return to_ret;
}

vector<vector<string>> list_to_vectors(PyObject* list) {
  vector<vector<vector<string>>> result;
  for (Py_ssize_t i = 0; i < PyList_Size(list); ++i) {
    PyObject* sublist = PyList_GetItem(list, i);
    if (PyList_Check(sublist)) {
      result.push_back(list_to_vectors(sublist));
    } else {
      // Преобразование элемента в string
      const char* str = str_to_string(sublist);
      string s(str);
      vector<string> v = {s};
      result.push_back(v);
    }
  }
  return result;
}

vector<vector<vector<string>>> list_to_vectors(PyObject* list) {
  vector<vector<vector<string>>> result;
  for (Py_ssize_t i = 0; i < PyList_Size(list); ++i) {
    PyObject* sublist = PyList_GetItem(list, i);
    if (PyList_Check(sublist)) {
      result.push_back(list_to_vectors(sublist));
    } else {
      // Преобразование элемента в string
      const char* str = str_to_string(sublist);
      string s(str);
      vector<string> v = {s};
      result.push_back(v);
    }
  }
  return result;
}

PyObject* vector_to_lists(const vector<vector<string>> vec) {
  PyObject* list = PyList_New(0);
  for (const auto& str : vec) {
    PyObject* pystr = string_to_str(str);
    PyList_Append(list, pystr);
  }
  return list;
}

PyObject* map_vector_to_python_object(map<string, vector<vector<string>>> data) {
	PyObject* dict = PyDict_New();
  
  	for (const auto& pair : data) {
		PyDict_SetItem(dict, PyUnicode_FromString(pair.first.c_str()), vector_to_lists(pair.second));
  	}

  	return dict;
}

static PyObject* analyze_py_vec(PyObject* self, PyObject* args) {
	PyObject* buffer;
	if (!PyArg_ParseTuple(args, "O", &buffer)) {
        return NULL;
    }

    return map_vector_to_python_object(analyze(list_to_vectors(buffer)));
}

static PyMethodDef methods[] = {
	{"analyze_py_vec", analyze_py_vec, METH_VARARGS, "Test optimize"},
	{NULL, NULL, 0, NULL} 
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "analyze",
    "All possible algorithms that can be useful for creating a website",
    -1,
    methods
};

PyMODINIT_FUNC PyInit_analyze(void) {
    return PyModule_Create(&module);
}