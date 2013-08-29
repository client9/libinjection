/* libinjection.i SWIG interface file for PHP */
%module libinjection
%{
#include "libinjection.h"
%}

%include "typemaps.i"

// automatically append string length into arg array
%apply (char *STRING, size_t LENGTH) { (const char *s, size_t slen) };

%include "libinjection.h"
