/* libinjection.i SWIG interface file */
%module libinjection
%{
#include "libinjection.h"

/* This is the callback function that runs a python function
 *
 */
static int libinjection_python_check_fingerprint(sfilter* sf, void* pyfunc)
{
    int sqli;
    PyObject *arglist;
    PyObject *result;
    // get sfilter->pattern
    // convert to python string
    PyObject* fp = SWIG_NewPointerObj((void*)sf, SWIGTYPE_p_sfilter,0);
    arglist = Py_BuildValue("(N)", fp);
    // call pyfunct with string arg
    result = PyObject_CallObject((PyObject*) pyfunc, arglist);
    Py_DECREF(arglist);
    Py_DECREF(fp);
    if (result == NULL) {
        printf("GOT NULL\n");
        // python call has an exception
        // pass it back
        //return NULL;
    }
    // convert value of python call to true/false
    sqli = PyObject_IsTrue(result);
    if (sqli == -1) {
        //return NULL;
    }
    Py_DECREF(result);
    return sqli;
}

%}
%include "typemaps.i"

// SWIG doesn't natively support fixed sized arrays.
// this typemap converts the fixed size array sfilter.tokevec
// into a list of pointers to stoken_t types. In otherword this code makes this example work
// s = sfilter()
// libinjection_is_sqli(s, "a string",...)
// for i in len(s.pat):
//   print s.tokevec[i].val
//

%typemap(out) stoken_t [ANY] {
int i;
$result = PyList_New($1_dim0);
for (i = 0; i < $1_dim0; i++) {
    PyObject *o =  SWIG_NewPointerObj((void*)(& $1[i]), SWIGTYPE_p_stoken_t,0);
    PyList_SetItem($result,i,o);
}
}

// automatically append string length into arg array
%apply (char *STRING, size_t LENGTH) { (const char *s, size_t slen) };

%typemap(in) (ptr_fingerprints_fn fn, void* callbackarg) {
    if ($input == Py_None) {
        $1 = NULL;
        $2 = NULL;
    } else {
        $1 = libinjection_python_check_fingerprint;
        $2 = $input;
    }
}
%include "libinjection.h"
