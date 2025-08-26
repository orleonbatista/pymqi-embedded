#include <Python.h>

static PyObject* stub(PyObject* self, PyObject* args) {
    return PyUnicode_FromString("IBM MQ client not embedded in tests.");
}

static PyMethodDef methods[] = {
    {"stub", stub, METH_NOARGS, "Return a stub message."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "_pymqi",
    "Stub C extension",
    -1,
    methods
};

PyMODINIT_FUNC PyInit__pymqi(void) {
    return PyModule_Create(&module);
}
