/**
 *
 * libinjection module for python
 *
 * Copyright 2012,2013  Nick Galbreath
 * nickg@client9.com
 * BSD License -- see COPYING.txt for details
 *
 */
#include <Python.h>
#include "sqlparse.h"

static PyObject *
libinjection_detectsqli(PyObject *self, PyObject *args)
{
    const char *userinput;
    int len;
    PyObject* dict = NULL;
    PyObject* value;
    int sqli;
    sfilter sf;

    if (!PyArg_ParseTuple(args, "s#|O!", &userinput, &len, &PyDict_Type, &dict)) {
        return NULL;
    }

    sqli = is_sqli(&sf, userinput, len, NULL, NULL);

    if (dict) {
        value = Py_BuildValue("s", sf.pat);
        if (value == NULL) {
            return NULL;
        }
        if (PyDict_SetItemString(dict, "fingerprint", value) == -1) {
            Py_DECREF(value);
            return NULL;
        }
    }

    if (sqli) {
        Py_RETURN_TRUE;
    } else {
        Py_RETURN_FALSE;
    }
}

static PyMethodDef libinjectionMethods[] = {
    {"detectsqli",  libinjection_detectsqli, METH_VARARGS,
     "Use libinjection to detect sqli from user input."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initlibinjection(void)
{
    PyObject* version;
    PyObject* m = Py_InitModule("libinjection", libinjectionMethods);
    if (m == NULL) {
        return;
    }

    /* PEP 396 - __version__
     * http://www.python.org/dev/peps/pep-0396/
     */
    version = Py_BuildValue("s", LIBINJECTION_VERSION);
    if (version == NULL) {
        return;
    }
    PyModule_AddObject(m, "__version__", version);
}
