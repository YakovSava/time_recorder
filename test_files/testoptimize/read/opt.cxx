# include <fstream>
# include <string_view>
# include <Python.h>
using namespace std;

static PyObject* string_to_str(string c_str) {
	return PyUnicode_FromString(c_str.c_str());
}

const char* str_to_string(PyObject* python_string) {
	return PyUnicode_AsUTF8(python_string);
}

int Cwrite(const char* filename, const char* lines) {
		FILE* fm = fopen(filename, "wt");

		if (fm == NULL) {

				return 0;
		} else {

				fprintf(fm, "%s", lines);
				fclose(fm);

				return 1;
		}
}

string Cread(const string filename) {
	ifstream file(filename, ios::binary);

	  // Получение размера файла
	  file.seekg(0, ios::end);
	  streamsize fileSize = file.tellg();
	  file.seekg(0, ios::beg);

	  // Выделение памяти для буфера
	  string buffer(fileSize, '\0');

	  // Чтение файла в буфер
	  file.read(&buffer[0], fileSize);

	  // Закрытие файла
	  file.close();

	  return buffer;
}

static PyObject* write(PyObject *self, PyObject *args) {
	PyObject* filename_obj;
	PyObject* data_obj;

	if (!PyArg_ParseTuple(args, "UU", &filename_obj, &data_obj)) {
		return NULL;
	}

	int result = Cwrite(str_to_string(filename_obj), str_to_string(data_obj));

	return Py_BuildValue("i", result);
}

static PyObject* read(PyObject* self, PyObject* args) {
	PyObject* filename;

	if (!PyArg_ParseTuple(args, "U", &filename)) {
		return NULL;
	}

	string result = Cread(str_to_string(filename));

	return string_to_str(result);
}

static PyMethodDef methods[] = {
	{"read", read, METH_VARARGS, "Reading a file using the low-level C++ programming language"},
	{"write", write, METH_VARARGS, "Writing to file using the low-level C++ programming language"},
	{NULL, NULL, 0, NULL} 
};

static struct PyModuleDef module = {
		PyModuleDef_HEAD_INIT,
		"opt",
		"Aaaaaaaaaaaaaaaaaa",
		-1,
		methods
};

PyMODINIT_FUNC PyInit_opt(void) {
		return PyModule_Create(&module);
}